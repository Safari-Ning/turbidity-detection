import numpy as np
from math import sqrt as sqrt
from App.utils.box_utils import generate_priors

image_mean_test = image_mean = np.array([127, 127, 127])
image_std = 128.0
iou_threshold = 0.3
center_variance = 0.1
size_variance = 0.2

# min_boxes = [[10, 16, 24], [32, 48], [64, 96], [128, 192, 256]]

shrinkage_list = []
# image_size = [320, 240]  # default input size 320*240
image_size = [640, 480]  # default input size 320*240
feature_map_w_h_list = [[40, 20, 10, 5], [30, 15, 8, 4]]  # default feature map size
priors = []
min_boxes_w = None
min_boxes_h = None
net_0={
        'min_boxes_base': [[16, 24], [24,32],[32, 48], [64, 96], [128, 192], [256, 320]],
        'aspect_ratios': [[2], [2],[2],[2],[2, 3], [2, 3]],
} #
net_1 = {
        'min_boxes_base': [[16, 24], [32, 48], [64, 96], [128, 192, 256, 320]],
        'aspect_ratios': [[2], [2, 3], [2, 3], [2]],
} # priors nums:31840

net_2 = {
        'min_boxes_base': [[16, 24], [32, 48], [64, 96], [128, 192, 256, 320]],
        'aspect_ratios': [[2], [2, 3, 4], [2, 3, 4], [2]],
}

net_3 = {
        'min_boxes_base': [[32], [64], [96, 128], [256, 320]],
        'aspect_ratios': [[2], [2], [2], [2]],
}

net_traffic = {
        'min_boxes_base': [[16, 24], [32, 48], [64, 96], [256, 320]],
        'aspect_ratios': [[2], [2], [2], [2]],
}


#net_ = net_1
#net_ = net_2
#net_ = net_3
net_ = net_0
#print('prior box infos: ', net_)
def define_min_max_box_ssd(base,ratio):
    w = []
    h = []
    for i, feature_map in enumerate(base):
        temp_w = []#feature map[16 24]
        temp_h = []
        for b in feature_map:
            temp_h.append(b)#16
            temp_w.append(b)
            for rt in ratio[i]:#rt；2
                temp_h.append(b*sqrt(rt))
                temp_w.append(b/sqrt(rt))
                temp_h.append(b/sqrt(rt))
                temp_w.append(b*sqrt(rt))
        w.append(temp_w)
        h.append(temp_h)
    return w, h
min_boxes_w_640, min_boxes_h_640 = define_min_max_box_ssd(net_['min_boxes_base'], net_['aspect_ratios'])
#print('w_ssd: {} \n h_ssd: {}'.format(min_boxes_w_640, min_boxes_h_640))

def define_img_size(size):
    global image_size, feature_map_w_h_list, priors, min_boxes_w, min_boxes_h
    img_size_dict = {128: [128, 96],
                     160: [160, 120],
                     320: [320, 240],
                     480: [480, 360],
                     640: [640, 480],
                     1280: [1280, 960]}
    image_size = img_size_dict[size]

    # if size == 480:
    #     min_boxes_w = min_boxes_w_480
    #     min_boxes_h = min_boxes_h_480
    # elif size == 640:
    min_boxes_w = min_boxes_w_640
    min_boxes_h = min_boxes_h_640
    # else:
    #     min_boxes_w = min_boxes_w_320
    #     min_boxes_h = min_boxes_h_320

    feature_map_w_h_list_dict = {128: [[16, 8, 4, 2], [12, 6, 3, 2]],
                                 160: [[20, 10, 5, 3], [15, 8, 4, 2]],
                                 320: [[40, 20, 10, 5], [30, 15, 8, 4]],
                                 480: [[60, 30, 15, 8], [45, 23, 12, 6]],
                                 #640: [[80, 40, 20, 10], [60, 30, 15, 8]],
                                 #640:[[80,40,50,20,10,5],[60,30,15,6,2,1]]
                                 640: [[80, 40, 20, 10, 9, 2], [60, 30, 15, 6, 4, 1]],
                                 1280: [[160, 80, 40, 20], [120, 60, 30, 15]]}

    feature_map_w_h_list = feature_map_w_h_list_dict[size]

    for i in range(0, len(image_size)):
        item_list = []
        for k in range(0, len(feature_map_w_h_list[i])):
            item_list.append(image_size[i] / feature_map_w_h_list[i][k])
        shrinkage_list.append(item_list)
    priors = generate_priors(feature_map_w_h_list, shrinkage_list, image_size, min_boxes_w, min_boxes_h)

