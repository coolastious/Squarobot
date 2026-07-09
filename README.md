# Squarobot: ROS 2 Autonomous Navigation 

A custom-built, differential-drive robot simulated in Gazebo, featuring full mapping and autonomous navigation capabilities using the ROS 2 Navigation Stack (Nav2) and SLAM Toolbox.

## 🛠️ System Specifications

This project was built and tested on the following system architecture:

| Component | Specification |
| :--- | :--- |
| **Host OS** | Mac OS 26.5.1 |
| **Guest OS** | Ubuntu 24.04 LTS |
| **Virtualization** | VmWare Fusion - Professional 26H1 |
| **ROS 2 Version**| Jazzy |
| **Simulation** | Gazebo Sim 8.11.0 |
| **Visualization**| RViz2 (14.1.20) / OGRE (1.12.10) |
| **Python** | 3.12.3 |

---

## 📦 Required Packages & Installation

Before running the project, ensure you have the necessary ROS 2 Jazzy packages installed. Open a terminal and run the following commands:

` ` `bash
sudo apt update

# Install SLAM Toolbox
sudo apt install ros-jazzy-slam-toolbox

# Install Navigation 2 (Nav2) and Bringup
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup

# Install Teleop Twist Keyboard for manual control
sudo apt install ros-jazzy-teleop-twist-keyboard

# Install Gazebo ROS packages (if not already installed)
sudo apt install ros-jazzy-ros-gz
` ` `

### To Install Workspace Itself
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/coolastious/Squarobot-ROS2-Jazzy-.git .
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

## 🗺️ GOAL
SLAM the squarobot in RViz, then save the map, and do the navigation of the robot in the saved map.

## 💻 Terminal Commands (Mapping)

### Gazebo Launch (Terminal 1)
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch squarobot_gazebo gazebo.launch.py
```

### Start SLAM (Terminal 2)
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/home/yz/ros2_ws/src/squarobot_slam/config/mapper_params_online_async.yaml use_sim_time:=true
```

### RViz Command (Terminal 3)
```bash
source /opt/ros/jazzy/setup.bash
ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true
```

### Teleop Key (Terminal 4)
```bash
source /opt/ros/jazzy/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### Map Saving Command (Terminal 5)
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run nav2_map_server map_saver_cli -t /map -f ~/ros2_ws/src/squarobot_slam/maps/my_first_map --ros-args -p use_sim_time:=true -p map_subscribe_transient_local:=true
```
## 🎯 Navigation Commands

### Start Gazebo (Terminal 1)
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch squarobot_gazebo gazebo.launch.py
```

### Launch Nav2 (Terminal 2)
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 launch nav2_bringup bringup_launch.py map:=/home/yz/ros2_ws/src/squarobot_slam/maps/my_first_map.yaml use_sim_time:=true
```

### Launch RViz (Terminal 3)
```bash 
cd ~/ros2_ws
source install/setup.bash
ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz --ros-args -p use_sim_time:=true
```
