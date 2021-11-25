#! /usr/bin/env python
# robot_state_machine

import smach_ros
import rospy
from smach import StateMachine
from robot_state import Detect_StartLine, Detect_BlockingBar, Autonomous_Drive, go_course2, DoCourse3, T_Parking, DoCourse3_1,LastTurn,do_course2,go_course3,go_course4, Obstacle, ParallelParking

class AutonomousDriving:

    def __init__(self):
        self.driving_machine = StateMachine(outcomes=['success'])
    def autonomos_drive(self):
        rospy.init_node('drive')
        with self.driving_machine:
            StateMachine.add('START', Detect_StartLine(), transitions={'success': 'BLOCKINGBAR'})
            StateMachine.add('BLOCKINGBAR', Detect_BlockingBar(), transitions={'success': 'DRIVELINE'})
            StateMachine.add('DRIVELINE', Autonomous_Drive(), transitions={'success': 'GO_COURSE2'})
            StateMachine.add('GO_COURSE2', go_course2(), transitions={'success': 'DO_COURSE2'})
            StateMachine.add('DO_COURSE2', do_course2(), transitions={'success': 'GO_COURSE3'})
            StateMachine.add('GO_COURSE3', go_course3(), transitions={'success': 'DO_COURSE3'})
            StateMachine.add('DO_COURSE3', DoCourse3(), transitions={'success': 'TPARKING'})
            StateMachine.add('TPARKING', T_Parking(), transitions={'success': 'DO_COURSE3_1'})
            StateMachine.add('DO_COURSE3_1', DoCourse3_1(), transitions={'success': 'GO_COURSE4'})
            StateMachine.add('GO_COURSE4', go_course4(), transitions={'success': 'DRIVELINE2'})
            StateMachine.add('DRIVELINE2', Autonomous_Drive(), transitions={'success': 'OBSTACLE'})
            StateMachine.add('OBSTACLE', Obstacle(), transitions={'success': 'PARALLELPARKING'})
            StateMachine.add('PARALLELPARKING', ParallelParking(), transitions={'success': 'success'})

            # StateMachine.add('TPARKING2', T_Parking_2(), transitions={'success': 'DOCOURSE3_1'})
            # StateMachine.add('TPARKING3', T_Parking_3(), transitions={'success': 'DOCOURSE3_1'})
            # StateMachine.add('DOCOURSE3_1', DoCourse3_2(), transitions={'success': 'DOCOURSE3_2'})
            # StateMachine.add('DOCOURSE3_2', DoCourse3_1(), transitions={'success': 'success'})
            # StateMachine.add('LastTurn', LastTurn(), transitions={'success': 'success'})
        self.driving_machine.execute()
        rospy.spin()

if __name__ == '__main__':
    drive = AutonomousDriving()
    drive.autonomos_drive()
