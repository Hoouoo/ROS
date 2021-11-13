#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist


class RobotBaseMove:
    def __init__(self):
        self.twist = Twist()
        self.twist.linear.x = 0.3
        #rospy.loginfo('initialize twist.angular.z = %s', self.twist.angular.z)
        #rospy.loginfo('initialize twist linear.x = %s', self.twist.linear.x)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop',
                                           Twist, queue_size=1)

    def set_heading(self, angle):
        self.twist.angular.z = angle
        #rospy.loginfo('set robot heading = %s', self.twist.angular.z)

    def set_velocity(self, velocity):
        self.twist.linear.x = velocity
        #rospy.loginfo('set velocity = %s', self.twist.linear.x)

    def up_velocity(self, increase):
        if self.twist.linear.x + increase <= 1:
            self.twist.linear.x += increase

    def down_velocity(self, increase):
        if self.twist.linear.x - increase > 0:
            self.twist.linear.x -= increase

    def go_forward(self):
        self.cmd_vel_pub.publish(self.twist)
        #rospy.loginfo('publish x: %s', self.twist.linear.x)
        #rospy.loginfo('publish z: %s', self.twist.angular.z)
