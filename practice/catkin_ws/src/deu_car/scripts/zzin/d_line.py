#!/usr/bin/env python
from functools import reduce
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

global image

class StartLine:
  def __init__(self):
    self.stoptoggle = True
    self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
    self.twist = Twist()
    self.change_time = time.time()
    #rospy.Time.now()+ rospy.Duration(3)
    print(self.change_time)
  


  def start_line(self):
    while True:
      self.twist.linear.x = 1.0
      self.cmd_vel_pub.publish(self.twist)

      if self.change_time + 1.7 < time.time():
        self.twist.linear.x = 0.0
        self.cmd_vel_pub.publish(self.twist)
        self.stoptoggle = False
        return False

class Detector:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop',
                                       Twist, queue_size=1)
    self.twist = Twist()
    
    
    self.image_sub = rospy.Subscriber('right_camera/rgb/image_raw', 
                                      Image, self.image_callback)
    
    self.time = rospy.Time.now()
    self.cam_loc = 'right'

  def image_callback(self, msg):
    global center_x2, center_x
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    v = cv2.split(hsv)[2] # RED
    mask = cv2.inRange(v, 217, 219)
#    l_mask = cv2.inRange(v, 217, 219)
#    r_mask = cv2.inRange(v, 217, 219)
    # BEGIN CROP
    h, w, d = image.shape

#    search_top = 3*h/4
#    search_bot = search_top + 20
    
    if self.cam_loc == 'left':
#      mask[0:h, w/5:w] = 0
      mask[0:150, 0:w] = 0
      mask[150:440, w/2: w] = 0
      mask[440:h, 0:w] = 0
    elif self.cam_loc == 'right':
      mask[0:150, 0:w] = 0
      mask[150:440, 0: w/2] = 0
      mask[440:h, 0:w] = 0
      
    corners = cv2.goodFeaturesToTrack(mask, 100, 0.01, 10)
    if corners is not None:
      corners = numpy.int0(corners)
      point_list = list()
      for i in corners:
        t_cx, t_cy = i[0,0], i[0,1]
        y_rel_x = {t_cy: t_cx}
        point_list.append(y_rel_x)
        point_list.sort()
        # cv2.circle(origin_image, (cx, cy), 3, (0, 0, 255), -1)
        # cv2.circle(binary_img, (cx, cy), 3, (0, 0, 255), -1)
      for i in range(int(len(point_list)/20)):
        del point_list[i]
        point_list.pop()
      '''for i in point_list:
         point = i.items()
         y_point = point[0][0]
         x_point = point[0][1]'''
      x_point = list(map(lambda x: x.items()[0][1], point_list))
      y_point = list(map(lambda x: x.items()[0][0], point_list))
      center_x = reduce(lambda x, y: x + y, x_point)/len(x_point)
      center_y = reduce(lambda x, y: x + y, y_point) / len(y_point)
    M = cv2.moments(mask)
    cv2.circle(mask, (center_x, center_y), 20, (255, 0, 0), -1)    
    if M['m00'] > 0:
      self.err = ( center_x ) /2 - 310
      
#        self.err = ( center_x ) - 150
      print(self.err)
      self.twist.linear.x = 0.9
      self.twist.angular.z = -float(self.err) / 100
      self.cmd_vel_pub.publish(self.twist)
       # END FORWARD
    cv2.imshow('window',mask)
    cv2.waitKey(3)   
    
if __name__ == '__main__':
  rospy.init_node('detector')
  start = StartLine()
  start.start_line()
 
  detector = Detector()
  rospy.spin()
  rate = rospy.Rate(20)
  while not rospy.is_shutdown():
    rate.sleep()
