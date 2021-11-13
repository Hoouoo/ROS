#! /usr/bin/env python

import rospy
import time
from line_detector import LineDetector
from robot_control import RobotBaseMove


class LineTracer:
    def __init__(self):
        self.line_one = LineDetector('my_left_camera/rgb/image_raw', 'left')
        self.line_two = LineDetector('my_right_camera/rgb/image_raw', 'right')
        self.robot_controller = RobotBaseMove()
        self.err = 0

    def start_line_trace(self, flag, angle=0):
        if angle == 0:
            if flag:
                self.err = (self.line_one.center + self.line_two.center)/2 - 320
                angle = -float(self.err)/100
                if abs(angle) < 0.5:
                    self.robot_controller.set_velocity(0.7)
                if abs(angle) >= 0.5:
                    self.robot_controller.set_velocity(0.35)
                self.robot_controller.set_heading(angle)
                self.robot_controller.go_forward()

        if flag == 'CONTROL':
            self.robot_controller.set_velocity(1)
            angle += angle
            self.robot_controller.set_heading(angle)
            self.robot_controller.go_forward()


if __name__ == '__main__':
    rospy.init_node('test')
    test = LineTracer()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        test.start_line_trace(True)
        rate.sleep()
    rospy.spin()
