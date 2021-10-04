#!/usr/bin/env python
# BEGIN ALL
import cv2
import numpy
import cv_bridge
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image



##-------------------------Stop Line-----------------------------------------------##

class StopLine:  #Detect Stopline
    def __init__(self):  # creator Detector
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.stopline_image_pub = rospy.Publisher('camera/rgb/image_raw/stopline', Image, queue_size=1)#detect stopline
        self.twist = Twist()
        self.stopable = 0
        self.linecount = 0       #stopline count

    def get_linecount(self):
        return self.linecount

    def image_callback(self, msg):
        stoplineimage = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(stoplineimage, cv2.COLOR_BGR2HSV)
        lower_white = numpy.array([0, 0, 225])
        upper_white = numpy.array([10, 10, 235])
        stoplinemask = cv2.inRange(hsv, lower_white, upper_white)  # color_into_white_color
        h, w, d = stoplineimage.shape
        search_top = 5 * h / 6 + 10
        search_bot = 5 * h / 6 + 30
        stoplinemask[0:search_top, 0:w] = 0
        stoplinemask[search_bot:h, 0:w] = 0
        stoplinemask[0:h,0:w/2] = 0
        stoplinemask[0:h,(w/2+20):w] = 0
        M2 = cv2.moments(stoplinemask) # stopline mask
        if M2['m00'] > 0 :   #fisrt detect
            if self.stopable == 0:                          # 0: True, 1:False
                if self.linecount==2 or self.linecount==3 or self.linecount==5 or self.linecount==8:
                    cx = int(M2['m10'] / M2['m00'])
                    cy = int(M2['m01'] / M2['m00'])
                    cv2.circle(stoplineimage, (cx, cy), 10, (255, 0, 0), -1)
                    self.stopable = 1
                    self.linecount += 1
                else : #1,4......
                    cx = int(M2['m10'] / M2['m00'])
                    cy = int(M2['m01'] / M2['m00'])
                    cv2.circle(stoplineimage, (cx, cy), 10, (255, 0, 0), -1)
                    # BGR = White
                    # BEGIN CONTROL
                    # Wait  3 Seconds
                    self.twist.linear.x = 0.0
                    rospy.sleep(3.0)
                    # END CONTROL
                    self.stopable=1
                    self.linecount += 1
            else : #next detect stopable=1
                cx = int(M2['m10'] / M2['m00'])
                cy = int(M2['m01'] / M2['m00'])
                cv2.circle(stoplineimage, (cx, cy), 10, (255, 0, 0), -1)
                self.twist.linear.x = 0.8
        else :  #No detect
            self.stopable = 0
            self.twist.linear.x = 0.8
        self.cmd_vel_pub.publish(self.twist)
        stoplineimage_msg = self.bridge.cv2_to_imgmsg(stoplineimage, 'bgr8')
        self.stopline_image_pub.publish(stoplineimage_msg) #publish
        rospy.loginfo('stopable = %d',self.stopable)
        rospy.loginfo('linecount = %d', self.linecount)


##-------------------------STop Bar-----------------------------------------------##
class Detector_Bar:
    def __init__(self):  # creator Detector_Bar
        self.bridge = cv_bridge.CvBridge()
        # cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.bar_pub = rospy.Publisher('camera/rgb/image_raw/p2_bar', Image, queue_size=1)  # detect blockbar
        self.twist = Twist()
        self.linecount=0

    def image_callback(self, msg):
        barimage = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(barimage, cv2.COLOR_BGR2HSV)
        lower_red = numpy.array([0, 30, 30])
        upper_red = numpy.array([10, 255, 130])
        mask = cv2.inRange(hsv, lower_red, upper_red)  # color_into_red_color
        h, w, d = barimage.shape
        search_top = 1
        search_bot = 3 * h / 4
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask[0:h, 0:250] = 0

        M = cv2.moments(mask)
        self.twist.linear.x = 0.8
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(barimage, (cx, cy), 10, (255, 0, 0), -1)
            # BGR = RED
            # BEGIN CONTROL
            self.twist.linear.x = 0.0
            # END CONTROL
            rospy.loginfo('detecting bar...')
        self.cmd_vel_pub.publish(self.twist)
        bar_image_msg = self.bridge.cv2_to_imgmsg(barimage, 'bgr8')
        self.bar_pub.publish(bar_image_msg)  # publish



