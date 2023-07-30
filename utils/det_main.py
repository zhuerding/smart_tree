# import cv2
#
# image_path = 'background.jpg'
# image = cv2.imread(image_path)
# first_point = (100, 100)
# last_point = (150, 150)
#
# cv2.rectangle(image, first_point, last_point, (0, 255, 0), 2)
# cv2.imwrite(image_path, image)

# import detect
#
# a = detect.detect(r"F:\pythonProject\yidun\picture\img\589.jpg")
# print(a)


# [{'name': 'CX', 'score': 0.89691246, 'crop': array([248,  26, 289,  73])}, {'name': 'Zu', 'score': 0.89235866,
# 'crop': array([178,  27, 225,  80])}, {'name': 'Cq', 'score': 0.81660295, 'crop': array([ 80,  46, 113,  94])},
# {'name': 'CK', 'score': 0.8690059, 'crop': array([197,  84, 238, 138])}, {'name': 'CK', 'score': 0.8582786,
# 'crop': array([178,  26, 224,  82])}, {'name': 'ZO', 'score': 0.7783948, 'crop': array([24, 22, 71, 74])},
# {'name': 'ZC', 'score': 0.86867243, 'crop': array([251,  73, 303, 124])}, {'name': 'Cu', 'score': 0.8659452,
# 'crop': array([ 54,  87,  92, 137])}]

# 导入必要的库
import random
import cv2
import numpy as np
from sklearn.cluster import KMeans


# 定义函数，将图像转换成数据点
def get_image_data(image_path, information):
    # 加载图像
    image = cv2.imread(image_path)
    crop = information["crop"]
    #  y1 y2 x1 x2
    image = image[crop[1]:crop[3], crop[0]:crop[2]]
    # image = image.astype(np.float64)
    # 调整图像大小
    image = cv2.resize(image, (320, 160))
    # 转化为RGB模式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 将像素值转换成浮点数
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    return image


# 定义函数，获取主颜色
def get_main_colors(image_path, n_colors, information):
    # 获取图像数据
    image = get_image_data(image_path, information)
    # 聚类
    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(image)
    # 获取聚类中心
    color = kmeans.cluster_centers_
    # 将小数值转换为整数值
    color = np.round(color).astype(np.uint8)
    return color


# 优化iou重复的情况，便于更好的输出结果
def de_weight(data):
    # crop = [x1, y1, x2, y2]
    arguments = []
    for tutle in data:
        square = tutle["square"]
        # x1 = tutle["crop"][0]
        # y1 = tutle["crop"][2]
        i = 0
        query = [{
            "name": tutle["name"],
            "score": tutle["score"],
            "index": data.index(tutle)
        }]
        box1 = tutle['crop']
        while i < len(data):
            # if 0.95 < square / data[i]["square"] < 1 or 1 < square / data[i]["square"] < 1.05:
            # and 0.85 * (data[i]["crop"][0] / data[i]["crop"][1]) < x1 / y1 < 1.25 * data[i]["crop"][0] / data[
            # i]["crop"][1]:
            # 寻找标记框重复率达95%以上的标记
            box2 = data[i]["crop"]
            xmin1, ymin1, xmax1, ymax1 = box1
            xmin2, ymin2, xmax2, ymax2 = box2
            p1_x = max(xmin1, xmin2)
            p1_y = max(ymin1, ymin2)
            p2_x = min(xmax1, xmax2)
            p2_y = min(ymax1, ymax2)
            AJoin = 0
            if p2_x > p1_x and p2_y > p1_y:
                AJoin = (p2_x - p1_x) * (p2_y - p1_y)
            A1 = (xmax1 - xmin1) * (ymax1 - ymin1)
            A2 = (xmax2 - xmin2) * (ymax2 - ymin2)
            AUnion = (A1 + A2 - AJoin)
            if AUnion > 0:
                if 1.25 > AJoin / AUnion > 0.40 and AJoin / AUnion != 1:
                    query.append({
                        "name": data[i]["name"],
                        "score": data[i]["score"],
                        "index": i
                    })
            i = i + 1
        # for sep in range(len(query) - 1, -1, -1):  # 倒序遍历
        if len(query) > 1:
            arguments.append(query)
    for argument in arguments:
        tim = 0
        while tim < len(arguments):
            if set(map(frozenset, argument)) == set(map(frozenset, arguments[tim])):
                arguments.remove(arguments[tim])
            tim = tim + 1
    for unit in arguments:  # 重叠的内容按照置信度排序，选择置信度大的
        d = max(unit, key=lambda x: x['score'])
        for i in unit:
            if i is not d:
                index = i["index"]
                data.pop(index)
    return data


