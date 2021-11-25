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
from course2 import Course2

from detect_stop_line import Stop_Line
from course4 import RightLineParallelParking
from course5 import RightLineFinal
from course5_1 import LeftLineFinal
from detect_park import DetectParking
from detect_stop_sign import DetectStopSign

blocking_toggle = False
stop_line_toggle = False
stop_sign_toggle = False
obstacle_toggle = False

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

#object sub callback
def obstacle_ch(msg):
    global obstacle_toggle
    if msg.data == 'DETECT_OBSTACLE':
        obstacle_toggle = True
    if msg.data == 'NO_OBSTACLE':
        obstacle_toggle = False

#stop_sign sub callback
def stop_sign_ch(msg):
    global stop_sign_toggle
    if msg.data == 'STOP_SIGN':
        stop_sign_toggle = True
    if msg.data == 'NO_STOP_SIGN':
        stop_sign_toggle = False

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

# stop_line_toggle sub
sto_sign_sub = rospy.Subscriber('stop_sign', String, stop_sign_ch)


# stop_line_toggle sub
obstacle_sub = rospy.Subscriber('obstacle', String, obstacle_ch)


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
        self.flag = 0
        # self.towardCourse2 = TowardCourse2()

    def execute(self, userdata):
        self.change_time = time.time()

        while True:

            if self.flag == 0:

                if self.change_time + 1.0 > time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(-0.14)
                    rospy.loginfo('turn!')
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 1:
                self.move.set_velocity(1.0)
                self.move.set_angle(0.0)
                self.move.go_forward()

                if self.change_time + 4.5< time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(0)
                    self.move.go_forward()
                    return 'success'

class do_course2(State):
    def __init__(self):
        global stop_line_toggle
        State.__init__(self, outcomes=['success'])
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.stop_line_check = 0
        self.check = 0
        self.time = time.time()
        self.state = 0

    def execute(self, userdata):
        #########
        # driving_bot = LineTracer()
        do_course2 = Course2()
        ########
        rate = rospy.Rate(20)

        while True:
            if do_course2.stop_line_cnt == 3 and self.state == 0:
                self.state += 1
                self.time = time.time()
            elif self.state == 1:
                if do_course2.stop_line_cnt == 3:
                    if self.time + 3.0 > time.time():
                            self.twist.linear.x = 0.0
                            self.twist.angular.z =0.0
                            self.cmd_vel_pub.publish(self.twist)
                    else:
                        self.time = time.time()
                        self.state += 1
            elif self.state == 2:
                if self.time + 4.0 > time.time():
                        self.twist.linear.x = 0.9
                        self.twist.angular.z =-0.25
                        self.cmd_vel_pub.publish(self.twist)
                else:
                    self.time = time.time()
                    self.state += 1

            elif self.state == 3:
                do_course2 = Course2()
                do_course2.stop_line_cnt = 2
                self.state += 1
            elif self.state == 4:
                if do_course2.stop_line_cnt == 3:
                    return 'success'
            rate.sleep()

class go_course3(State):
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

                if self.change_time + 1.0 > time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(0.25)
                    rospy.loginfo('turn!')
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 1:
                self.move.set_velocity(0.9)
                self.move.set_angle(0)
                self.move.go_forward()

                if self.change_time + 5.3 < time.time():
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

            if detectRight.state == 1:
                return 'success'
            self.time = rospy.Time.now()
            # print(">>>>>>>>>>>>>>>>>:", detectRight.state)
            rate.sleep()

