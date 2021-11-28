#!/usr/bin/env python
# coding=utf-8

import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class DetectObstacle:
    def __init__(self):
        self.scan_sub = rospy.Subscriber('scan', LaserScan, self.scan_callback)
        self.go_sign_pub = rospy.Publisher('obstacle', String, queue_size=1)
        self.go_sign = None

    def scan_callback(self, msg):
        distance = msg.ranges[len(msg.ranges)/2]
        laser_values = list()

        for i in range(200):
            laser_value = msg.ranges[(len(msg.ranges)/2)-160 + i]
            laser_values.append(laser_value)
        obstacle_value = len(list(filter(lambda x: math.isnan(x), laser_values)))

        if obstacle_value > 100:
            print('No')
            self.go_sign = 'NO_OBSTACLE'
            self.go_sign_pub.publish(self.go_sign)
        if obstacle_value <= 100 and distance < 1.7:
            print('Yes')
            self.go_sign = 'DETECT_OBSTACLE'
            self.go_sign_pub.publish(self.go_sign)

if __name__ == "__main__":
    rospy.init_node('obstacle')
    # while not rospy.is_shutdown():
    detector_object = DetectObstacle()
      # rate = rospy.Rate(20)
      # rate.sleep()
    rospy.spin()