# 这是一个对元件放大缩小的函数，./tutle文件夹里的元件已经去背景随机缩小好了，这个只是上传着玩
from rembg import remove
from PIL import Image
import os
import random
import shutil


def get_folders(directory):
    folders = []  # 创建一个空列表来存放文件夹
    for entry in os.listdir(directory):  # 遍历目录中的所有条目
        if os.path.isdir(os.path.join(directory, entry)):  # 如果条目是文件夹
            folders.append(entry)  # 将条目添加到列表中
    return folders  # 返回列表


out_path = r''  # 元件输出文件夹
path = r""  # 元件输入文件夹

a = get_folders(path)  # 打印F:/Python/PAMC目录下的所有文件夹

# for dir in a:
#     b = os.listdir(path + dir)
#     for i in b:
#         c = os.listdir(path + dir + "/" + i)
#         for tutle in c:
#             input_path = path + dir + "/" + i + '/' + tutle  # 输入图片的路径
#             output_path = path + dir + "/" + i + "/" + tutle  # 输出图片的路径
#             im = Image.open(input_path)  # 打开图片
#             width, height = im.size  # 获取原始宽度和高度
#
#             target_width = int(width * random.randint(18, 25) / 100)  # 定义目标宽度
#             ratio = target_width / width  # 计算宽高比
#             target_height = int(height * ratio)  # 计算目标高度
#
#             im = im.resize((target_width, target_height), Image.LANCZOS)  # 将图片缩小到目标尺寸，使用LANCZOS滤波器
#             im.save(output_path)  # 保存缩小后的图片
#         print(i + ' done!')


# b = os.listdir(path)
# for i in b:
#     input_path2 = os.path.join(path, i)
#     c = os.listdir(input_path2)
#     for tutle in c:
#         input_path = os.path.join(input_path2, tutle)
#         shutil.copy(input_path, out_path)

b = os.listdir(path)
for tutle in b:
    input_path = path + tutle  # 输入图片的路径
    output_path = path + tutle  # 输出图片的路径
    im = Image.open(input_path)  # 打开图片
    width, height = im.size  # 获取原始宽度和高度

    target_width = int(width * random.randint(18, 25) / 100)  # 定义目标宽度
    ratio = target_width / width  # 计算宽高比
    target_height = int(height * ratio)  # 计算目标高度

    im = im.resize((target_width, target_height), Image.LANCZOS)  # 将图片缩小到目标尺寸，使用LANCZOS滤波器
    im.save(output_path)  # 保存缩小后的图片
