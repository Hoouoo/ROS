#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from base_move import BaseMove

stop_line_toggle = False

#stop_line sub callback
def stop_line_ch(msg):
    global stop_line_toggle
    if msg.data == 'STOP_LINE':
        stop_line_toggle = True
    if msg.data == 'NO_STOP_LINE':
        stop_line_toggle = False
#stop_line_toggle sub
sto_line_sub = rospy.Subscriber('stop_line', String, stop_line_ch)

class RightLineParallelParking:
    def __init__(self):
        self.robot_controller = BaseMove()
        self.bridge = cv_bridge.CvBridge()
        #cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('right_camera/rgb/image_raw', Image, self.image_callback)
        global stop_line_toggle
        self.stop_line_cnt = 0
        self.areaindex = 0
        self.time = rospy.Time.now()
        self.area = 0
        self.lower_color = numpy.array([0, 0, 200])
        self.upper_color = numpy.array([0, 0, 255])
        self.parking = 0
        self.parking_check = False
        self.velocity = 0.4
        self.status = 0
        self.parking_toggle = False

    def image_callback(self, msg):
        if stop_line_toggle == True:
            if self.time + rospy.Duration(5) < rospy.Time.now():
                rospy.loginfo('DETECTOR STOP LINE')
                self.stop_line_cnt += 1
                # if self.check == 1:
                #     self.check = 0
                # self.check = 1
                rospy.sleep(3)
                self.time = rospy.Time.now()
        if self.stop_line_cnt == 1:
            self.velocity = 0.28
        right_yellow_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(right_yellow_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower_color, self.upper_color)

        h, w, d = right_yellow_image.shape
        search_top = 1 * h / 2
        search_bot = 3 * h / 4 + 20

        mask[0:h, 0:w/2] = 0
        mask[0:h/2, 0:w] = 0

        # mask[0:320, 0:w] = 0
        # mask[0:h, 0:480] = 0

        gray = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        edges = cv2.Canny(gray, 40, 120)

        M = cv2.moments(mask)
        _,contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            cnt = contours[len(contours) - 1]
            self.area = max(list(map(lambda x: cv2.contourArea(x), contours)))
            rospy.loginfo(self.area)

            if self.areaindex == 20000:
                if self.area < 20000:
                    if M['m00'] > 0:
                        cx_white = int(M['m10'] / M['m00'])
                        cy_white = int(M['m01'] / M['m00'])

                        # cx = (cx_white + cx_white - 350) // 2
                        # cx = (cx_yellow + cx_white) //2
                        if self.area < 1000:
                            cx = cx_white - 225
                        else:
                            cx = cx_white - 245
                        cy = (cy_white + cy_white) // 2

                        cv2.circle(right_yellow_image, (cx_white, cy_white), 10, (0, 255, 255), -1)


                        err = cx - w / 2
                        self.robot_controller.set_velocity(self.velocity)
                        self.robot_controller.set_angle(-float(err) / 100)
                        self.robot_controller.go_forward()
                else:
                    self.robot_controller.set_velocity(self.velocity)
                    self.robot_controller.set_angle(-0.1)
                    self.robot_controller.go_forward()

            if self.areaindex == 4:
               if M['m00'] > 0:
                   cx_white = int(M['m10'] / M['m00'])
                   cy_white = int(M['m01'] / M['m00'])

                   # cx = (cx_white + cx_white - 350) // 2
                   # cx = (cx_yellow + cx_white) //2

                   cx = cx_white - 320
                   cy = (cy_white + cy_white) // 2

                   cv2.circle(right_yellow_image, (cx_white, cy_white), 10, (0, 255, 255), -1)

                   err = cx - w / 2
                   self.robot_controller.set_velocity(0.9)
                   self.robot_controller.set_angle(-float(err) / 300)
                   self.robot_controller.go_forward()

            if self.areaindex == 5000:
                _, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                print('edges',len(contours))
                if M['m00'] > 0:
                    cx_white = int(M['m10'] / M['m00'])
                    cy_white = int(M['m01'] / M['m00'])

                    # cx = (cx_white + cx_white - 350) // 2
                    # cx = (cx_yellow + cx_white) //2
                    if self.area < 1000:
                        cx = cx_white - 225
                    else:
                        cx = cx_white - 245
                    cy = (cy_white + cy_white) // 2

                    cv2.circle(right_yellow_image, (cx_white, cy_white), 10, (0, 255, 255), -1)

                    err = cx - w / 2
                if self.parking_toggle == False and self.time + rospy.Duration(9) < rospy.Time.now():
                    self.parking_toggle = True
                elif self.parking_toggle == True:
                    # if self.area >= 30000 and self.parking >= 1:
                    #     rospy.loginfo('soon parking')
                    #     self.lower_color = numpy.array([0, 0, 200])
                    #     self.upper_color = numpy.array([0, 0, 255])
                    #     self.robot_controller.set_angle(0.5)
                    #     self.robot_controller.go_forward()
                    if self.parking >= 1:
                        ## parking gogo
                        if self.parking_check == False and self.time + rospy.Duration(1) < rospy.Time.now():
                            #print(self.time)
                            self.parking_check = True
                        elif self.parking_check == True:
                            self.image_sub.unregister()

                    if self.area < 5000 or self.area > 10000:
                        self.robot_controller.set_velocity(self.velocity)
                        self.robot_controller.set_angle(-float(err) / 100)
                        self.robot_controller.go_forward()
                    else:
                        self.parking+=1
                        if self.parking == 1:
                            rospy.loginfo('pakring start')
                            #################################
                            self.time = rospy.Time.now()
                            ################################
                            self.robot_controller.set_angle(-0.8)
                            #####
                            self.robot_controller.set_velocity(0.5)
                            self.robot_controller.go_forward()
                            self.lower_color = numpy.array([25, 52, 72])
                            self.upper_color = numpy.array([102, 255, 255])
                        elif self.parking > 1:
                            ####
                            self.robot_controller.set_velocity(0.5)
                            self.robot_controller.set_angle(-float(err) / 300)
                            self.robot_controller.go_forward()
                else:
                    self.robot_controller.set_velocity(self.velocity)
                    self.robot_controller.set_angle(-float(err) / 100)
                    self.robot_controller.go_forward()

            print('parkrkrkrkr', self.parking)
            # END CONTROL
        else:
             self.robot_controller.set_angle(-0.8)
             self.robot_controller.set_velocity(0.5)

             self.robot_controller.go_forward()
        #cv2.imshow("window", right_yellow_image)
        #cv2.waitKey(3)
