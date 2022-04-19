#!/bin/bash

echo "How many drones"
read num_drones
x-terminal-emulator  -e cd ~/PX4-Autopilot/Tools
./gazebo_sitl_multiple_run.sh -m plane -n num_drones


