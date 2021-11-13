#! /usr/bin/env python

import smach_ros
from smach import StateMachine
from robot_state import *


if __name__ == '__main__':
    rospy.init_node('drive_test')

    DrivingMachine = StateMachine(outcomes=['success'])
    with DrivingMachine:
        StateMachine.add('BLOCKING_BAR', BlockingBarState(), transitions={'success': 'NORMAL_DRIVE'})
        StateMachine.add('NORMAL_DRIVE', NormalDriveState(), transitions={'success': 'CROSSROAD'},
                         remapping={'input_enter_cnt': 'output_enter_cnt'})
        StateMachine.add('CROSSROAD', CrossRoadState(), transitions={'straight_to_s': 'S_COURSE',
                                                                     'straight_to_t': 'T_COURSE',
                                                                     'turn_left': 'STOP_SIGN'},
                         remapping={'input_enter_cnt': 'output_enter_cnt'})
        StateMachine.add('S_COURSE', SCourseState(), transitions={'success': 'CROSSROAD'})
        StateMachine.add('T_COURSE', TCourseState(), transitions={'success': 'CROSSROAD'})
        StateMachine.add('STOP_SIGN', StopSignState(), transitions={'success': 'OBSTACLE'})
        StateMachine.add('OBSTACLE', ObstacleState(), transitions={'success': 'FINISH'})
        StateMachine.add('FINISH', FinishState(), transitions={'success': 'success'})

    sis = smach_ros.IntrospectionServer('drive_test', DrivingMachine, '/SM_ROOT')
    sis.start()

    DrivingMachine.execute()

    rospy.spin()
    sis.stop()
