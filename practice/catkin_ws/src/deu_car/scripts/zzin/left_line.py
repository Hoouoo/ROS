#!/usr/bin/env python
from functools import reduce
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

global image

class Detector:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    self.image_sub = rospy.Subscriber('/left_camera/rgb/image_raw', 
                                      Image, self.image_callback)
    self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop',
                                       Twist, queue_size=1)
    self.twist = Twist()
    self.time = rospy.Time.now()
    self.cam_loc = left

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
      mask[0:340, 0:w] = 0
      mask[340:440, w - 320: w] = 0
      mask[440:h, 0:w] = 0
    else:
      mask[0:340, 0:w] = 0
      mask[340:440, 0 : 320] = 0
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
      self.center = center_x
      M = cv2.moments(mask)
      if M['m00'] > 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
        # BEGIN CONTROL
        err = cx - w/2
        self.twist.linear.x = 0.2
        self.twist.angular.z = -float(err) / 100
        self.cmd_vel_pub.publish(self.twist)
        # END CONTROL
      
      cv2.circle(mask, (center_x, center_y), 20, (255, 0, 0), -1)
      cv2.imshow('window',mask)
      cv2.waitKey(3)   

      return M

rospy.init_node('detector')
detector = Detector()
rospy.spin()
