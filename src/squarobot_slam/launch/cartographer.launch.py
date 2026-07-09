import os
import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch_ros.actions import Node
from launch.conditions import IfCondition

def generate_launch_description():
  prefix_address = get_package_share_directory('squarobot_slam')
  config_directory = os.path.join(prefix_address, 'config')
  slam_config = 'slam.lua'
  res = LaunchConfiguration('resolution', default='0.05')
  publish_period = LaunchConfiguration('publish_period_sec', default='1.0')
  use_sim_time = LaunchConfiguration('use_sim_time')
  exploration = LaunchConfiguration('exploration')  # SLAM in exploration mode
  map_file = LaunchConfiguration('map')
  #pbstream_file = LaunchConfiguration('load_state_filename', default='/home/pi/amr/src/squarobot_slam/maps/mymap.pbstream')

  return LaunchDescription([
    SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
    
    DeclareLaunchArgument(
      name='use_sim_time',
      default_value='False',
      description='Flag to enable use_sim_time'
    ),
    
    DeclareLaunchArgument(
      name='exploration',
      default_value='False',        #True
      description='Flag to enable exploration mode'
    ),
    
    DeclareLaunchArgument(
      'resolution',
      default_value=res,
      description='Configure the resolution'
    ),

    DeclareLaunchArgument(
      'publish_period_sec',
      default_value=publish_period,
      description='Publish period in seconds'
    ),

    DeclareLaunchArgument(
      'configuration_directory',
      default_value=config_directory,
      description='Path to the .lua files'
    ),

    DeclareLaunchArgument(
      'slam_configuration_basename',
      default_value=slam_config,
      description='Name of .lua file to be used'
    ),

    DeclareLaunchArgument(
      'localization_configuration_basename',
      default_value=slam_config,
      description='Name of .lua file to be used'
    ),
    
  #  DeclareLaunchArgument(
  #    'load_state_filename',
  #    default_value=pbstream_file,
  #    description='Path to the saved .pbstream file for localization'
  #  ),

    DeclareLaunchArgument(
      'map',
      default_value='/home/robotry/squrobot/src/squarobot_slam/maps/demo_map.yaml',  #output_map.yaml# Path to your map file
      description='Path to the saved map .yaml file for localization'
    ),
    
    ################### Cartographer ROS Nodes ###################
    
    Node(
      package='cartographer_ros',
      condition=IfCondition(exploration),
      executable='cartographer_node',
      name='as21_cartographer_node',
      arguments=[
        '-configuration_directory', config_directory,
        '-configuration_basename', slam_config
      ],
      parameters=[{'use_sim_time': use_sim_time}],
      output='screen'
    ),

  #  Node(
  #    package='cartographer_ros',
  #    condition=IfCondition(PythonExpression(['not ', exploration])),
  #    executable='cartographer_node',
  #    name='as21_cartographer_node',
  #    arguments=[
   #     '-configuration_directory', config_directory,
   #     '-configuration_basename', slam_config,
   #     '-load_state_filename', pbstream_file
   #   ],
   #   parameters=[{'use_sim_time': use_sim_time}],
   #   output='screen'
   # ),

    Node(
      package='cartographer_ros',
      condition=IfCondition(exploration),
      executable='cartographer_occupancy_grid_node',
      name='cartographer_occupancy_grid_node',
      arguments=[
        '-resolution', res,
        '-publish_period_sec', publish_period
      ],
      output='screen'
    ),

    Node(
      package='nav2_map_server',
      condition=IfCondition(PythonExpression(['not ', exploration])),
      executable='map_server',
      name='map_server',
      output='screen',
      parameters=[{'use_sim_time': use_sim_time},
                  {'yaml_filename': map_file}]
    ),
  ])

