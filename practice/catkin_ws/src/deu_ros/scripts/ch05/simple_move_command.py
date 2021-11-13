#!/usr/bin/env python

import rospy
from actionlib import SimpleActionClient
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseFeedback

def feddback_cb(msg):
  x = msg.base_position.pose.position.x
  y = msg.base_position.pose.position.y
  print 'x : %.2f y :  %.2f' %(x, y)
 
def done_cb(status, result):
  print 'status  : ', status
  print 'result  : ', result, '(NOTIONG)'
  if status == GoalStatus.SUCCEEDED:
    print '>>> move succeeded!'
  elif status == GoalStatus.REJECTED:
    print '>>> move rejected!'
  else:
    print 'find the status GoalStatus.msg'
  
rospy.init_node('move_one_meter')
client = SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "base_footprint"
goal.target_pose.header.stamp = rospy.get_rostime()

goal.target_pose.pose.position.x = 1.0
goal.target_pose.pose.position.y = 0.0
goal.target_pose.pose.orientation.w = 1.0
client.send_goal(goal, done_cb = done_cb, feedback_cb=feddback_cb)

client.wait_for_result()

