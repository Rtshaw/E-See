# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
import tensorflow as tf
import sys

sys.path.append("..")
from utils import label_map_util
from utils import visualization_utils as vis_util


def objectdetection():
    MODEL_NAME = 'inference_graph'
    IMAGE_NAME = './origin/takephoto.png'

    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
    PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)
    NUM_CLASSES = 4
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    image = cv2.imread(PATH_TO_IMAGE)
    image_expanded = np.expand_dims(image, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.8)

    shape = image.shape

    cv2.line(image,(int(shape[1]),0),(int(shape[1]),int(shape[0])),(255,0,150),4)
    cv2.line(image,(int(shape[1]/3),0),(int(shape[1]/3),int(shape[0])),(255,0,150),4)
    cv2.line(image,(int(shape[1]*2/3),0),(int(shape[1]*2/3),int(shape[0])),(255,0,150),4)

    cv2.line(image,(0,int(shape[0])),(shape[1],int(shape[0])),(255,0,150),4)
    cv2.line(image,(0,int(shape[0]/3)),(shape[1],int(shape[0]/3)),(255,0,150),4)
    cv2.line(image,(0,int(shape[0]*2/3)),(shape[1],int(shape[0]*2/3)),(255,0,150),4)

    ## ymin,xmin,ymax,xmax = boxes
    ## classes '1' = spoon '2' = fork '3' = knife '4' = chopsticks
    for i in range(int(classes[0][0])):
        if classes[0][i] == 1 :
            text = "你面前有隻湯匙"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'w') as f:
                f.write('%s，' %text)
        if classes[0][i] == 2 :
            text = "你面前有隻叉子"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'w') as f:
                f.write('%s，' %text)
        if classes[0][i] == 3 :
            text = "你面前有隻刀子"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'w') as f:
                f.write('%s，' %text)
        if classes[0][i] == 4 :
            text = "你面前有雙筷子"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'w') as f:
                f.write('%s，' %text)
    
        y_value = (shape[0]*boxes[0][i][2] + shape[0]*boxes[0][i][0])/2
        x_value = (shape[1]*boxes[0][i][3] + shape[1]*boxes[0][i][1])/2
        
        if x_value <= shape[1]/3:
            text = "他在你的右手邊"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'a+') as f:
                f.write('%s，' %text)
        if shape[1]/3 < x_value < shape[1]*2/3:
            text = "他在你的正中間"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'a+') as f:
                f.write('%s，' %text)
        if x_value >= shape[1]*2/3:
            text = "他在你的左手邊"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'a+') as f:
                f.write('%s，' %text)

        if y_value <= shape[0]/3:
            text = "距離大約三個手掌的距離"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'a+') as f:
                f.write('%s。' %text)
        if shape[0]/3 < y_value < shape[0]*2/3:
            text = "距離大約二個手掌的距離"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'a+') as f:
                f.write('%s。' %text)
        if y_value >= shape[0]*2/3:
            text = "距離大約一個手掌的距離"
            print("[INFO] %s" %text)
            with open('./result/audio/objoutcome.txt', 'a+') as f:
                f.write('%s。' %text)

        
#cv2.imshow('Object detector', image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

