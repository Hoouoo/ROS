#! /usr/bin/env python
# coding=utf-8

import rospy
import cv2
from detector import Detector
from std_msgs.msg import String


class StopLineDetector(Detector):
    def __init__(self):
        Detector.__init__(self, 'camera/rgb/image_raw')
        self.sample_img = None
        self.go_sign = False
        self.go_sign_pub = rospy.Publisher('stop_line', String, queue_size=1)

    def image_callback(self, msg):
        target_image = self.image_convert(msg, 'gray')
        target_image = self.image_mask(target_image, 350, 420, 180, 180)
        target_image = cv2.inRange(target_image, 215, 221)
        contours = cv2.findContours(target_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        area = 0

        if len(contours) > 0:
            area = cv2.contourArea(contours.pop())
        # 정지선이 인식되면 STOP 발행
        if area != 0 and area > 9500:
            self.go_sign = 'STOP'
            self.go_sign_pub.publish(self.go_sign)
        if area == 0 and area <= 9500:
            self.go_sign = 'GO'
            self.go_sign_pub.publish(self.go_sign)