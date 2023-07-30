import onnx
import onnxruntime as ort
import numpy as np

import sys

import onnx
import onnxruntime as ort
import cv2
import numpy as np

CLASSES = ['red', 'gray', 'blue', 'yellow', 'green']  # 识别标签


# CLASSES = ['electrode', 'breathers', 'ventilate', 'press']


class Yolov5ONNX(object):
    def __init__(self, onnx_path):
        """检查onnx模型并初始化onnx"""
        onnx_model = onnx.load(onnx_path)
        try:
            onnx.checker.check_model(onnx_model)
        except Exception:
            print("Model incorrect")
        else:
            pass
        options = ort.SessionOptions()
        options.enable_profiling = True
        # self.onnx_session = ort.InferenceSession(onnx_path, sess_options=options,
        #                                          providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.onnx_session = ort.InferenceSession(onnx_path)
        self.input_name = self.get_input_name()  # ['images']
        self.output_name = self.get_output_name()  # ['output0']

    def get_input_name(self):
        """获取输入节点名称"""
        input_name = []
        for node in self.onnx_session.get_inputs():
            input_name.append(node.name)

        return input_name

    def get_output_name(self):
        """获取输出节点名称"""
        output_name = []
        for node in self.onnx_session.get_outputs():
            output_name.append(node.name)

        return output_name

    def get_input_feed(self, image_numpy):
        """获取输入numpy"""
        input_feed = {}
        for name in self.input_name:
            input_feed[name] = image_numpy

        return input_feed

    def inference(self, img_path):
        """ 1.cv2读取图像并resize
        2.图像转BGR2RGB和HWC2CHW(因为yolov5的onnx模型输入为 RGB：1 × 3 × 640 × 640)
        3.图像归一化
        4.图像增加维度
        5.onnx_session 推理 """
        img = cv2.imread(img_path)
        or_img = cv2.resize(img, (320, 160))  # resize后的原图 (640, 640, 3)
        img = or_img[:, :, ::-1].transpose(2, 0, 1)  # BGR2RGB和HWC2CHW
        img = img.astype(dtype=np.float32)  # onnx模型的类型是type: float32[ , , , ]
        img /= 255.0
        img = np.expand_dims(img, axis=0)  # [3, 640, 640]扩展为[1, 3, 640, 640]
        # img尺寸(1, 3, 640, 640)
        input_feed = self.get_input_feed(img)  # dict:{ input_name: input_value }
        pred = self.onnx_session.run(None, input_feed)[0]  # <class 'numpy.ndarray'>(1, 25200, 9)

        return pred, or_img


# dets:  array [x,6] 6个值分别为x1,y1,x2,y2,score,class
# thresh: 阈值
def nms(dets, thresh):
    # # dets:x1 y1 x2 y2 score class
    # # x[:,n]就是取所有集合的第n个数据
    # x1 = dets[:, 0]
    # y1 = dets[:, 1]
    # x2 = dets[:, 2]
    # y2 = dets[:, 3]
    # # -------------------------------------------------------
    # #   计算框的面积
    # #	置信度从大到小排序
    # # -------------------------------------------------------
    # areas = (y2 - y1 + 1) * (x2 - x1 + 1)
    # scores = dets[:, 4]
    # # print(scores)
    # keep = []
    # index = scores.argsort()[::-1]  # np.argsort()对某维度从小到大排序
    # # [::-1] 从最后一个元素到第一个元素复制一遍。倒序从而从大到小排序
    #
    # while index.size > 0:
    #     i = index[0]
    #     keep.append(i)
    #     # -------------------------------------------------------
    #     #   计算相交面积
    #     #	1.相交
    #     #	2.不相交
    #     # -------------------------------------------------------
    #     x11 = np.maximum(x1[i], x1[index[1:]])
    #     y11 = np.maximum(y1[i], y1[index[1:]])
    #     x22 = np.minimum(x2[i], x2[index[1:]])
    #     y22 = np.minimum(y2[i], y2[index[1:]])
    #
    #     w = np.maximum(0, x22 - x11 + 1)
    #     h = np.maximum(0, y22 - y11 + 1)
    #
    #     overlaps = w * h
    #     # -------------------------------------------------------
    #     #   计算该框与其它框的IOU，去除掉重复的框，即IOU值大的框
    #     #	IOU小于thresh的框保留下来
    #     # -------------------------------------------------------
    #     ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)
    #     idx = np.where(ious <= thresh)[0]
    #     index = index[idx + 1]
    # boxes: a list of [x1, y1, x2, y2] coordinates
    # scores: a list of confidence scores for each box
    # threshold: a scalar value for IoU threshold
    # initialize an empty list for the final boxes
    final_boxes = []
    scores = dets[:, 4]
    # sort the boxes and scores by scores in descending order
    order = np.argsort(scores)[::-1]
    boxes = dets
    # loop until there are no more boxes
    while order.size > 0:
        # pick the box with the highest score
        i = order[0]
        final_boxes.append(i)

        # compute the IoU between the picked box and the rest of the boxes
        xx1 = np.maximum(boxes[i, 0], boxes[order[1:], 0])
        yy1 = np.maximum(boxes[i, 1], boxes[order[1:], 1])
        xx2 = np.minimum(boxes[i, 2], boxes[order[1:], 2])
        yy2 = np.minimum(boxes[i, 3], boxes[order[1:], 3])
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        union = (boxes[i, 2] - boxes[i, 0] + 1) * (boxes[i, 3] - boxes[i, 1] + 1) + \
                (boxes[order[1:], 2] - boxes[order[1:], 0] + 1) * (
                            boxes[order[1:], 3] - boxes[order[1:], 1] + 1) - inter
        iou = inter / union

        # find the indices of the boxes that have IoU less than the threshold
        inds = np.where(iou <= thresh)[0]

        # update the order by keeping only those indices
        order = order[inds + 1]

    # return the final boxes
    return final_boxes


