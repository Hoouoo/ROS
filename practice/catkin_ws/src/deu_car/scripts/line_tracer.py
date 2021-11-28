#! /usr/bin/env python

import rospy, cv2
from line_detector import Detector
import threading
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from base_move import BaseMove
from line_tracer2_straight import StraightDetector
import time
from nav_msgs.msg import Odometry

class LineTracer:
    def __init__(self):

        self.robot_controller = BaseMove()
        self.left_line = Detector('left_camera/rgb/image_raw', 'left')
        self.right_line = Detector('right_camera/rgb/image_raw', 'right')
        # self.left_line2 = StraightDetector('left_camera/rgb/image_raw', 'left')
        # self.right_line2 = StraightDetector('right_camera/rgb/image_raw', 'right')

        self.err = 0

    def autonomous_drive(self, flag, velocity = 5.7, angle=0):
        if angle == 0:
            if flag:
                print("left = ", self.left_line.center)
                print("right = ", self.right_line.center)
                print("<< l_ len(line) = ", self.left_line.contour)
                print(">> r_ len(line) = ", self.right_line.contour)
                print("devide = ", (self.left_line.center + self.right_line.center) / 2)
                if self.left_line.center == 0 and self.right_line.contour == 0:
                    self.robot_controller.set_velocity(0.3)
                    #  if abs(angle) >= 0.5:
                    # self.robot_controller.set_velocity(0.35)
                    self.robot_controller.go_forward()
                elif self.left_line.contour - self.right_line.contour > 30:
                    self.robot_controller.set_velocity(velocity) # Lane 1 0.57
                    # self.err = (self.right_line.center)/2 - 320
                    self.robot_controller.set_angle(-float(70) / 100)
                    self.robot_controller.go_forward()

                elif self.right_line.contour - self.left_line.contour > 30  :
                    self.robot_controller.set_velocity(velocity) # Lane 1 0.57
                    # self.err = (self.right_line.center)/2 - 320
                    self.robot_controller.set_angle(float(70) / 100)
                    self.robot_controller.go_forward()
                 # self.robot_controller.set_velocity(0.2)
                 # self.robot_controller.set_angle(float(80) / 100)
                 # self.robot_controller.go_forward()
                else:
                    self.err = (self.right_line.center + self.left_line.center) / 2 - 305
                    print self.err
                    angle = -float(self.err) / 100
                    print 'angle = ', angle
                    if abs(angle) < 0.4:
                        self.robot_controller.set_velocity(0.5) # Lane 1 0.5
                    if abs(angle) >= 0.4:
                        self.robot_controller.set_velocity(0.2)
                    self.robot_controller.set_angle(angle)
                    self.robot_controller.go_forward()
        ############obstacle course and final course
        if flag == 'STRAIGHT2':
            if self.left_line.center == 0 and self.right_line.center == 0:
                self.robot_controller.set_velocity(0.1)
                self.robot_controller.go_forward()
            elif self.right_line.center >= 600:
                self.robot_controller.set_velocity(0.2)
                self.robot_controller.set_angle(-float(80) / 100)
                self.robot_controller.go_forward()
            elif self.left_line.center > 110 and self.left_line.center < 160 and self.right_line.center > 100:

                self.robot_controller.set_velocity(velocity)
                self.robot_controller.set_angle(0.0)
                self.robot_controller.go_forward()
            else:
                self.err = (self.left_line.center + self.left_line.center) / 2 - 300
                # self.err = (self.right_line.center + self.left_line.center) / 2 - 295
                angle = -float(self.err) / 100
                # print 'angle = ', angle
                if abs(angle) < 0.4:
                    self.robot_controller.set_velocity(velocity)
                if abs(angle) >= 0.4:
                    self.robot_controller.set_velocity(0.2)
                self.robot_controller.set_angle(angle)
                self.robot_controller.go_forward()

        if flag == 'CONTROL':
            self.robot_controller.set_velocity(1)

            self.robot_controller.set_angle(self.err)
            self.robot_controller.go_forward()


class StartLine:
    def __init__(self):
        self.stoptoggle = True
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()
        # rospy.Time.now()+ rospy.Duration(3)
        print(self.change_time)

    def start_line(self):
        while True:
            self.twist.linear.x = 1.0
            self.cmd_vel_pub.publish(self.twist)

            if self.change_time + 3.0 < time.time():
                self.twist.linear.x = 0.0
                self.cmd_vel_pub.publish(self.twist)
                self.stoptoggle = False
                return False


if __name__ == '__main__':

    rospy.init_node('linetracer')
    start = StartLine()
    start.start_line()
    linetracer = LineTracer()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        linetracer.autonomous_drive(True)
        rate.sleep()
    rospy.spin()