class DoCourse3_1(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.time = rospy.Time.now()
        self.move = BaseMove()
        self.flag = 0

    def execute(self, userdata):
        detectLeft = DetectLeftLine()
        rate = rospy.Rate(20)
        self.change_time = time.time()

        while True:

            if self.flag == 0:
                self.move.set_velocity(0.0)
                self.move.set_angle(0.4)
                self.move.go_forward()

                if self.change_time + 1.0 < time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(0)
                    self.move.go_forward()
                    self.change_time = time.time()
                    self.flag += 1
            if detectLeft.state == 1:
                return 'success'
            self.time = rospy.Time.now()
            # print(">>>>>>>>>>>>>>>>>:", detectRight.state)
            rate.sleep()

class T_Parking(State):
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

                if self.change_time + 3.0 > time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(-1.06)
                    rospy.loginfo('turn!')
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 2:

                if self.change_time + 4.5 > time.time():
                    self.move.set_velocity(0.9)
                    self.move.set_angle(0.69)
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
                    self.flag += 1

            elif self.flag == 4:

                if self.change_time + 1.9 > time.time():
                    self.move.set_velocity(0.8)
                    self.move.set_angle(-0.6)
                    self.move.go_forward()

                else:
                    self.flag += 1
                    self.change_time = time.time()
                    return 'success'

class go_course4(State):
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

                if self.change_time + 1.7 > time.time():
                    self.move.set_velocity(1.0)
                    self.move.set_angle(-0.03)
                    rospy.loginfo('turn!')
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    self.flag += 1
                    return 'success'


class LastTurn(State):
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
                self.move.set_angle(-0.9)
                self.move.go_forward()

                if self.change_time + 2.0 < time.time():
                    self.move.set_velocity(0)
                    self.move.set_angle(0)
                    self.move.go_forward()
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 1:

                if self.change_time + 2.1 > time.time():
                    self.move.set_velocity(1.0)
                    self.move.set_angle(0)
                    rospy.loginfo('turn!')
                    self.move.go_forward()

                else:
                    self.change_time = time.time()
                    self.flag += 1

            elif self.flag == 2:

                if self.change_time + 2.0> time.time():
                    self.move.set_velocity(1)
                    self.move.set_angle(-0.8)
                    self.move.go_forward()

                else:
                    self.flag += 1
                    self.change_time = time.time()
                    return 'success'

#Obstacle course code
class Obstacle(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global obstacle_toggle
        global stop_sign_toggle
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.change_time = time.time()
        self.check = 0
        self.stop_sign = False
        self.state = 0

    def execute(self, userdata):
        bot = DetectParking('right')
        global driving_bot
        rate = rospy.Rate(20)
        #########################################
        # test code
        driving_bot = LineTracer()
        # stop_sign = DetectStopSign()
        ############################################
        while True:
            if stop_sign_toggle == True and self.state == 0:
                rospy.loginfo('DETECTOR STOP SIGN1')
                self.stop_sign = True
            if self.stop_sign == True:
                if self.state == 0:
                    rospy.loginfo('DETECTOR STOP SIGN2')
                    self.change_time = time.time()
                    self.state += 1
                elif self.state == 1:
                    if self.change_time + 0.6 < time.time():
                        rospy.loginfo('DETECTOR STOP SIGN3')
                        self.change_time = time.time() - 20
                        self.state += 1
                elif self.state == 2:
                    if self.change_time + 10 < time.time():
                        rospy.loginfo('DETECTOR STOP SIGN')
                        rospy.sleep(3)
                        self.stop_sign = False
                        self.change_time = time.time()

            if obstacle_toggle == True:
               rospy.loginfo("obstacle")
               self.twist.linear.x = 0.0
               self.twist.angular.z = 0.0
               self.cmd_vel_pub.publish(self.twist)
            elif self.check == 0 and bot.cnt >= 39:
               self.change_time = time.time()
               self.check = 1
            if self.check == 1 and self.change_time + 0.5 < time.time():
                rospy.loginfo("parking")
                return 'success'
            elif self.check == 1 and self.change_time + 0.5 > time.time():
                self.twist.linear.x = 0.8
                self.twist.angular.z = -0.2
                self.cmd_vel_pub.publish(self.twist)
            else:
               driving_bot.autonomous_drive('STRAIGHT', 0.7)
            rate.sleep()

##ParallelParking code
class ParallelParking(State):
    def __init__(self):
        global stop_line_toggle
        global stop_sign_toggle
        State.__init__(self, outcomes=['success'])
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()
        self.stop_line_check = 0
        self.check = 0
        self.course = 0
        self.checkp = 0
        self.time = rospy.Time.now()

    def execute(self, userdata):
        global driving_bot, leftline_bot
        gogo = None
        rate = rospy.Rate(20)
        self.twist.angular.z = 0.1
        self.cmd_vel_pub.publish(self.twist)
        self.time = rospy.Time.now()
        driving = RightLineParallelParking()
        driving.areaindex = 5000
        driving.time = rospy.Time.now()
        ############test code############
        stop_sign = DetectStopSign()
        ###############################
        # driving.status = 4
        while True:

            if stop_sign_toggle == True:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                return 'success'
            if driving.parking_check == True:
                if driving.status == 0 and self.time + rospy.Duration(3) < rospy.Time.now():
                    rospy.sleep(3)
                    self.time = rospy.Time.now()
                    driving.status = 1
            if driving.status == 1:
                if self.time + rospy.Duration(4) > rospy.Time.now():
                    self.twist.angular.z = 0.85
                    self.twist.linear.x = 0.2
                    self.cmd_vel_pub.publish(self.twist)
                else:
                    self.time = rospy.Time.now()
                    driving.status = 2
            elif driving.status == 2:
                if self.time + rospy.Duration(1) > rospy.Time.now():
                    self.twist.angular.z = -0.9
                    self.twist.linear.x = 1.0
                    self.cmd_vel_pub.publish(self.twist)
                else:
                    self.time = rospy.Time.now()
                    driving.status = 3
            elif driving.status == 3:
                if self.time + rospy.Duration(1) > rospy.Time.now():
                    self.twist.angular.z = 0.0
                    self.twist.linear.x = 0.2
                    self.cmd_vel_pub.publish(self.twist)
                else:
                    driving.status = 4
            elif driving.status == 4:
                driving_bot.autonomous_drive('STRAIGHT', 0.3)
                if stop_line_toggle == True:
                    if self.time + rospy.Duration(5) < rospy.Time.now():
                        rospy.loginfo('DETECTOR STOP LINE')
                        self.stop_line_check = self.stop_line_check + 1
                        if self.check == 1:
                            self.check = 0
                        self.check = 1
                        rospy.sleep(3)
                        self.time = rospy.Time.now()
                if self.stop_line_check == 1:
                    self.time = rospy.Time.now()
                    driving.status = 5
            elif driving.status == 5:
                if self.time + rospy.Duration(2) > rospy.Time.now():
                    self.twist.angular.z = 0.0
                    self.twist.linear.x = 0.5
                    self.cmd_vel_pub.publish(self.twist)
                else:
                    self.time = rospy.Time.now()
                    bot = DetectParking('left')
                    leftline_bot = LeftLineFinal()
                    leftline_bot.state = 0
                    driving.status = 6
            elif driving.status == 6:
                if self.time + rospy.Duration(18) < rospy.Time.now():
                    leftline_bot.state = 1
                    driving.status = 7
            if driving.status == 7:

                bot = RightLineFinal()
                driving.status = 8
            if stop_sign_toggle == True:
                driving.stop_sign_check = True
                return 'success'
            rate.sleep()
