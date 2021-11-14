#! /usr/bin/env python
# robot_state_machine

import smach_ros
import rospy
from smach import StateMachine
from robot_state import Detect_StartLine, Detect_BlockingBar, Autonomous_Drive

class AutonomousDriving:

    def __init__(self):
        self.driving_machine = StateMachine(outcomes=['success'])
    def autonomos_drive(self):
        rospy.init_node('drive')
        with self.driving_machine:
            StateMachine.add('START', Detect_StartLine(), transitions={'success': 'DRIVELINE'})
            #StateMachine.add('BLOCKINGBAR', Detect_BlockingBar(), transitions={'success': 'DRIVELINE'})
            StateMachine.add('DRIVELINE', Autonomous_Drive(), transitions={'success': 'success'})

        self.driving_machine.execute()
        rospy.spin()

if __name__ == '__main__':
    drive = AutonomousDriving()
    drive.autonomos_drive()
