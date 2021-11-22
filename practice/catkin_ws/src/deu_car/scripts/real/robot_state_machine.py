#! /usr/bin/env python
# robot_state_machine

import smach_ros
import rospy
from smach import StateMachine
from robot_state import Detect_StartLine, Detect_BlockingBar, Autonomous_Drive, go_course2, DoCourse3,T_Parking_1,T_Parking_2,T_Parking_3,DoCourse3_2, DoCourse3_3

class AutonomousDriving:

    def __init__(self):
        self.driving_machine = StateMachine(outcomes=['success'])
    def autonomos_drive(self):
        rospy.init_node('drive')
        with self.driving_machine:
            # StateMachine.add('START', Detect_StartLine(), transitions={'success': 'BLOCKINGBAR'})
            # StateMachine.add('BLOCKINGBAR', Detect_BlockingBar(), transitions={'success': 'DRIVELINE'})
            # StateMachine.add('DRIVELINE', Autonomous_Drive(), transitions={'success': 'success'})
            # StateMachine.add('GO_COURSE2', go_course2(), transitions={'success': 'success'})

            StateMachine.add('DOCOURSE3', DoCourse3(), transitions={'success': 'TPARKING'})
            StateMachine.add('TPARKING', T_Parking_1(), transitions={'success': 'DOCOURSE3_2'})
            # StateMachine.add('TPARKING2', T_Parking_2(), transitions={'success': 'DOCOURSE3_1'})
            # StateMachine.add('TPARKING3', T_Parking_3(), transitions={'success': 'DOCOURSE3_1'})
            # StateMachine.add('DOCOURSE3_1', DoCourse3_2(), transitions={'success': 'DOCOURSE3_2'})
            StateMachine.add('DOCOURSE3_2', DoCourse3_3(), transitions={'success': 'success'})
        self.driving_machine.execute()
        rospy.spin()

if __name__ == '__main__':
    drive = AutonomousDriving()
    drive.autonomos_drive()
