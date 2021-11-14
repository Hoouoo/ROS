#! /usr/bin/env python
#robot_state.py

import rospy
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from smach import State
from line_detector import Detector
from base_move import BaseMove
from line_tracer import LineTracer

blocking_toggle = False
stop_line_toggle = False
loop = False

#blocking_toggle sub callback
def blocking_bar_flag(msg):
    global blocking_toggle
    if msg.data == 'ON':
        blocking_toggle = True
    if msg.data == 'OFF':
        blocking_toggle = False

#stop_line sub callback
def stop_line_flag(msg):
    global stop_line_toggle
    if msg.data == 'STOP_LINE':
        stop_line_toggle = True
    if msg.data == 'NO_STOP_LINE':
        stop_line_toggle = False

#Move for a second at the start
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

            if self.change_time + 3 < time.time():
                self.twist.linear.x = 0.0
                self.twist.angular.z = 0.0
                self.cmd_vel_pub.publish(self.twist)
                return 'success'

#blocking_toggle sub
blocking_toggle_sub = rospy.Subscriber('blocking_bar', String, blocking_bar_flag)

#blockingbar drive
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
             #rospy.loginfo("blocking bar open")
             return 'success'
          rate.sleep()

#stop_line_toggle sub
sto_line_sub = rospy.Subscriber('stop_line', String, stop_line_flag)

#drive bot
class Autonomous_Drive(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global stop_line_toggle
        self.change_time = time.time()
        # self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        # self.twist = Twist()

    def execute(self, userdata):
        rate = rospy.Rate(20)
        line_tracer = LineTracer()
        while True:
            if loop == True:
                return 'success'
            line_tracer.autonomous_drive(True)
            rospy.loginfo("Autonomous_Drive")
            rate.sleep()
