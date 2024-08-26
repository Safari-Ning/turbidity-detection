import os


import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image

import App.utils.box_utils_numpy as box_utils
from App.utils.fd_config import define_img_size
from App.utils import fd_config

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


def regression_predict(img, modelfile):
    """@func:回归模块,实现浊度回归
    @param: img:pil格式的图片(对接detection_predict的输出), modelfile:模型文件路径
    @return: turbidity:浊度值
    """
    image = img.resize((64,64))
    image_mean = np.array([0, 0, 0])
    image = (image - image_mean) / 255
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)
    
    sess = ort.InferenceSession(modelfile)
    input_name = sess.get_inputs()[0].name  
    output_name = sess.get_outputs()[0].name

    pred_onnx = sess.run([output_name], {input_name: image})
    
    return pred_onnx[0][0]*10

def getbox(width, height, confidences, boxes, prob_threshold, iou_threshold=0.2, top_k=-1):
    boxes = boxes[0]
    confidences = confidences[0]
    picked_box_probs = []
    picked_labels = []
    for class_index in range(1, confidences.shape[1]):
        probs = confidences[:, class_index]
        mask = probs > prob_threshold
        probs = probs[mask]
        if probs.shape[0] == 0:
            continue
        subset_boxes = boxes[mask, :]
        box_probs = np.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
        box_probs = box_utils.hard_nms(box_probs,
                                        iou_threshold=iou_threshold,
                                        top_k=top_k)
        picked_box_probs.append(box_probs)
        picked_labels.extend([class_index] * box_probs.shape[0])
    if not picked_box_probs:
        return np.array([]), np.array([]), np.array([])
    picked_box_probs = np.concatenate(picked_box_probs)
    picked_box_probs[:, 0] *= width
    picked_box_probs[:, 1] *= height
    picked_box_probs[:, 2] *= width
    picked_box_probs[:, 3] *= height
    return picked_box_probs[:, :4].astype(np.int32), np.array(picked_labels), picked_box_probs[:, 4]



def detection_predict(orig_image,modelfile):
    """@func:检测模块,检测浊度回归区域
    @param: orig_image:原始图片, modelfile:模型文件路径
    @return: result_data:(bbox,class_name,confidence): 检测结果数据, 
        pil_img:根据box值裁剪得到的图片(若box为None则该值为None)
    """
    define_img_size(640)
    

    image = cv2.resize(orig_image, (640, 480))
    
    image_mean = np.array([127, 127, 127])
    image = (image - image_mean) / 128
    image = np.transpose(image, [2, 0, 1])
    image = np.expand_dims(image, axis=0)
    image = image.astype(np.float32)

    

    ort_session = ort.InferenceSession(modelfile)
    input_name = ort_session.get_inputs()[0].name
    
    confidences, boxes = ort_session.run(None, {input_name: image})
    
    boxes = box_utils.convert_locations_to_boxes(boxes, fd_config.priors, 
                                                fd_config.center_variance, 
                                                fd_config.size_variance)
    boxes = box_utils.center_form_to_corner_form(boxes)

    boxes, labels, probs = getbox(orig_image.shape[1], orig_image.shape[0], confidences, boxes, 0.5)

    class_names=['background','beaker']
    
    box = []
    class_name = ''
    confidence = ''
    
    for i in range(boxes.shape[0]):
        box = boxes[i, :]
        box = box.tolist()
        class_name = f"{class_names[labels[i]]}"
        confidence = f"{probs[i]:.2f}"
            
    if(boxes.size>0):
        image_pil = Image.fromarray(cv2.cvtColor(orig_image,cv2.COLOR_BGR2RGB))
        image_pil = image_pil.crop(boxes[0])
    else:
        image_pil = None
    
    return (box,class_name,confidence),image_pil

def batch_detection(img_paths,detection_model_path,regression_model_path):
    """@func:批量检测图片
    @param
    @return valid_list[(img_path,turbidity),(···,···)]:合法数据列表
            invalid_list[img_path,···]:非法数据列表
    """
    valid_list = []
    invalid_list = []
    for img_path in img_paths:
        box_img,pil_img=detection_predict(img_path,detection_model_path)
        if(pil_img!=None):
            turbidity = regression_predict(pil_img,regression_model_path)
            valid_list.append((img_path,turbidity))
        else:
            invalid_list.append(img_path)
    return valid_list,invalid_list
    
if __name__=='__main__':
    pass
