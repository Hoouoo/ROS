#!/usr/bin/env bash

echo "setting GAZEBO_RESOURCE_PATH to $(pwd)/world"
export GAZEBO_RESOURCE_PATH=$(pwd)/world:$(pwd)/world/models:$GAZEBO_RESOURCE_PATH
echo "setting GAZEBO_PLUGIN_PATH to $(pwd)/build"
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:$(pwd)/build
echo "setting GAZEBO_MODEL_PATH to $(pwd)/world/models"
export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:$(pwd)/world/models

