#! /usr/bin/env python
# coding=utf-8

import cv2
import numpy as np
import rospy
from detector import Detector
from functools import reduce



class LineDetector(Detector):
    def __init__(self, topic_name, camera_loc):
        Detector.__init__(self, topic_name)
        self.camera_loc = camera_loc
        if camera_loc == 'left':
            self.left_interval = 0
            self.right_interval = 320
        if camera_loc == 'right':
            self.left_interval = 320
            self.right_interval = 0
        self.center = 0

    def image_callback(self, msg):
        origin_image = self.image_convert(msg, 'bgr8')
        hsv_image = self.image_convert(msg, 'hsv')

        v = cv2.split(hsv_image)[2]
        binary_img = cv2.inRange(v, 217, 219)
        mask_image = self.image_mask(binary_img, 340, 440, self.left_interval, self.right_interval)

       
        corners = cv2.goodFeaturesToTrack(mask_image, 100, 0.01, 10)
        if corners is not None:
            corners = np.int0(corners)
            point_list = list()
            for i in corners:
                cx, cy = i[0, 0], i[0, 1]
                y_rel_x = {cy: cx}
                point_list.append(y_rel_x)
                point_list.sort()
                # cv2.circle(origin_image, (cx, cy), 3, (0, 0, 255), -1)
                # cv2.circle(binary_img, (cx, cy), 3, (0, 0, 255), -1)
            for i in range(int(len(point_list)/20)):
                del point_list[i]
                point_list.pop()
            '''for i in point_list:
                point = i.items()
                y_point = point[0][0]
                x_point = point[0][1]'''
            x_point = list(map(lambda x: x.items()[0][1], point_list))
            y_point = list(map(lambda x: x.items()[0][0], point_list))
            center_x = reduce(lambda x, y: x + y, x_point)/len(x_point)
            center_y = reduce(lambda x, y: x + y, y_point) / len(y_point)
            self.center = center_x
            cv2.circle(origin_image, (center_x, center_y), 20, (255, 0, 0), -1)
        
        cv2.imshow("window", image)
        cv2.imshow("window2", mask)
        cv2.waitKey(3)
    rospy.init_node('t_line_detector')
    t_line_detector = Linedetector(Detector)
    rospy.spin()

