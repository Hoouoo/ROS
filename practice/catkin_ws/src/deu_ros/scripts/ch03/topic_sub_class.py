#!/usr/bin/env python

import rospy
from std_msgs.msg import Int32


class TopicSubscriber:
    def __init__(self):
        rospy.init_node('topic_subscriber')
        self.sub = rospy.Subscriber('counter', Int32, self.__callback)
        rospy.spin()

    def __callback(self, msg):
        print 'msg type = ', type(msg)
        print 'data = ', msg.data


if __name__ == "__main__":
    subscriber = TopicSubscriber()
