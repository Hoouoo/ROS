#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist


class Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        #    cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('left_camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()

    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_yellow = numpy.array([20, 80, 80])
        upper_yellow = numpy.array([45, 255, 255])

        lower_white = numpy.array([0, 0, 190])
        upper_white = numpy.array([255, 40, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = image.shape
        search_top = 2 * h / 3
        search_bot = 3 * h / 4 + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask_yellow[0:search_top, 0:w] = 0
        mask_yellow[search_bot:h, 0:w * 2 / 3] = 0
        mask_yellow[search_top:search_bot - 1, 0:w * 2 / 3] = 0

        M = cv2.moments(mask)
        M_w = cv2.moments(mask_white)
        M_y = cv2.moments(mask_yellow)

        if M['m00'] > 0:
            cx_yellow = int(M_y['m10'] / M_y['m00'])
            cy_yellow = int(M_y['m01'] / M_y['m00'])
            cx_white = int(M_w['m10'] / M_w['m00'])
            cy_white = int(M_w['m01'] / M_w['m00'])

            cx = (cx_yellow + cx_yellow - 400) // 2
            # cx = (cx_yellow + cx_white) //2
            cy = (cy_yellow + cy_white) // 2

            cv2.circle(image, (cx_yellow, cy_yellow), 20, (0, 255, 255), -1)
            #      cv2.circle(image, (cx_white, cy_white), 20, (255,255,255), -1)
            #      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # BEGIN CONTROL
            err = cx - w / 2
            self.twist.linear.x = 0.9
            self.twist.angular.z = -float(err) / 100
            self.cmd_vel_pub.publish(self.twist)
            # END CONTROL
        cv2.imshow("window", image)
        cv2.waitKey(3)


rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL
