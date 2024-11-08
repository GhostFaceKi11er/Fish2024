import bpy
import json
import math
import random

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def outputinfo():
    with open("/home/haitaoxu/code/data.json", "r") as f:
        data = json.load(f)

    joints = {}  # 用于存储每个 joint 对象，以便设置 link 的相对位置

    # 创建 joint 并显示在世界坐标系中（绝对坐标）
    for joint in data["joints"]:
        joint_obj = bpy.data.objects.new(joint["name"], None)
        joint_obj.location = joint["origin_xyz"]  # 使用绝对坐标
        joint_obj.rotation_euler = [math.radians(angle) for angle in joint["origin_rpy"]]
        #bpy.context.collection.objects.link(joint_obj)


    # 创建 link 并设置位置和 delta 属性
    for index, link in enumerate(data["links"]):
        if link["collision"]:
            bpy.ops.import_mesh.stl(filepath=link["collision"])
            visual_obj = bpy.context.selected_objects[0]
            visual_obj.name = link["name"] + "_collision"

            # 第一个 link 直接使用世界坐标
            if index == 0:
                visual_obj.location = link["origin_xyz"]  # 绝对位置
                visual_obj.rotation_euler = [math.radians(angle) for angle in link["origin_rpy"]]
            else:
                # 其他 link 的位置相对于前一个 joint
                previous_joint = joints.get(link["name"])
                if previous_joint:
                    visual_obj.parent = previous_joint  # 设置前一个 joint 为父对象
                    visual_obj.location = link["origin_xyz"]  # 相对位置
                    visual_obj.rotation_euler = [math.radians(angle) for angle in link["origin_rpy"]]
                    # 清除相对位置的变换，使其相对于父 joint 的局部位置生效
                    visual_obj.matrix_parent_inverse = previous_joint.matrix_world.inverted()

            # 设置 delta_location 和 delta_rotation_euler
            joint = data["joints"][index] if index < len(data["joints"]) else None
            if joint:
                visual_obj.delta_location = joint["origin_xyz"]
                visual_obj.delta_rotation_euler = [angle for angle in joint["origin_rpy"]]
        else:
            pass


def main():
    print('输出到 Blender 中')
    outputinfo()

if __name__ == '__main__':
    main()
