#! /usr/bin/env python
import cv2
import numpy
import numpy as np

import cv_bridge
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import Image

##detector stop_line
class Stop_Line():

    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        self.stop_line_toggle = None
        self.stop_line_pub = rospy.Publisher('stop_line', String, queue_size=1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.stop_line_check = list()
        self.area = 0

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_white = numpy.array([0, 0, 200])
        upper_white = numpy.array([0, 0, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)

        h, w = mask.shape
        mask[0: h/2, 0: w] = 0
        mask[0:h, 0:w / 4] = 0
        #mask[0:h, w - (w / 4):w] = 0
        ret, thr = cv2.threshold(mask, 127, 255, 0)

        _,contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            cnt = contours[len(contours) - 1]
            self.area = max(list(map(lambda x: cv2.contourArea(x), contours)))
            rospy.loginfo(self.area)
            if self.area >= 9000:
                self.stop_line_toggle = 'STOP_LINE'
                self.stop_line_pub.publish(self.stop_line_toggle)
            else:
                rospy.loginfo(self.area)
                self.stop_line_toggle = 'NO_STOP_LINE'
                self.stop_line_pub.publish(self.stop_line_toggle)

if __name__ == "__main__":
    rospy.init_node('stop_line')
    # while not rospy.is_shutdown():
    detector_stop_line = Stop_Line()
      # rate = rospy.Rate(20)
      # rate.sleep()
    rospy.spin()