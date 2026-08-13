joints=""

for i in range(1,21):
    joints += f'''
  <joint name="joint{i}">
    <command_interface name="position"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
'''

xml=f'''
<ros2_control name="MechanicalHandSystem" type="system">

  <hardware>
    <plugin>gazebo_ros2_control/GazeboSystem</plugin>
  </hardware>

{joints}

</ros2_control>
'''

print(xml)
