#! /usr/bin/env python

import rospy
import numpy
import cv_bridge
import cv2
from sensor_msgs.msg import Image

class Detector:
  def __init__(self, image_topic):
    self.bridge = cv_bridge.CvBridge()
    slef.image_sub = rospy.Subscriber(image_topic, Image, self.image_callback)
    
    
