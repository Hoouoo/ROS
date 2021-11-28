#! /usr/bin/env python
# blocking_bar.py

import cv2
import numpy

import cv_bridge
import rospy

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import Image

##detector blocking_bar
class Blocking_Bar():

    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        # cv2.namedWindow("window", 1)
        self.blocking_toggle = None
        self.twist = Twist()
        self.blocking_toggle_pub = rospy.Publisher('blocking_bar', String, queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = numpy.array([0, 0, 90])
        upper_red = numpy.array([5, 5, 110])

        mask = cv2.inRange(hsv, lower_red, upper_red)

        h, w, d = image.shape
        search_top = 2 * h / 7
        search_bot = 3 * h / 7 + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask[0:h, 0:120] = 0
        mask[0:h, 640:w] = 0
        _, bar_check, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(bar_check) > 1:
            self.blocking_toggle = 'OFF'
            self.blocking_toggle_pub.publish(self.blocking_toggle)
            self.twist.linear.x = 0.0
            self.cmd_vel_pub.publish(self.twist)
        else:
            self.blocking_toggle = 'ON'
            self.blocking_toggle_pub.publish(self.blocking_toggle)


if __name__ == "__main__":
    rospy.init_node('blocking_bar')
    # while not rospy.is_shutdown():
    detector_blocking_bar = Blocking_Bar()
      # rate = rospy.Rate(20)
      # rate.sleep()
    rospy.spin()
