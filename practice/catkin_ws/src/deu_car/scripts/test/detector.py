#! /usr/bin/env python

import rospy
import cv_bridge
import numpy as np
import cv2
from sensor_msgs.msg import Image


class Detector:
    def __init__(self, image_topic):
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber(image_topic, Image, self.image_callback)

    def image_convert(self, image, cvt_type):
        if cvt_type == 'bgr8':
            converted_img = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
            return converted_img
        if cvt_type == 'hsv':
            converted_img = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
            converted_img = cv2.cvtColor(converted_img, cv2.COLOR_BGR2HSV)
            return converted_img
        if cvt_type == 'gray':
            converted_img = self.bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')
            converted_img = cv2.cvtColor(converted_img, cv2.COLOR_BGR2GRAY)
            return converted_img

    def image_mask(self, res_image, search_top, search_bot, left_inetval, right_interval):
        h, w = res_image.shape
        image = np.copy(res_image)
        image[0:search_top, 0:w] = 0
        image[search_top:search_bot, 0:left_inetval] = 0
        image[search_top:search_bot, w - right_interval:w] = 0
        image[search_bot:h, 0:w] = 0
        return image

    def image_callback(self, msg):
        raise NotImplementedError
