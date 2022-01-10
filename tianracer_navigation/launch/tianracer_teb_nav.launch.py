# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This launches nav2 using TEB as controller

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
# from rclpy.node import Node
from launch_ros.actions import Node


def generate_launch_description():
    # Get the launch directory
    teb_launch_dir = os.path.join(
        get_package_share_directory('tianracer_navigation'), 'param')
    nav2_bringup_launch_dir = os.path.join(
        get_package_share_directory('nav2_bringup'), 'launch')

    map_yaml_file = LaunchConfiguration('map', default=os.path.join(
            get_package_share_directory('tianracer_slam'), 'maps', 'test_ros_map.yaml'))
    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value=map_yaml_file,
        description='Full path to map yaml file to load')

    params_file = os.path.join(teb_launch_dir, 'tianracer_teb.yaml')

    bringup_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_bringup_launch_dir, 'bringup_launch.py')),
        launch_arguments={
            'params_file': params_file,
            'map': map_yaml_file
        }.items(),
    )

    ld = LaunchDescription()
    ld.add_action(bringup_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(
        Node(
            package='tianracer_navigation',
            executable='cmd_vel_to_ackermann_drive.py',
            output='screen',
        )
    )


    return ld