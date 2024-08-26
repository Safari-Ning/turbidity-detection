import time
import cv2
import numpy as np

from flask import jsonify,request
from flask.blueprints import Blueprint
from flask.templating import render_template

from App.model_api import detection_predict, regression_predict,batch_detection

blue = Blueprint("blue", __name__)


def init_view(app):
    app.register_blueprint(blue)

@blue.route("/", methods=['GET', 'POST'])
def index():
    return  render_template("./index.html",template_folder='../templates')

@blue.route("/file_upload", methods=['GET','POST'])
def turbidity_detection():
    """单张图片的浊度检测
    """
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"get request")
    file = request.files.get("file")
    img = file.read()
    img = cv2.imdecode(np.frombuffer(img, np.uint8), cv2.IMREAD_COLOR)
    res_data,pil_img = detection_predict(img,"./App/model/MobileNetSSD.onnx")
    if(pil_img!=None):
        turbidity = regression_predict(pil_img,"./App/model/CNNRegression.onnx") 
        turbidity = "{:.3f}".format(turbidity)
        return jsonify({"code":"201",
                        "msg":"成功完成检测",
                        "data":
                            {
                                "turbidity":turbidity,
                                "bbox":res_data[0],
                                "class":res_data[1],
                                "confidence":res_data[2]
                            }
                        })
    else:
        return jsonify({'code': '202', 'msg': '无法检测出待检测区域'})



