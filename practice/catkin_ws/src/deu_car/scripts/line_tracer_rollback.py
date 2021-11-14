#! /usr/bin/env python

import rospy, cv2
from left_line import Detector
import threading
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from base_move import BaseMove


class LineTracer:
  def __init__(self):
  
    self.robot_controller = BaseMove()
    self.robot_controller.set_velocity(0.9)
    self.robot_controller.go_forward()
    
    self.left_line = Detector('left_camera/rgb/image_raw', 'left')
    self.right_line = Detector('right_camera/rgb/image_raw', 'right')

    
    self.err = 0
    
  def start_line_trace(self, flag, angle=0):
    if angle == 0:
      if flag:
        print ("left = ", self.left_line.center)
        print ("right = ", self.right_line.center)
        print ("devide = ",  (self.left_line.center + self.right_line.center)/2)
        self.err = (self.right_line.center+ self.left_line.center)/2 - 320
        print self.err
        angle = -float(self.err)/100
        if abs(angle) < 0.5:
          self.robot_controller.set_velocity(0.7)
        if abs(angle) >= 0.5:
          self.robot_controller.set_velocity(0.35)
        self.robot_controller.set_angle(angle)
        self.robot_controller.go_forward()
    
    if flag == 'CONTROL':
      self.robot_controller.set_velocity(1)
      angle += angle
      self.robot_controller.set_heading(angle)
      self.robot_controller.go_forward()

 
if __name__ == '__main__':

  rospy.init_node('linetracer')
  linetracer = LineTracer()
  rate = rospy.Rate(20)
  while not rospy.is_shutdown():
    linetracer.start_line_trace(True)
    rate.sleep()
  rospy.spin()
