#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
가제보에서 상자를 좌우로 움직이게 하는 ROS 토픽 발생 방법 사례.

실행 방법:

$ roslaunch gazebo_ros empty_world.launch
$ rosrun deu_ros obstacle_spawn.py

"""

import rospy
from gazebo_msgs.msg import ModelState, LinkState
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Quaternion
import tf.transformations as transform
import sys
import os


class BoxHandler:
    MODEL_FILE = sys.argv[1] + "my_box/model.sdf"
    INIT_POSE = (9.5, -3.0, 0.15)
    XMAX_BOX = 2.5

    def __init__(self):
        rospy.init_node('gazebo_box_handler')
        rospy.wait_for_service("gazebo/spawn_sdf_model")
        self.spawn_model = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
        self.delete_model = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
        self.model_pub = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size=1)
        self.link_pub = rospy.Publisher('/gazebo/set_link_state', LinkState, queue_size=1)
        self.position = list(BoxHandler.INIT_POSE)  # x, y, z
        self.orientation = [.0, .0, .0]  # r, p, s
        self.sign = 1
        self.MODEL_NAME = 'my_box'

    def do_spawn_model(self):
        self.delete_model(self.MODEL_NAME)  # delete the previous spawned object
        try:
            with open(BoxHandler.MODEL_FILE) as f:
                model_xml = f.read()
        except IOError:  # useless actually because of lines 81-85
            rospy.logerr('%s not found. export GAZEBO_MODEL_PATH=models_dir_path', BoxHandler.MODEL_FILE)
            sys.exit(-1)

        model_pose = Pose()
        model_pose.position.x = self.position[0]
        model_pose.position.y = self.position[1]
        model_pose.position.z = self.position[2]
        model_pose.orientation = Quaternion(*transform.quaternion_from_euler(0, 0, 0))  # roll, pitch, yaw
        self.spawn_model(self.MODEL_NAME, model_xml, "", model_pose, "world")

    def update_model(self):
        x, y, z = self.position
        x += (self.sign * 0.05)

        msg = ModelState()
        msg.model_name = self.MODEL_NAME  # 'unit_box'
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        msg.reference_frame = 'world'
        self.model_pub.publish(msg)
        self.position[0] = x
        self.position[1] = y
        self.position[2] = z
        if x < BoxHandler.INIT_POSE[0]  or x > BoxHandler.INIT_POSE[0] + BoxHandler.XMAX_BOX:
            self.sign = self.sign * (-1)

    def update_link(self):
        """ not working currently """
        msg = LinkState()
        msg.link_name = "cart_front_steer::wheel_front_left_spin"
        msg.reference_frame = "world"
        # msg.twist.linear.x = 0.2
        msg.twist.angular.z = 0.05
        self.link_pub.publish(msg)
        msg.link_name = "cart_front_steer::wheel_front_right_spin"
        self.link_pub.publish(msg)

    def loop(self):
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            # self.update_link()
            self.update_model()
            r.sleep()


if __name__ == "__main__":

    rospy.loginfo("The following shell command should be run: export ROBOT_INITIAL_POSE='-Y 1.57'")

    try:
        print('GAZEBO_MODEL_PATH = %s' % os.environ['GAZEBO_MODEL_PATH'])
    except KeyError as err:
        print('Cannot find the environment variable %s' % err)
        sys.exit(-1)

    handler = BoxHandler()
    handler.do_spawn_model()
    handler.loop()
