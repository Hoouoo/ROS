#! /usr/bin/env python
# robot_state.py

import rospy
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from smach import State
from line_detector import Detector
from base_move import BaseMove
from line_tracer import LineTracer
from base_move import BaseMove
from detect_right_line import DetectRightLineBumper
from detec_right_to_left import DetectRightToLeft
from detect_left_line import DetectLeftLine

from detect_stop_line import Stop_Line

blocking_toggle = False
stop_line_toggle = False


# blocking_toggle sub callback
def blocking_bar_flag(msg):
    global blocking_toggle
    if msg.data == 'ON':
        blocking_toggle = True
    if msg.data == 'OFF':
        blocking_toggle = False


# stop_line sub callback
def stop_line_flag(msg):
    global stop_line_toggle
    if msg.data == 'STOP_LINE':
        stop_line_toggle = True
    if msg.data == 'NO_STOP_LINE':
        stop_line_toggle = False


# Move for a second at the start
class Detect_StartLine(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()

    def execute(self, userdata):
        while True:
            self.twist.linear.x = 1.0
            self.twist.angular.z = 0.0
            self.cmd_vel_pub.publish(self.twist)

            if self.change_time + 2.5 < time.time():
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.cmd_vel_pub.publish(self.twist)
                return 'success'


# blocking_toggle sub
blocking_toggle_sub = rospy.Subscriber('blocking_bar', String, blocking_bar_flag)


# blockingbar drive
class Detect_BlockingBar(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global blocking_toggle
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()

    def execute(self, userdata):
        rate = rospy.Rate(20)
        while True:
            if blocking_toggle == True:
                # rospy.loginfo("blocking bar open")
                return 'success'
            rate.sleep()


# stop_line_toggle sub
sto_line_sub = rospy.Subscriber('stop_line', String, stop_line_flag)


# drive bot
class Autonomous_Drive(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global stop_line_toggle
        self.change_time = time.time()
        self.time = rospy.Time.now()
        self.flag = 0
        # self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        # self.twist = Twist()

    def execute(self, userdata):
        global line_follower

        line_follower = LineTracer()
        # detect_stop_line = Stop_Line()
        rate = rospy.Rate(20)
        while True:
            if stop_line_toggle == True:
                if self.time + rospy.Duration(5) < rospy.Time.now():
                    rospy.loginfo('===============STOP LINE=============')
                    self.flag = self.flag + 1
                    rospy.sleep(3)
                    self.time = rospy.Time.now()
            if self.flag == 4:  # before 4
                return 'success'

            line_follower.autonomous_drive(True)
            rospy.loginfo("Autonomous_Drive")
            rate.sleep()


# Course 1 clear Course 2 in
class go_course2(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        # self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()
        self.move = BaseMove()
        # self.towardCourse2 = TowardCourse2()

    def execute(self, userdata):
        self.change_time = time.time()

        while True:
            self.move.set_velocity(0.9)
            self.move.set_angle(0)
            self.move.go_forward()

            if self.change_time + 5.0 < time.time():
                self.move.set_velocity(0)
                self.move.set_angle(0)
                self.move.go_forward()
                return 'success'


class DoCourse3(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.time = rospy.Time.now()
        self.flag = 0

    def execute(self, userdata):
        detectRight = DetectRightLineBumper()
        rate = rospy.Rate(20)

        while True:
            # self.flag = detectRight.state
            # if detectRight.state== 1:  # before 4
            #     if self.time + rospy.Duration(5) < rospy.Time.now():
            #         rospy.loginfo('DETECTOR STOP LINE')
            #         # if self.check == 1:
            #         #     self.check = 0
            #         # self.check = 1
            #         rospy.sleep(3)

            if detectRight.state == 1:
                return 'success'
            self.time = rospy.Time.now()
            # print(">>>>>>>>>>>>>>>>>:", detectRight.state)
            rate.sleep()

class DoCourse3_2(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.time = rospy.Time.now()
        self.flag = 0

    def execute(self, userdata):
        detectRight = DetectRightToLeft()
        rate = rospy.Rate(20)

        while True:
            # self.flag = detectRight.state
            # if detectRight.state== 1:  # before 4
            #     if self.time + rospy.Duration(5) < rospy.Time.now():
            #         rospy.loginfo('DETECTOR STOP LINE')
            #         # if self.check == 1:
            #         #     self.check = 0
            #         # self.check = 1
            #         rospy.sleep(3)

            if detectRight.state == 2:
                return 'success'
            self.time = rospy.Time.now()
            # print(">>>>>>>>>>>>>>>>>:", detectRight.state)
            rate.sleep()

class DoCourse3_3(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.time = rospy.Time.now()
        self.flag = 0

    def execute(self, userdata):
        detectLeft = DetectLeftLine()
        rate = rospy.Rate(20)

        while True:
            # self.flag = detectRight.state
            # if detectRight.state== 1:  # before 4
            #     if self.time + rospy.Duration(5) < rospy.Time.now():
            #         rospy.loginfo('DETECTOR STOP LINE')
            #         # if self.check == 1:
            #         #     self.check = 0
            #         # self.check = 1
            #         rospy.sleep(3)

            if detectLeft.state == 1:
                return 'success'
            self.time = rospy.Time.now()
            # print(">>>>>>>>>>>>>>>>>:", detectRight.state)
            rate.sleep()

class T_Parking_1(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        # self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()
        self.move = BaseMove()
        self.flag = 0
        # self.towardCourse2 = TowardCourse2()

    def execute(self, userdata):
        self.change_time = time.time()

        while True:

            if self.flag == 0:
                self.move.set_velocity(1.0)
                self.move.set_angle(0.27)
                self.move.go_forward()

                if self.change_time + 4.5 < time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(0)
                    self.move.go_forward()
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 1:

                if self.change_time + 1.0 > time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(-2.3)
                    rospy.loginfo('turn!')
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 2:

                if self.change_time + 4.5 > time.time():
                    self.move.set_velocity(1)
                    self.move.set_angle(0.35)
                    self.move.go_forward()

                else:
                    self.flag += 1
                    self.change_time = time.time()

            elif self.flag == 3:

                if self.change_time + 1.0 > time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(-1.8)
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    return 'success'


class T_Parking_2(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        # self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()
        self.time = rospy.Time.now()
        self.move = BaseMove()
        self.step = 0

    def execute(self, userdata):
        self.change_time = time.time()

        while True:

            self.move.set_velocity(-1.0)
            self.move.set_angle(-0.8)
            self.move.go_forward()

            if self.change_time + 3.8 < time.time():
                self.move.set_velocity(0)
                self.move.set_angle(0)
                self.move.go_forward()
                self.step = 1

            if self.step == 1:
                if self.time + rospy.Duration(5) < rospy.Time.now():
                    rospy.loginfo('DETECTOR STOP LINE')
                    # if self.check == 1:
                    #     self.check = 0
                    # self.check = 1
                    rospy.sleep(3)
                    self.time = rospy.Time.now()

                else:
                    return 'success'

class T_Parking_3(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        # self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()
        self.move = BaseMove()
        # self.towardCourse2 = TowardCourse2()
        self.step = 0

    def execute(self, userdata):
        self.change_time = time.time()

        while True:

            self.move.set_velocity(1.0)
            self.move.set_angle(0.5)
            self.move.go_forward()

            if self.change_time + 0.7 < time.time():
                self.move.set_velocity(0)
                self.move.set_angle(0)
                self.move.go_forward()

                return 'success'

