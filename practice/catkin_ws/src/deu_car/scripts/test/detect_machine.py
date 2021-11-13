#! /usr/bin/env python
# coding=utf-8

import rospy
from block_bar_detect import BlockDetector
from obstacle_checker import ObstacleChecker
from stopline_detector import StopLineDetector
from stopsign_detector import StopSignDetector


class DetectMachine:

    def __init__(self):
        self._dict = {}
        self.blocking_bar_detector = None
        self.obstacle_checker_detector = None
        self.stopline_detector = None
        self.stopsign_detector = None

    def dm_on_blocking_bar(self):
        rospy.loginfo('on blocking_bar detector')
        self.blocking_bar_detector = BlockDetector()
        rospy.spin()

    def dm_on_obstacle_checker(self):
        rospy.loginfo('on obstacle_checker')
        self.obstacle_checker_detector = ObstacleChecker()
        rospy.spin()

    def dm_on_stopline_detector(self):
        rospy.loginfo('on stop_line detector')
        self.stopline_detector = StopLineDetector()
        rospy.spin()

    def dm_on_stopsign_detector(self):
        rospy.loginfo('on stop_sign detector')
        self.stopline_detector = StopSignDetector()
        rospy.spin()
