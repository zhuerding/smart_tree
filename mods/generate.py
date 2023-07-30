# 这是一个用来生成随机空间推理验证码，并自动生成标注好的yolov5标签的脚本
# 脚本需要在./tutle文件夹所有文件均存在的情况下才能运行
# 运行后output文件夹中有images和labels两个文件夹，images是生成的图片，labels是相对应的yolov5标签文件
import os
from PIL import Image
import random
import numpy


# def decide(information, wid, hig):
#     position = information["position"]
#     original_width = information["width"]
#     original_height = information["height"]
#     a = []
#     if 1.2 * position[0] < wid + width < 1.2 * (position[0] + original_width) or 1.2 * position[0] < wid < 1.2 *(position[0] + original_width):
#         a.append(True)
#     else:
#         a.append(False)
#     if 1.2 * position[1] < hig + height < 1.2 * (position[1] + original_height) or 1.2 * position[1] < hig < 1.2 * (position[1] + original_height):
#         a.append(True)
#     else:
#         a.append(False)
#     if a[0] == a[1]:
#         return True
#     else:
#         return False
#
#
# def rand(width, height):
#     wid = numpy.random.randint(0, 320 - width)
#     hig = numpy.random.randint(0, 160 - height)
#     return wid, hig
#
#
# def rad(width, height, broad):
#     wid, hig = rand(width, height)
#     if broad is not None:
#         for information in broad:
#             while decide(information, wid, hig) is True:
#                 wid, hig = rand(width, height)
#         # for information in broad: position = information["position"] original_width = information["width"]
#         # original_height = information["height"] # print((1.2 * position[0] < wid < 1.2 * (position[0] +
#         # original_width)), (1.2 * position[1] < hig < 1.2 * (position[1] + original_height)))
#     return wid, hig
#
#
# number = random.randint(5, 7)
#
# num1 = random.randint(0, number)
# num2 = number - num1
# path1 = r'F:\pythonProject\yidun\6\A-Z'
# path2 = r'F:\pythonProject\yidun\6\Xa-z'
# out_path = r"F:\pythonProject\yidun\8"
#
# bg = Image.open(r"F:\pythonProject\yidun\picture\background.jpg")  # 打开背景图片
# sep = 51
# with open("predefined_classes.txt", 'r') as f:
#     lst = f.read()
# lst = lst.split('\n')
# while sep <= 100:
#     broad = []
#     bg_copy = bg.copy()  # 创建背景图片的副本
#     if num1 > 0:
#         b = os.listdir(path1)
#         AZ_elements = random.sample(b, num1)
#     if num2 > 0:
#         c = os.listdir(path2)
#         az_elements = random.sample(c, num2)
#     if num1 > 0:
#         for i in AZ_elements:
#             fig_path = os.path.join(path1, i)
#             fg = Image.open(fig_path).convert("RGBA")  # 打开前景图片
#             alpha = fg.split()[-1]
#             width, height = fg.size
#             wid, hig = rad(width, height, broad)
#             information = {
#                 "name": i,
#                 "position": [wid, hig],
#                 "width": width,
#                 "height": height
#             }
#             broad.append(information)
#             position = (wid, hig)
#             fg_copy = fg.copy()  # 创建前景图片的副本
#             bg_copy.paste(fg_copy, position, mask=alpha)  # 将前景图片的副本粘贴到背景图片的副本上，位置为(100, 100)
#     if num2 > 0:
#         for i in az_elements:
#             fig_path = os.path.join(path2, i)
#             fg = Image.open(fig_path).convert("RGBA")  # 打开前景图片
#             alpha = fg.split()[-1]
#             width, height = fg.size
#             wid, hig = rad(width, height, broad)
#             information = {
#                 "name": i,
#                 "position": [wid, hig],
#                 "width": width,
#                 "height": height
#             }
#             broad.append(information)
#             position = (wid, hig)
#             fg_copy = fg.copy()  # 创建前景图片的副本
#             bg_copy.paste(fg_copy, position, mask=alpha)
#     png_output = os.path.join(out_path, "images", f"{sep}.jpg")
#     bg_copy.save(png_output)  # 保存合成后的图片
#     txt_output = os.path.join(out_path, "labels", f"{sep}.txt")
#     with open(txt_output, "a") as p:
#         for unit in broad:
#             width_coordinate = (unit["position"][0] + unit["width"] / 2) / 320
#             height_coordinate = (unit["position"][1] + unit["height"] / 2) / 160
#             width = unit["width"] / 320
#             height = unit["height"] / 160
#             obj = lst.index(unit["name"][:-5])
#             content = f"{obj} {width_coordinate} {height_coordinate} {width} {height}"
#             p.write(content + '\n')
#         p.close()
#     print(broad)
#     print(f'{sep} done!')
#     sep = sep + 1
# 防重叠函数，但是似乎好像没有什么卵用
def decide(information, wid, hig):
    position = information["position"]
    original_width = information["width"]
    original_height = information["height"]
    a = []
    if 1.2 * position[0] < wid + width < 1.2 * (position[0] + original_width) or 1.2 * position[0] < wid < 1.2 *(position[0] + original_width):
        a.append(True)
    else:
        a.append(False)
    if 1.2 * position[1] < hig + height < 1.2 * (position[1] + original_height) or 1.2 * position[1] < hig < 1.2 * (position[1] + original_height):
        a.append(True)
    else:
        a.append(False)
    if a[0] == a[1]:
        return True
    else:
        return False


