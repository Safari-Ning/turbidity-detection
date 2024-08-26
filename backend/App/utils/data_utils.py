def get_all_images(src):
    with open(src, 'r',encoding='utf-8') as fr:
        lines = fr.readlines()
    ret = []
    for line in lines:
        if line.startswith('#'):
            name = line[1:].strip()
            ret.append(name)
        else :
            ret.append(line.strip('\n')+'.jpg')
    return ret

def get_classes(src):
    class_string = ""
    with open(src, 'r') as infile:
        for line in infile:
            class_string += line.rstrip()

    # classes should be a comma separated list

    classes = class_string.split(',')
    # prepend BACKGROUND as first class
    classes.insert(0, 'BACKGROUND')

    return classes

def get_all_xmls(src):
    with open(src, 'r') as fr:
        lines = fr.readlines()
    ret = []
    for line in lines:
        if line.startswith('#'):
            name = line[1:].strip()
            ret.append(name)
        else :
            ret.append(line.strip('\n')+'.xml')
    return ret