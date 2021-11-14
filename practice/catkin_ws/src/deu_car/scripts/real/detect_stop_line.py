#! /usr/bin/env python
# coding=utf-8

import rospy
import cv2, cv_bridge
from std_msgs.msg import String
from sensor_msgs.msg import Image

class StopLineDetector(Detector):
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('camera / rgb / image_raw', Image, self.image_callback)

        self.flag = False
        self.go_pub = rospy.Publisher('stop_line', String, queue_size=1)

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        mask = cv2.inRange(image, 215, 221)

        h, w = image.shape

        mask[0:350, 0:w] = 0
        mask[350:420, 0:180] = 0
        mask[350:420, w - 180:w] = 0
        mask[420:h, 0:w] = 0

        contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        area = 0

        if len(contours) > 0:
            area = cv2.contourArea(contours.pop())
        if area != 0 and area > 9500:
            self.flag = 'STOP'
            self.go_pub.publish(self.flag)
        if area == 0 and area <= 9500:
            self.flag = 'GO'
            self.go_pub.publish(self.go_sign)