#----------------------RedSign------------------------------------------
class Detector_Redsign:
    def __init__(self):  # creator Detector_Bar
        self.bridge = cv_bridge.CvBridge()
        #cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.redsign_pub = rospy.Publisher('camera/rgb/image_raw/redsign', Image, queue_size=1)#detect blockbar
        self.twist = Twist()
        global reddetectcount
        reddetectcount = True
        self.redcount = True


    def image_callback(self, msg):
        redsignimage = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(redsignimage, cv2.COLOR_BGR2HSV)
        lower_red = numpy.array([-1, 195, 90])
        upper_red = numpy.array([1, 205, 100])
        mask = cv2.inRange(hsv, lower_red, upper_red)  # color_into_red_color
        h, w, d = redsignimage.shape

        search_top = 1
        search_bot = 5*h/6
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask[0:h, 0:w-40] = 0
        M3 = cv2.moments(mask)
        if M3['m00'] > 0:
            if self.redcount == True:
                cx = int(M3['m10'] / M3['m00'])
                cy = int(M3['m01'] / M3['m00'])
                cv2.circle(redsignimage, (cx, cy), 10, (255, 0, 0), -1)
                # BGR = RED
                # BEGIN CONTROL
                self.twist.linear.x = 0.0
                rospy.sleep(3.0)
                self.redcount=False

                # END CONTROL
            else :
                cx = int(M3['m10'] / M3['m00'])
                cy = int(M3['m01'] / M3['m00'])
                cv2.circle(redsignimage, (cx, cy), 10, (255, 0, 0), -1)
                # BGR = RED
                # BEGIN CONTROL
                # END CONTROL
        else:
            self.redcount = True

        self.cmd_vel_pub.publish(self.twist)
        redsignimage_msg = self.bridge.cv2_to_imgmsg(redsignimage, 'bgr8')
        self.redsign_pub.publish(redsignimage_msg) #publish


#----------------------------------------------------------------------good right yellow

