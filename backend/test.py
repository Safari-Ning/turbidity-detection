import requests,json
import numpy as np
import os

if __name__=="__main__":
    img_path = "./backend/App/static/img/3.2-45-高.jpg"
    file = {"file": ("file_name.jpg",open(img_path,'rb'), "image/jpg")}
    res = requests.post("http://1.116.14.254:8000/file_upload",files=file)
    resp = json.loads(res.content)
    data = resp["data"]
    box = data["bbox"]
    class_name = data["class"]
    confidence = data["confidence"]
    turbidity = data["turbidity"]
    print(type(box))
    print("D:")