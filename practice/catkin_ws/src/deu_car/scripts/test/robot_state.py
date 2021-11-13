#! /usr/bin/env python
# coding=utf-8

import rospy
import time
from std_msgs.msg import String
from smach import State
from lane_follower import LineTracer


lane_tracer = LineTracer()
stop_sign = False
stop_sign_panel = False
stop_sign_obs = False


def obstacle_sign_cb(msg):
    global stop_sign_obs
    if msg.data == 'STOP':
        stop_sign_obs = True
    if msg.data == 'GO':
        stop_sign_obs = False


def stop_sign_cb(msg):
    global stop_sign_panel
    if msg.data == 'STOP':
        stop_sign_panel = True
    if msg.data == 'GO':
        stop_sign_panel = False


def stop_line_cb(msg):
    global stop_sign
    if msg.data == 'STOP':
        stop_sign = True
    if msg.data == 'GO':
        stop_sign = False


stop_line_sub = rospy.Subscriber('stop_line', String, stop_line_cb)
stop_sign_sub = rospy.Subscriber('stop_sign', String, stop_sign_cb)
obstacle_sign_sub = rospy.Subscriber('obstacle', String, obstacle_sign_cb)


# 주행시험장 시작시의 상태
class BlockingBarState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        self.blocking_bar_sub = rospy.Subscriber('blocking_bar', String, self.block_bar_cb)
        self.stop_sign = False

    def block_bar_cb(self, msg):
        if msg.data == 'GO':
            self.stop_sign = True
        if msg.data == 'STOP':
            self.stop_sign = False

    def execute(self, ud):
        rospy.loginfo("블로킹 바 감지 상태")
        rate = rospy.Rate(20)
        while True:
            if self.stop_sign:
                rospy.loginfo("출발합니다...")
                return 'success'
            if not self.stop_sign:
                rospy.loginfo("정지중...")
            rate.sleep()


# 일반적인 도로 중앙으로 라인 트레이싱 하는 경우의 상태
class NormalDriveState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'],
                       output_keys=['output_enter_cnt'])
        global stop_sign
        self.stop_line_cnt = 0

    def execute(self, ud):
        global lane_tracer
        rospy.loginfo("일반 주행 상태")
        rate = rospy.Rate(20)
        ud.output_enter_cnt = 'normal_drive'
        while True:
            if self.stop_line_cnt == 4:
                return 'success'
            if stop_sign:
                rospy.loginfo("정지선 발견")
                self.stop_line_cnt += 1
                stop_time = time.time()
                current_time = time.time()
                while current_time - stop_time < 3:
                    current_time = time.time()
            lane_tracer.start_line_trace(True)
            rate.sleep()


# 사거리 진입시의 상태
class CrossRoadState(State):
    def __init__(self):
        State.__init__(self, outcomes=['straight_to_s', 'straight_to_t', 'turn_left'],
                       input_keys=['input_enter_cnt'], output_keys=['output_enter_cnt'])

    def execute(self, ud):
        global lane_tracer, stop_sign
        rate = rospy.Rate(20)
        rospy.loginfo("사거리 진입")
        if ud.input_enter_cnt == 'normal_drive':
            rospy.loginfo("직진합니다")
            start_time = time.time()
            current_time = time.time()
            while current_time - start_time < 4:
                current_time = time.time()
                lane_tracer.start_line_trace('CONTROL', 0.05)
            start_time = time.time()
            while True:
                current_time = time.time()
                if current_time - start_time > 10:
                    return 'straight_to_s'
                lane_tracer.start_line_trace(True)
                rate.sleep()

        if ud.input_enter_cnt == 's_course_clear':
            rospy.loginfo("사거리 진입")
            start_time = time.time()
            current_time = time.time()
            while current_time - start_time < 4:
                current_time = time.time()
                lane_tracer.start_line_trace('CUSTOM', 0)

            while True:
                if stop_sign:
                    start_time = time.time()
                    current_time = time.time()
                    while current_time - start_time < 3:
                        current_time = time.time()
                    break
                lane_tracer.start_line_trace(True)
                rate.sleep()
            start_time = time.time()
            current_time = time.time()
            while current_time - start_time < 4:
                current_time = time.time()
                lane_tracer.start_line_trace('CONTROL', -0.16)
            return 'straight_to_t'
        if ud.input_enter_cnt == 't_course_clear':
            rospy.loginfo("좌회전 합니다")
            start_time = time.time()
            current_time = time.time()
            while current_time - start_time < 3:
                current_time = time.time()
            return 'turn_left'


# 사거리 이후 S코스 진입 및 주행 상태
class SCourseState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'],
                       output_keys=['output_enter_cnt'])

    def execute(self, ud):
        ud.output_enter_cnt = 's_course_clear'
        global stop_sign
        global lane_tracer
        rospy.loginfo("S코스 인식")
        rospy.loginfo("S코스 진입")
        int(rospy.Time.now().to_sec())
        start_time1 = time.time()
        current_time1 = time.time()
        while current_time1 - start_time1 < 6:
            current_time1 = time.time()
            lane_tracer.start_line_trace('CONTROL', -0.22)

        rospy.loginfo("S코스 주행")
        '''start_time2 = time.time()
        current_time2 = time.time()
        while current_time2 - start_time2 < 25:
            current_time2 = time.time()
            lane_tracer.start_line_trace(True)
        '''
        while not stop_sign:
            lane_tracer.start_line_trace(True)
        rospy.loginfo("코스 탈출")
        return 'success'


# 사거리 이후 T코스 진입 및 주행 상태
class TCourseState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'],
                       output_keys=['output_enter_cnt'])
        self.stop_flag = False

    def execute(self, ud):
        global stop_sign
        ud.output_enter_cnt = 't_course_clear'
        rospy.loginfo('T코스 구간 진입')
        while True:
            if stop_sign:
                break
            lane_tracer.start_line_trace(True)
        rospy.loginfo('T구간 탈출')
        return 'success'


# 정지 표지판 인식 및 정지 상태
class StopSignState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global lane_tracer

    def execute(self, ud):
        rospy.loginfo("정지 표지판 구간 진입")
        global stop_sign_panel
        while True:
            if stop_sign_panel:
                break
            lane_tracer.start_line_trace(True)
        start_time = time.time()
        current_time = time.time()
        while current_time - start_time < 5:
            current_time = time.time()
        rospy.loginfo("정지 이후 출발")
        return 'success'


# 임시 장애물 회피구간
class ObstacleState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global lane_tracer

    def execute(self, ud):
        global stop_sign_obs
        while not stop_sign_obs:
            lane_tracer.start_line_trace(True)
        rospy.loginfo('장애물 구간 통과')
        return 'success'


# 전체 시험 종료후 정지 상태
class FinishState(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
        global lane_tracer

    def execute(self, ud):
        rospy.loginfo("최종 구간 돌입")
        while True:
            lane_tracer.start_line_trace(True)
        rospy.loginfo("급격한 90도 커브")
        time.sleep(1)
        return 'success'