class Right_Yellow_Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        #cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('right_camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()

    def image_callback(self, msg):

        right_yellow_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(right_yellow_image, cv2.COLOR_BGR2HSV)

        lower_yellow = numpy.array([20, 80, 80])
        upper_yellow = numpy.array([60, 255, 255])

        lower_white = numpy.array([0, 0, 190])
        upper_white = numpy.array([255, 40, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = right_yellow_image.shape
        search_top = 1 * h / 2
        search_bot = 3 * h / 4 + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask_yellow[0:search_top, 0:w/2] = 0
        mask_yellow[search_bot:h, 0:w/2] = 0
        mask_yellow[search_top:search_bot - 1, 0:50] = 0

        M = cv2.moments(mask)
        M_w = cv2.moments(mask_white)
        M_y = cv2.moments(mask_yellow)

        if M['m00'] > 0:
            cx_yellow = int(M_y['m10'] / M_y['m00'])
            cy_yellow = int(M_y['m01'] / M_y['m00'])
            cx_white = int(M_w['m10'] / M_w['m00'])
            cy_white = int(M_w['m01'] / M_w['m00'])

            cx = (cx_yellow + cx_yellow - 350) // 2
            # cx = (cx_yellow + cx_white) //2
            cy = (cy_yellow + cy_yellow) // 2

            cv2.circle(right_yellow_image, (cx_yellow, cy_yellow), 10, (0, 255, 255), -1)
            #      cv2.circle(image, (cx_white, cy_white), 20, (255,255,255), -1)
            #      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # BEGIN CONTROL
            err = cx - w / 2
            self.twist.linear.x = StopLine.robotspeed
            self.twist.angular.z = -float(err) / 30
            self.cmd_vel_pub.publish(self.twist)
            # END CONTROL
        cv2.imshow("window", right_yellow_image)
        cv2.waitKey(3)
#-------------------------------------------------------------------------------------------good left yellow

class Left_Yellow_Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        #    cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('left_camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()

    def image_callback(self, msg):
        #stopline = StopLine()
        #if stopline.get_linecount() >= 1 and  stopline.get_linecount() < 4:
        left_yellow_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(left_yellow_image, cv2.COLOR_BGR2HSV)

        lower_yellow = numpy.array([20, 80, 80])
        upper_yellow = numpy.array([60, 255, 255])

        lower_white = numpy.array([0, 0, 190])
        upper_white = numpy.array([255, 40, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = left_yellow_image.shape
        search_top = 1 * h / 2
        search_bot = 4 * h / 5
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask_yellow[0:search_top, w/2:w] = 0
        mask_yellow[search_bot:h, w/2:w] = 0
        mask_yellow[search_top:search_bot - 1, w-50:w] = 0

        M = cv2.moments(mask)
        M_w = cv2.moments(mask_white)
        M_y = cv2.moments(mask_yellow)

        if M['m00'] > 0:
            cx_yellow = int(M_y['m10'] / M_y['m00'])
            cy_yellow = int(M_y['m01'] / M_y['m00'])
            cx_white = int(M_w['m10'] / M_w['m00'])
            cy_white = int(M_w['m01'] / M_w['m00'])

            cx = (cx_yellow + cx_yellow + 350) // 2
            # cx = (cx_yellow + cx_white) //2
            cy = (cy_yellow + cy_yellow) // 2

            cv2.circle(left_yellow_image, (cx_yellow, cy_yellow), 10, (0, 255, 255), -1)
            #      cv2.circle(image, (cx_white, cy_white), 20, (255,255,255), -1)
            #      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # BEGIN CONTROL
            err = cx - w / 2
            self.twist.linear.x = 0.8
            self.twist.angular.z = -float(err) / 30
            self.cmd_vel_pub.publish(self.twist)
            # END CONTROL
        cv2.imshow("window", left_yellow_image)
        cv2.waitKey(3)

#----------------------------------------------------------------------------------------------

class Right_White_Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        # cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('right_camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()

    def image_callback(self, msg):
        #stopline = StopLine()
        #if stopline.get_linecount() >= 4 and stopline.get_linecount() < 5:
        right_white_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(right_white_image, cv2.COLOR_BGR2HSV)

        lower_yellow = numpy.array([20, 80, 80])
        upper_yellow = numpy.array([60, 255, 255])

        lower_white = numpy.array([0, 0, 190])
        upper_white = numpy.array([255, 40, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = right_white_image.shape
        search_top = 1 * h / 2
        search_bot = 3 * h / 4 + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask_white[0:search_top, 0:w / 2] = 0
        mask_white[search_bot:h, 0:w / 2] = 0
        mask_white[search_top:search_bot - 1, 0:50] = 0

        M = cv2.moments(mask)
        M_w = cv2.moments(mask_white)
        M_y = cv2.moments(mask_yellow)

        if M['m00'] > 0:
            cx_yellow = int(M_y['m10'] / M_y['m00'])
            cy_yellow = int(M_y['m01'] / M_y['m00'])
            cx_white = int(M_w['m10'] / M_w['m00'])
            cy_white = int(M_w['m01'] / M_w['m00'])

            cx = (cx_white+ cx_white - 350) // 2
            # cx = (cx_yellow + cx_white) //2
            cy = (cy_white + cy_white) // 2

            cv2.circle(right_white_image, (cx_white, cy_white), 10, (0, 255, 255), -1)
            #      cv2.circle(image, (cx_white, cy_white), 20, (255,255,255), -1)
            #      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # BEGIN CONTROL
            err = cx - w / 2
            self.twist.linear.x = StopLine.robotspeed
            self.twist.angular.z = -float(err) / 30
            self.cmd_vel_pub.publish(self.twist)
            # END CONTROL
        cv2.imshow("window", right_white_image)
        cv2.waitKey(3)

class Left_White_Follower:
    def __init__(self):
        self.bridge = cv_bridge.CvBridge()
        # cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('right_camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.twist = Twist()

    def image_callback(self, msg):
        #stopline = StopLine()
        #if stopline.get_linecount() >= 4 and stopline.get_linecount() < 5:
        right_white_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(right_white_image, cv2.COLOR_BGR2HSV)

        lower_yellow = numpy.array([20, 80, 80])
        upper_yellow = numpy.array([60, 255, 255])

        lower_white = numpy.array([0, 0, 190])
        upper_white = numpy.array([255, 40, 255])

        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(hsv, lower_white, upper_white)

        h, w, d = right_white_image.shape
        search_top = 1 * h / 2
        search_bot = 3 * h / 4 + 20
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask_white[0:search_top, 0:w / 2] = 0
        mask_white[search_bot:h, 0:w / 2] = 0
        mask_white[search_top:search_bot - 1, 0:50] = 0

        M = cv2.moments(mask)
        M_w = cv2.moments(mask_white)
        M_y = cv2.moments(mask_yellow)

        if M['m00'] > 0:
            cx_yellow = int(M_y['m10'] / M_y['m00'])
            cy_yellow = int(M_y['m01'] / M_y['m00'])
            cx_white = int(M_w['m10'] / M_w['m00'])
            cy_white = int(M_w['m01'] / M_w['m00'])

            cx = (cx_white+ cx_white - 350) // 2
            # cx = (cx_yellow + cx_white) //2
            cy = (cy_white + cy_white) // 2

            cv2.circle(right_white_image, (cx_white, cy_white), 10, (0, 255, 255), -1)
            #      cv2.circle(image, (cx_white, cy_white), 20, (255,255,255), -1)
            #      cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
            # BEGIN CONTROL
            err = cx - w / 2
            self.twist.linear.x = StopLine.robotspeed
            self.twist.angular.z = -float(err) / 30
            self.cmd_vel_pub.publish(self.twist)
            # END CONTROL
        cv2.imshow("window", right_white_image)
        cv2.waitKey(3)

def main():
    rospy.init_node('driving_bot')
    driving_bot = StopLine()
    #stoplinecount = driving_bot.get_linecount()
    driving_bot = Detector_Bar()
    #driving_bot = Left_Yellow_Follower()
    #driving_bot = Right_White_Follower()

    rospy.spin()
    #driving_bot = Detector_Redsign()
    #driving_bot = Right_Yellow_Follower()
    #driving_bot = Yellow_White_Follower()
    #driving_bot = Detector_Redsign()
    #driving_bot = Right_White_Follower()

if __name__ == "__main__":
    main()

