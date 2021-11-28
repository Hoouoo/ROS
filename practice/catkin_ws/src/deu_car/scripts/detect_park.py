#!/usr/bin/env python
# BEGIN ALL
import numpy as np

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from base_move import BaseMove

stop_line_toggle = False

#stop_line sub callback
def stop_line_ch(msg):
    global stop_line_toggle
    if msg.data == 'STOP_LINE':
        stop_line_toggle = True
    if msg.data == 'NO_STOP_LINE':
        stop_line_toggle = False
#stop_line_toggle sub
sto_line_sub = rospy.Subscriber('stop_line', String, stop_line_ch)

class DetectParking:
    def __init__(self, camera):
        self.robot_controller = BaseMove()
        self.bridge = cv_bridge.CvBridge()
        #cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber(camera+'_camera/rgb/image_raw', Image, self.image_callback)

        global stop_line_toggle
        self.stop_line_cnt = 0
        self.time = rospy.Time.now()
        self.cnt = 0
    def image_callback(self, msg):
        right_yellow_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(right_yellow_image, cv2.COLOR_BGR2HSV)

        lower_white = numpy.array([0, 0, 200])
        upper_white = numpy.array([0, 0, 255])

        mask = cv2.inRange(hsv, lower_white, upper_white)
        gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(gray, 40, 120)

        h, w, d = right_yellow_image.shape
        search_top = 1 * h / 2
        search_bot = 3 * h / 4 + 20

        # cv2.imshow('edges', edges)
        M = cv2.moments(mask)
        _,contours,_ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.cnt = len(contours)
        if self.cnt >= 40:
            self.image_sub.unregister()
        # cv2.waitKey(3)

