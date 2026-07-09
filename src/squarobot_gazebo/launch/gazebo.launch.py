import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue  # <-- Added this import

def generate_launch_description():
    pkg_squarobot_gazebo = get_package_share_directory('squarobot_gazebo')
    pkg_squarobot_urdf = get_package_share_directory('squarobot_urdf')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Path to files
    world_path = os.path.join(pkg_squarobot_gazebo, 'worlds', 'simple_wall.sdf')
    xacro_file = os.path.join(pkg_squarobot_urdf, 'urdf', 'squaroboturdf.xacro') 
    
    use_sim_time = LaunchConfiguration('use_sim_time')

    # 1. Robot State Publisher (Fixed for Jazzy strict typing)
    robot_description_content = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description_content
        }]
    )

    # 2. Start Gazebo Harmonic
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_path]}.items(),
    )

    # 3. Spawn the robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'squarobot',
            '-topic', 'robot_description',
            '-z', '0.1' 
        ],
        output='screen'
    )

    # 4. The ROS 2 <-> Gazebo Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Clock (Gazebo -> ROS)
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            # Velocity Commands (ROS -> Gazebo)
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            # Odometry (Gazebo -> ROS)
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            # LiDAR Scan (Gazebo -> ROS)
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            # Joint States (Gazebo -> ROS)
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            # TF (Gazebo -> ROS)
            '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
        ],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Flag to enable use_sim_time'
        ),
        robot_state_publisher,
        gz_sim,
        spawn_entity,
        bridge
    ])