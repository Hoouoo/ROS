#! /usr/bin/env python
# coding=utf-8

import rospy
import cv2, cv_bridge
import numpy as np
from base_move import BaseMove
from sensor_msgs.msg import Image
from std_msgs.msg import String

class DetectStopSign:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.stop_sign_pub = rospy.Publisher('stop_sign', String, queue_size=1)
        self.drive_controller = BaseMove()
        self.stop_sign_check = None

    def image_callback(self, msg):

        origin_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(origin_image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 0, 90])
        upper_red = np.array([5, 5, 110])
        gray_img = cv2.inRange(hsv, lower_red, upper_red)

        h, w = gray_img.shape
        block_bar_mask = gray_img
        # block_bar_mask[0:h, 0: w- w/5] = 0
        block_bar_mask[h/2:h, 0:w] = 0
        block_bar_mask[0:h/10, 0:w] = 0
        _, self.contours, _ = cv2.findContours(block_bar_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(self.contours) > 0:
            # print('>>>>>>', cv2.contourArea(self.contours[len(self.contours)-1]))
            if cv2.contourArea(self.contours[len(self.contours)-1]) >= 130:
                self.stop_sign_check = 'STOP_SIGN'
                self.stop_sign_pub.publish(self.stop_sign_check)
            else:
                self.stop_sign_check = 'NO_STOP_SIGN'
                self.stop_sign_pub.publish(self.stop_sign_check)
        # cv2.imshow("66", block_bar_mask)
        # cv2.waitKey(3)

if __name__ == '__main__':
    rospy.init_node('stop_sign')
    detect_stop_sign = DetectStopSign()
    rospy.spin()