# 用于将图片打上颜色和朝向属性
def select(dat, col):
    for i in dat:  # 将朝向进行分类
        if 'C' in i["name"][:1]:
            i["direct"] = 'flank'
            i["name"] = i["name"][1:]
        elif 'Z' in i["name"][:1]:
            i["direct"] = 'front'
            i["name"] = i["name"][1:]
        else:
            i["direct"] = "undirected"
        i["color"] = 'color'
    for i in dat:
        box1 = i["crop"]
        for color in col:
            box2 = color["crop"]
            xmin1, ymin1, xmax1, ymax1 = box1
            xmin2, ymin2, xmax2, ymax2 = box2
            p1_x = max(xmin1, xmin2)
            p1_y = max(ymin1, ymin2)
            p2_x = min(xmax1, xmax2)
            p2_y = min(ymax1, ymax2)
            AJoin = 0
            if p2_x > p1_x and p2_y > p1_y:
                AJoin = (p2_x - p1_x) * (p2_y - p1_y)
            A1 = (xmax1 - xmin1) * (ymax1 - ymin1)
            A2 = (xmax2 - xmin2) * (ymax2 - ymin2)
            AUnion = (A1 + A2 - AJoin)
            if AUnion > 0:
                if 1.25 > AJoin / AUnion > 0.50:
                    i['color'] = color["name"]
    return dat


#  颜色形状转译
def trans_color(color):
    if color == "红色":
        eng_color = 'red'
    elif color == '蓝色':
        eng_color = "blue"
    elif color == '绿色':
        eng_color = 'green'
    elif color == '灰色':
        eng_color = 'gray'
    elif color == '黄色':
        eng_color = 'yellow'
    elif color == '立方体':
        eng_color = 'LFT'
    elif color == '圆锥':
        eng_color = 'YZ'
    elif color == '圆柱':
        eng_color = 'YZT'
    elif color == '球':
        eng_color = 'QX'
    elif color == '侧向':
        eng_color = 'flank'
    elif color == '正向':
        eng_color = 'front'
    elif color == 'o':
        eng_color = 'O'
    elif color == 'v':
        eng_color = 'V'
    else:
        eng_color = color
    return eng_color


#  将所有元素的信息进行整合，以便于主函数的判断
def information(all_data, noun):
    if len(noun) > 2:
        original_name = trans_color(noun[0]["name"])  # 获取问题中元素名
        sep = 0
        eng_color = None
        while sep < len(noun[0]["adj"]):  # 判断问题中是否提到颜色
            if "色" in noun[0]["adj"][sep]:
                eng_color = trans_color(noun[0]["adj"][sep])
            sep = sep + 1
        original_color = eng_color
        question = ''
        if eng_color is not None:  # 如果问题中有颜色
            for item in all_data:
                if original_name == item["name"] and original_color == item["color"]:  # 寻找名字和颜色一样的图像
                    question = item
        else:
            for item in all_data:  # 寻找名字一样的图像
                if original_name in item["name"]:
                    question = item
        if question == '':
            return '没有找到指定的目标，识别失败呜呜'
        answer = ''
        answer_name = noun[2]["name"]

        if noun[1] == '朝向':  # 如果问题要求是朝向一致
            direct = question['direct']
            for i in all_data:
                if direct == i['direct'] and answer_name == i['name']:  # 寻找朝向一致且名字符合要求的图像
                    answer = i
        else:
            color = question['color']
            for i in all_data:
                if color == i['color'] and answer_name == i['name']:  # 寻找颜色一致且名字符合要求的图像
                    answer = i
        if answer == '':
            return '没有找到指定的目标，识别失败呜呜'
        return answer
    else:
        name = trans_color(noun[0]["name"])  # 获取问题中元素名
        sep = 0
        eng_color = None
        eng_direct = None
        while sep < len(noun[0]["adj"]):  # 判断问题中是否提到颜色
            if "色" in noun[0]["adj"][sep]:
                eng_color = trans_color(noun[0]["adj"][sep])
            sep = sep + 1
        while sep < len(noun[0]["adj"]):  # 判断问题中是否提到颜色
            if "向" in noun[0]["adj"][sep]:
                eng_direct = trans_color(noun[0]["adj"][sep])
            sep = sep + 1
        answer = ''
        if eng_color is not None and eng_direct is not None:
            for item in all_data:
                if name == item["name"] and eng_color == item["color"] and eng_direct == item["direct"]:
                    # 寻找名字和朝向颜色一样的图像
                    answer = item
        elif eng_color is not None:  # 如果问题中有颜色
            for item in all_data:
                if name == item["name"] and eng_color == item["color"]:  # 寻找名字和颜色一样的图像
                    answer = item
        elif eng_direct is not None:  # 如果问题中有朝向
            for item in all_data:
                if name in item["name"] and eng_direct == item["direct"]:  # 寻找名字和朝向一样的图像
                    answer = item
        else:
            for item in all_data:  # 寻找名字一样的图像
                if name in item["name"]:
                    answer = item
        if answer == '':
            return '没有找到指定的目标，识别失败呜呜'
        return answer

# a = 3
# information = dat[a]
# n_colors = 1
# colors = get_main_colors(image_path, n_colors, information)
# print(colors)
