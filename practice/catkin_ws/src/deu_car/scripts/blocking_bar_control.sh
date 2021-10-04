#!/usr/bin/env bash

#rosservice call /gazebo/apply_joint_effort '{joint_name: "blocking_bar_joint", effort: 10, start_time: 0, duration: -1 }'
#rosservice call /gazebo/apply_joint_effort '{joint_name: "blocking_bar_joint", effort: 10, start_time: 0, duration: -1 }'
#sleep 1
#rosservice call /gazebo/clear_joint_forces '{joint_name: blocking_bar_joint}'
sleep 10

for i in {1..10};
do
    sleep_time=$(($RANDOM % 10))
    # sleep_time=$(($sleep_time + 3))
    sleep $sleep_time
    echo "Open the blocking bar..."
    rosservice call /gazebo/apply_joint_effort '{joint_name: "blocking_bar_joint", effort: 10, start_time: 0, duration: -1 }'
    rosservice call /gazebo/apply_joint_effort '{joint_name: "blocking_bar_joint", effort: 10, start_time: 0, duration: -1 }'
    sleep 1
    echo "Close the blocking bar..."
    rosservice call /gazebo/clear_joint_forces '{joint_name: blocking_bar_joint}'
    sleep 5
done

