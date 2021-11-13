#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from detector import Detector

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
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_gray = numpy.array([0, 0, 0])
    upper_gray = numpy.array([255, 10, 250])
    #mask = cv2.inRange(hsv, lower_gray, upper_gray)
    v = cv2.split(hsv)[2] # RED
    mask = cv2.inRange(v, 215, 219)
    l_mask = cv2.inRange(v, 215, 219)
    r_mask = cv2.inRange(v, 215, 219)

    # BEGIN CROP
    h, w, d = image.shape
    search_top = 3*h/4
    search_bot = search_top + 20
    mask[0:340, 0:w] = 0
    mask[h-60:h, 0:w] = 0
    mask[0:h, 0:180] = 0
    mask[0:h, 450:w] = 0
    
    l_test_right = 320
    l_test_left = 0
    
    r_test_left = 320
    r_test_right = 0
    
    test_top = 340
    test_bot = 440
    
    l_mask[0:340, 0:w] = 0
    l_mask[340:440, 0:l_test_left] = 0
    l_mask[340:440, w-l_test_right:w] = 0
    l_mask[440:h, 0:w] = 0
    
    r_mask[0:340, 0:w] = 0
    r_mask[340:440, 0:r_test_left] = 0
    r_mask[340:440, w-r_test_right:w] = 0
    r_mask[440:h, 0:w] = 0
    
    corners = cv2.goodFeaturesToTrack(l_mask, 100, 0.01, 10)
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
      cv2.circle(l_mask, (center_x, center_y), 20, (255, 0, 0), -1)
      cv2.circle(image, (center_x, center_y), 20, (255, 0, 0), -1)
      
      
    corners2 = cv2.goodFeaturesToTrack(r_mask, 100, 0.01, 10)
    if corners2 is not None:
      corners2 = numpy.int0(corners2)
      point_list2 = list()
      for i in corners2:
        t_cx2, t_cy2 = i[0,0], i[0,1]
        y_rel_x2 = {t_cy2: t_cx2}
        point_list2.append(y_rel_x2)
        point_list2.sort()
        # cv2.circle(origin_image, (cx, cy), 3, (0, 0, 255), -1)
        # cv2.circle(binary_img, (cx, cy), 3, (0, 0, 255), -1)
      for i in range(int(len(point_list2)/20)):
        del point_list2[i]
        point_list2.pop()
      '''for i in point_list:
         point = i.items()
         y_point = point[0][0]
         x_point = point[0][1]'''
      x_point2 = list(map(lambda x: x.items()[0][1], point_list2))
      y_point2 = list(map(lambda x: x.items()[0][0], point_list2))
      center_x2 = reduce(lambda x, y: x + y, x_point2)/len(x_point2)
      center_y2 = reduce(lambda x, y: x + y, y_point2) / len(y_point2)
      self.center = center_x2
      cv2.circle(r_mask, (center_x2, center_y2), 20, (255, 0, 0), -1)
      cv2.circle(image, (center_x2, center_y2), 20, (255, 0, 0), -1)
      
      
    
    # END CROP
    
    #################### Stop Bar ###############################
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
    #################### Stop Line ###############################
    
    #################### Stop Line ###############################
    lower_white = numpy.array([0, 0, 200])
    upper_white = numpy.array([180, 255, 255])
    wmask = cv2.inRange(hsv, lower_white, upper_white)
    h, w, d = image.shape
    
    wmask[0:360, 0:w] = 0
    wmask[380:h, 0:w] = 0
    wmask[0:h, 0:w/3] = 0
    wmask[0:h, w/3+30:w] = 0
    _, qq, _ = cv2.findContours(wmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print len(qq)
    ################################################################
    
    # BEGIN FINDER
    M = cv2.moments(mask)
    if M['m00'] > 0 and len(c) < 5:
    
      # BEGIN STOP LINE
      if len(qq) == 1 and self.time + rospy.Duration(5) < rospy.Time.now():
        rospy.sleep(3)
        self.time = rospy.Time.now()
        #self.twist.linear.x = 1.0
        self.cmd_vel_pub.publish(self.twist)
        # END CONTROL 
      
      else:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # END FINDER
        # BEGIN CIRCLE
        #cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
        err = cx - w/2
        #self.twist.linear.x = 1.0
        #self.twist.angular.z = -float(err) / 100
        self.cmd_vel_pub.publish(self.twist)
      
    # END CIRCLE

    cv2.imshow("window", image)
    cv2.imshow("window2", l_mask)
    cv2.imshow("windows3", r_mask)
    cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
