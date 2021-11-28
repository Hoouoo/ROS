#!/usr/bin/env python
# BEGIN ALL
from functools import reduce
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from base_move import BaseMove
import time

stop_line_toggle = False


def stop_line_ch(msg):
    global stop_line_toggle
    if msg.data == 'STOP_LINE':
        stop_line_toggle = True
    if msg.data == 'NO_STOP_LINE':
        stop_line_toggle = False


# stop_line_toggle sub
sto2_line_sub = rospy.Subscriber('stop_line', String, stop_line_ch)


class LeftLineFinal:
    def __init__(self):
        global stop_line_toggle
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('left_camera/rgb/image_raw',
                                          Image, self.image_callback)
        self.robot_controller = BaseMove()
        self.time = rospy.Time.now()

        self.state = 0
        self.state_after = 1

        self.center = 0
        self.err = 0
        self.area = 0

        self.change_time = time.time()

    def image_callback(self, msg):
        global angle

        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v = cv2.split(hsv)[2]  # GRAY
        lower_yellow = numpy.array([20, 80, 80])
        upper_yellow = numpy.array([45, 255, 255])

        mask = cv2.inRange(v, 217, 250)
        mask_bumper = cv2.inRange(hsv, lower_yellow, upper_yellow)

        h, w, d = image.shape
        mask[0:259, 0:w] = 0
        # mask[250:440, : w] = 0
        # mask[320:440, w/3: w] = 0
        mask[440:h, 0:w] = 0

        # mask[w/2:w][0:h] = 0
        # # mask[0:h/2][0:w] = 0
        # # mask[0:h][w/2:w] = 0

        corners = cv2.goodFeaturesToTrack(mask, 100, 0.01, 10)
        if corners is not None:
            corners = numpy.int0(corners)
            point_list = list()
            for i in corners:
                t_cx, t_cy = i[0, 0], i[0, 1]
                y_rel_x = {t_cy: t_cx}
                point_list.append(y_rel_x)
                point_list.sort()
                # cv2.circle(origin_image, (cx, cy), 3, (0, 0, 255), -1)
                # cv2.circle(binary_img, (cx, cy), 3, (0, 0, 255), -1)
            for i in range(int(len(point_list) / 20)):
                del point_list[i]
                point_list.pop()
            '''for i in point_list:
            point = i.items()
            y_point = point[0][0]
            x_point = point[0][1]'''
            x_point = list(map(lambda x: x.items()[0][1], point_list))
            y_point = list(map(lambda x: x.items()[0][0], point_list))
            center_x = reduce(lambda x, y: x + y, x_point) / len(x_point)
            center_y = reduce(lambda x, y: x + y, y_point) / len(y_point)
            self.center = center_x
            cv2.circle(image, (center_x, center_y), 20, (255, 0, 0), -1)

            # rospy.loginfo(self.center)

            self.err = (center_x) / 2 + 10
            print(self.err)
            angle = -float(self.err) / 100
            print('angle = ', angle)

        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print('edges', len(contours))

        if stop_line_toggle == True:
            if self.time + rospy.Duration(5) < rospy.Time.now():
                rospy.loginfo('DETECTOR STOP LINE')
                self.state += 1
                rospy.sleep(3)
                self.time = rospy.Time.now()
            else:
                if len(contours) > 0:
                    self.robot_controller.set_angle(angle)
                    self.robot_controller.set_velocity(0.4)
                    self.robot_controller.go_forward()
                else:
                    self.robot_controller.set_angle(0.2)
                    self.robot_controller.set_velocity(0.4)
                    self.robot_controller.go_forward()

        else:
            if len(contours) > 0:
                self.robot_controller.set_angle(angle)
                self.robot_controller.set_velocity(0.4)
                self.robot_controller.go_forward()
            else:
                self.robot_controller.set_angle(0.4)
                self.robot_controller.set_velocity(0.4)
                self.robot_controller.go_forward()

        if self.state == 1:
            self.image_sub.unregister()

        rospy.loginfo(angle)

        # END CONTROL
        # cv2.imshow("window", mask)
        # #cv2.imshow('right', image)
        # # # # cv2.imshow("window_m", image)
        # cv2.waitKey(3)

# if __name__ == '__main__':
#
#     rospy.init_node('righttracer')
#     start = DetectRight()
#     rate = rospy.Rate(20)
#     while not rospy.is_shutdown():
#         rate.sleep()
#     rospy.spin()
