from PIL import Image

def cut_img(img_path,box):
    img=Image.open(img_path)
    #图片剪切crop(x,y,x1,y1)
    im=img.crop(box)
    return im