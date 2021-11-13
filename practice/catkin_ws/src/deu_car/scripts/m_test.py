#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
import cv2 as cv
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    cv2.namedWindow("window", 1)
    self.image_sub = rospy.Subscriber('camera/rgb/image_raw', 
                                      Image, self.image_callback)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop',
                                       Twist, queue_size=1)             
    self.twist = Twist()
    self.time = rospy.Time.now()
  def image_callback(self, msg):
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #lower_yellow = numpy.array([10, 10, 10])
    lower_gray = numpy.array([0, 0, 0])
    #upper_yellow = numpy.array([255, 255, 250])
    upper_gray = numpy.array([255, 10, 250])
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([40,255,255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    h, w, d = image.shape
    print h, w, d
    search_top = 3*h/4
    search_bot = 3*h/4 + 20
    mask[0:search_top, 0:w] = 0
    mask[search_bot:h, 0:w] = 0
    mask[0:h, 0:120] = 0
    M = cv2.moments(mask)
    #########################################
    lower_red = numpy.array([0, 0, 90])
    upper_red = numpy.array([5, 5, 110])
    rmask = cv2.inRange(hsv, lower_red, upper_red)
    h, w, d = image.shape
    search_top = 3*h/7
    search_bot = 3*h/7 + 20
    rmask[0:search_top, 0:w] = 0
    rmask[search_bot:h, 0:w] = 0
    rmask[0:h, 0:120] = 0
    rmask[0:h, 640:w] = 0
    _, c, _ = cv2.findContours(rmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #########################################
    #########################################
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 255, 255])
    wmask = cv2.inRange(hsv, lower_white, upper_white)
    h, w, d = image.shape
    
    wmask[0:360, 0:w] = 0
    wmask[380:h, 0:w] = 0
    wmask[0:h, 0:w/3] = 0
    wmask[0:h, w/3+30:w] = 0
    _, qq, _ = cv2.findContours(wmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("bar", wmask)
    print len(c)
    #########################################
    if len(c) < 5:
        if M['m00'] > 0:
            cx = int(M['m10']/M['m00']) -170
            cy = int(M['m01']/M['m00'])
            cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # BEGIN CONTROL
            err = cx - w/2
            self.twist.linear.x = 1.0
            if len(qq) == 1 and self.time + rospy.Duration(5) < rospy.Time.now():
                rospy.sleep(3)
                self.time = rospy.Time.now()
              
            self.twist.linear.x = 1.0
            self.twist.angular.z = -float(err) / 100
            self.cmd_vel_pub.publish(self.twist)
            # END CONTROL
    cv2.imshow("window", image)
    cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
