#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32

class TopicPublisher:
    def __init__(self):
        rospy.init_node('topic_publisher')
        self.pub = rospy.Publisher('counter', Int32)

    def loop(self):
        rate = rospy.Rate(2)
        count = 0

        while not rospy.is_shutdown():
            self.pub.publish(count)
            count += 1
            rate.sleep()

if __name__== "__main__":
    publisher = TopicPublisher()
    publisher.loop()

