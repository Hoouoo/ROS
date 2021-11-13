#! /usr/bin/env python

import rospy
from detect_machine import DetectMachine

if __name__ == '__main__':
    rospy.init_node('detector_stopline')
    blocking_bar_detector = DetectMachine()
    blocking_bar_detector.dm_on_stopline_detector()
