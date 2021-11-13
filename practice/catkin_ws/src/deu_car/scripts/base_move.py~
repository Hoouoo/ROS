#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist


class BaseMove:
  def __init__(self):
    self.twist = Twist()
    self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop',
                                           Twist, queue_size=1)

  def set_angle(self, angle):
    self.twist.angular.z = angle
    rospy.loginfo('set robot angle = %s', self.twist.angular.z)


  def set_velocity(self, velocity):
    self.twist.linear.x = velocity
    rospy.loginfo('set robot velocity = %s', self.twist.linear.x)

      
  def go_forward(self):
    self.cmd_vel_pub.publish(self.twist)


