#!/usr/bin/env python
# coding=utf-8

import rospy
import math
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class ObstacleChecker:
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
            self.go_sign = 'GO'
            self.go_sign_pub.publish(self.go_sign)
        if obstacle_value <= 100 and distance < 1.7:
            self.go_sign = 'STOP'
            self.go_sign_pub.publish(self.go_sign)