def xywh2xyxy(x):
    # [x, y, w, h] to [x1, y1, x2, y2]
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2
    y[:, 1] = x[:, 1] - x[:, 3] / 2
    y[:, 2] = x[:, 0] + x[:, 2] / 2
    y[:, 3] = x[:, 1] + x[:, 3] / 2
    return y


def filter_box(org_box, conf_thres, iou_thres):  # 过滤掉无用的框
    # -------------------------------------------------------
    #   删除为1的维度
    #	删除置信度小于conf_thres的BOX
    # -------------------------------------------------------
    org_box = np.squeeze(org_box)  # 删除数组形状中单维度条目(shape中为1的维度)
    # (25200, 9)
    # […,4]：代表了取最里边一层的所有第4号元素，…代表了对:,:,:,等所有的的省略。此处生成：25200个第四号元素组成的数组
    conf = org_box[..., 4] > conf_thres  # 0 1 2 3 4 4是置信度，只要置信度 > conf_thres 的
    box = org_box[conf == True]  # 根据objectness score生成(n, 9)，只留下符合要求的框

    # -------------------------------------------------------
    #   通过argmax获取置信度最大的类别
    # -------------------------------------------------------
    cls_cinf = box[..., 5:]  # 左闭右开（5 6 7 8），就只剩下了每个grid cell中各类别的概率
    cls = []
    for i in range(len(cls_cinf)):
        cls.append(int(np.argmax(cls_cinf[i])))  # 剩下的objecctness score比较大的grid cell，分别对应的预测类别列表
    all_cls = list(set(cls))  # 去重，找出图中都有哪些类别
    # set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。
    # -------------------------------------------------------
    #   分别对每个类别进行过滤
    #   1.将第6列元素替换为类别下标
    #	2.xywh2xyxy 坐标转换
    #	3.经过非极大抑制后输出的BOX下标
    #	4.利用下标取出非极大抑制后的BOX
    # -------------------------------------------------------
    output = []
    for i in range(len(all_cls)):
        curr_cls = all_cls[i]
        curr_cls_box = []
        curr_out_box = []

        for j in range(len(cls)):
            if cls[j] == curr_cls:
                box[j][5] = curr_cls
                curr_cls_box.append(box[j][:6])  # 左闭右开，0 1 2 3 4 5

        curr_cls_box = np.array(curr_cls_box)  # 0 1 2 3 4 5 分别是 x y w h score class
        # curr_cls_box_old = np.copy(curr_cls_box)
        curr_cls_box = xywh2xyxy(curr_cls_box)  # 0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class
        curr_out_box = nms(curr_cls_box, iou_thres)  # 获得nms后，剩下的类别在curr_cls_box中的下标
        for k in curr_out_box:
            output.append(curr_cls_box[k])
    output = np.array(output)
    return output


def draw(image, box_data):
    # -------------------------------------------------------
    #	取整，方便画框
    # -------------------------------------------------------

    boxes = box_data[..., :4].astype(np.int32)  # x1 x2 y1 y2
    scores = box_data[..., 4]
    classes = box_data[..., 5].astype(np.int32)
    data = []
    for box, score, cl in zip(boxes, scores, classes):
        top, left, right, bottom = box
        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(CLASSES[cl], score),
                    (top, left),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 2)
        square = (top - bottom) * (right - left)
        tutle = {
            "name": CLASSES[cl],
            "score": score,
            "crop": box,
            "square": square
        }
        data.append(tutle)
    return image, data


def detect(img_path):
    # onnx_path = 'weights/sim_best20221027.onnx'
    model = Yolov5ONNX(r'F:\pythonProject\smart_tree\Reqfile\color.onnx')
    # output, or_img = model.inference('data/images/img.png')
    output, or_img = model.inference(img_path)
    outbox = filter_box(output, 0.5, 0.5)  # 最终剩下的Anchors：0 1 2 3 4 5 分别是 x1 y1 x2 y2 score class
    if len(outbox) == 0:
        print('没有发现物体')
        sys.exit(0)
    or_img, data = draw(or_img, outbox)
    # cv2.imwrite('res.jpg', or_img)
    return data