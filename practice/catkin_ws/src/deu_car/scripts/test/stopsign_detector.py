#!/usr/bin/env python
# coding=utf-8

import rospy
import cv2
from detector import Detector
from std_msgs.msg import String
import os


class StopSignDetector(Detector):
    def __init__(self):
        Detector.__init__(self, 'camera/rgb/image_raw')
        self.matching_value = 0
        self.stop_sign_pub = rospy.Publisher('stop_sign', String, queue_size=1)
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.res_img = cv2.imread(self.abs_path + '/StopSign_Diffuse.png', cv2.IMREAD_GRAYSCALE)
        self.res_img = self.image_mask(self.res_img, 0, 320, 150, 0)
        self.res_img = self.res_img[0:320, 150:465]
        self.stop_sign = None
        self.stop_sign_pub = rospy.Publisher('stop_sign', String, queue_size=1)

    def image_callback(self, msg):
        target_img = self.image_convert(msg, 'gray')

        sift = cv2.xfeatures2d.SIFT_create()

        kp1, des1 = sift.detectAndCompute(target_img, None)
        kp2, des2 = sift.detectAndCompute(self.res_img, None)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        self.matching_value = len(matches)
        if self.matching_value > 100:
            self.stop_sign = 'STOP'
            self.stop_sign_pub.publish(self.stop_sign)
        if self.matching_value < 100:
            self.stop_sign = 'GO'
            self.stop_sign_pub.publish(self.stop_sign)
