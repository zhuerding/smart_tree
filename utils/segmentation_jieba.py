import logging
import random

import jieba
import jieba.posseg as pseg

# strs = ['正向的大写C', "红色大写B", "正向的数字9", "大写L颜色一样的小写n", "红色小写a朝向一样的大写F", "大写W颜色一样的大写S", '大写N颜色一样的数字2',
#         "蓝色大写B朝向一样的球", "侧向的小写e", "请点击绿色数字1朝向一样的大写W"]


# words = pseg.cut(strs[random.randint(0, len(strs))][3:])  # jieba默认模式
# words = pseg.cut(strs[random.randint(0, len(strs))])  # jieba默认模式
def segmentation(content):
    words = pseg.cut(content)
    keys = []
    tag = []
    nam = 0
    jieba.setLogLevel(logging.ERROR)
    for word, flag in words:  # 将请求到的内容按照类型进行分类
        if word not in ['数字']:  # 过滤掉数字这一名词
            keys.append(word)  # 将分词后内容进行储存
            tag.append(flag)
            if word in ['立方体', '圆锥', '圆柱', '球']:
                nam = word
    for i in ['立方体', '圆锥', '圆柱', '球']:
        if i in keys:
            fms = True
        else:
            fms = False
    if fms is False:  # 根据词性进行分类
        if 'r' in tag:  # 如果出现朝向/颜色条件
            adj1 = keys[0:tag.index("x")]  # 获得第一个名词前的所有形容词
            noun1 = {'name': keys[tag.index("x")], 'adj': adj1}  # 获取第一个名词
            attach = keys[tag.index("r") - 1]  # 获取条件朝向/颜色
            adj2 = keys[tag.index("r") + 2:len(keys) - 1]  # 获得第二个名词前的所有形容词
            noun2 = {'name': keys[len(keys) - 1], 'adj': adj2}  # 获取第二个名词
            noun = [noun1, attach, noun2]
        else:
            adj = keys[0:len(keys) - 1]  # 获得名词前的所有形容词
            attach = ''
            noun = [{"name": keys[len(keys) - 1], 'adj': adj}, attach]
    else:
        if 'x' in tag:  # 如果出现字符串内容，如A-Z，1-9
            if keys.index(nam) > tag.index("x"):  # 如果立方体这些内容在字符串内容后
                adj1 = keys[0:tag.index("x")]
                noun1 = {'name': keys[tag.index("x")], 'adj': adj1}
                attach = keys[tag.index("r") - 1]
                adj2 = keys[tag.index("r") + 2:len(keys) - 1]
                noun2 = {'name': keys[len(keys) - 1], 'adj': adj2}
                noun = [noun1, attach, noun2]
            else:
                adj1 = keys[0:keys.index(nam)]
                noun1 = {'name': keys[keys.index(nam)], 'adj': adj1}
                attach = keys[tag.index("r") - 1]
                adj2 = keys[tag.index("r") + 2:len(keys) - 1]
                noun2 = {'name': keys[len(keys) - 1], 'adj': adj2}
                noun = [noun1, attach, noun2]
        else:
            adj = keys[0:len(keys) - 1]
            attach = ''
            noun = [{"name": keys[len(keys) - 1], 'adj': adj}, attach]
    return noun

# {小写，大写}+{字母}+{朝向，颜色}+一样+{大写，小写}+{字母}
# 大写J颜色一样的小写b
# {数字}+{朝向，颜色}+一样+{大写，小写}+{数字}
# 2朝向一样的黄色3
# {颜色}+{小写，大写}+{字母}+{朝向，颜色}+一样+{大写，小写}+{字母}

# {颜色}+{形状}

# {颜色}+{小写，大写}+{字母}

# 圆锥、立方体、圆柱、球体

# {方向}+{字母}
