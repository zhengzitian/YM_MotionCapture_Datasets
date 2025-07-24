from urdfpy import URDF

# 加载 URDF 文件
robot = URDF.load("/home/ym/robots/y1_description/urdf/ymbot_E.urdf")

joint_name = []
lower_limit = []
upper_limit = []
effort = []
velocity = []

# 遍历所有关节
for joint in robot.joints:
    print(f"Joint Name: {joint.name}")
    
    # 检查是否有关节限制
    
    if joint.joint_type == "revolute" and joint.limit is not None:
        print(f"  Lower Limit: {joint.limit.lower}")
        print(f"  Upper Limit: {joint.limit.upper}")
        print(f"  Effort: {joint.limit.effort}")
        print(f"  Velocity: {joint.limit.velocity}")
        joint_name.append(joint.name)
        lower_limit.append(joint.limit.lower)   
        upper_limit.append(joint.limit.upper)
        effort.append(joint.limit.effort)
        velocity.append(joint.limit.velocity)

    else:
        print("  No limits defined for this joint.")

    print(1)
print(joint_name)
print(lower_limit)
print(upper_limit)
print(effort)
print(velocity)

print(2)