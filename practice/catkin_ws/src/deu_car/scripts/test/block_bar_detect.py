#! /usr/bin/env python
# coding=utf-8

import rospy
import cv2
from detector import Detector
from std_msgs.msg import String


class BlockDetector(Detector):
    def __init__(self):
        Detector.__init__(self, 'camera/rgb/image_raw')
        self.go_sign = None
        self.go_sign_pub = rospy.Publisher('blocking_bar', String, queue_size=1)

    def image_callback(self, msg):
        mask = self.image_convert(msg, 'hsv')
        s = cv2.split(mask)[1]
        mask = self.image_mask(s, 180, 240, 0, 0)
        mask = cv2.inRange(mask, 254, 255)

        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        if len(contours) != 0:
            self.go_sign = 'STOP'
            self.go_sign_pub.publish(self.go_sign)
        if len(contours) == 0:
            self.go_sign = 'GO'
            self.go_sign_pub.publish(self.go_sign)