# 位置随机函数，用于生成字母坐标
def rand(width, height):
    wid = numpy.random.randint(0, 320 - width)
    hig = numpy.random.randint(0, 160 - height)
    return wid, hig


# 忘了干啥的函数
def rad(width, height, broad):
    wid, hig = rand(width, height)
    if broad is not None:
        for information in broad:
            while decide(information, wid, hig) is True:
                wid, hig = rand(width, height)
        # for information in broad: position = information["position"] original_width = information["width"]
        # original_height = information["height"] # print((1.2 * position[0] < wid < 1.2 * (position[0] +
        # original_width)), (1.2 * position[1] < hig < 1.2 * (position[1] + original_height)))
    return wid, hig


# 转译函数
def english(name):
    if name == "黄":
        eng_name = "yellow"
    elif name == "绿":
        eng_name = 'green'
    elif name == "蓝":
        eng_name = "blue"
    elif name == "灰":
        eng_name = "gray"
    else:
        eng_name = "red"
    return eng_name


number = random.randint(5, 7)

num1 = random.randint(0, number)
num2 = 7 - num1
path1 = r'./tutle/A-Z'  # 存放A-Z元件的文件夹
path2 = r'./tutle/Xa-z'  # 存放a-z、数字0-9和立体形状元件的文件夹
out_path = r"./output"  # 生成的验证码输出文件夹
background_path = r'./tutle/background.jpg'

bg = Image.open(background_path)  # 打开背景图片
sep = 0  # 可以修改这个来修改生成的验证码文件名的起始编号
# 判断输出文件夹是否完整
if os.path.exists(os.path.join(out_path, "images")):
    pass
else:
    os.mkdir(os.path.join(out_path, "images"))
if os.path.exists(os.path.join(out_path, "labels")):
    pass
else:
    os.mkdir(os.path.join(out_path, "labels"))
with open(r"./tutle/predefined_classes.txt", 'r') as f:  # 加载标签文件
    lst = f.read()
lst = lst.split('\n')
while sep <= 400:   # 可以修改这个来修改生成的验证码的张数
    broad = []
    bg_copy = bg.copy()  # 创建背景图片的副本
    if num1 > 0:
        b = os.listdir(path1)
        AZ_elements = random.sample(b, num1)
    if num2 > 0:
        c = os.listdir(path2)
        az_elements = random.sample(c, num2)
    if num1 > 0:
        for i in AZ_elements:
            fig_path = os.path.join(path1, i)
            fg = Image.open(fig_path).convert("RGBA")  # 打开前景图片
            alpha = fg.split()[-1]
            width, height = fg.size
            wid, hig = rad(width, height, broad)
            information = {
                "name": i,
                "position": [wid, hig],
                "width": width,
                "height": height
            }
            broad.append(information)
            position = (wid, hig)
            fg_copy = fg.copy()  # 创建前景图片的副本
            bg_copy.paste(fg_copy, position, mask=alpha)  # 将前景图片的副本粘贴到背景图片的副本上，位置为(100, 100)
    if num2 > 0:
        for i in az_elements:
            fig_path = os.path.join(path2, i)
            fg = Image.open(fig_path).convert("RGBA")  # 打开前景图片
            alpha = fg.split()[-1]
            width, height = fg.size
            wid, hig = rad(width, height, broad)
            information = {
                "name": i,
                "position": [wid, hig],
                "width": width,
                "height": height
            }
            broad.append(information)
            position = (wid, hig)
            fg_copy = fg.copy()  # 创建前景图片的副本
            bg_copy.paste(fg_copy, position, mask=alpha)
    png_output = os.path.join(out_path, "images", f"{sep}.jpg")
    bg_copy.save(png_output)  # 保存合成后的图片
    txt_output = os.path.join(out_path, "labels", f"{sep}.txt")
    with open(txt_output, "w") as p:  # 生成yolov5格式的txt文件
        for unit in broad:
            width_coordinate = (unit["position"][0] + unit["width"] / 2) / 320
            height_coordinate = (unit["position"][1] + unit["height"] / 2) / 160
            width = unit["width"] / 320
            height = unit["height"] / 160
            name = unit["name"][:1]
            obj = lst.index(english(name))
            content = f"{obj} {width_coordinate} {height_coordinate} {width} {height}"
            p.write(content + '\n')
        p.close()
    print(broad)
    print(f'{sep} done!')
    sep = sep + 1
