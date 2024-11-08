from urchin import URDF
import urchin
# from urdfpy import URDF
import numpy as np
import json

robot = URDF.load("/home/haitaoxu/code/robot_dart-master/utheque/ur3e/ur3e.urdf")



filenameFront = '/home/haitaoxu/code/robot_dart-master/utheque/ur3e/'


class Linknew:
    def __init__(self, name='', visual='', collision='', origin_xyz = [0, 0, 0],origin_rpy = [0, 0, 0]):
        self.name = name
        self.visual = visual
        self.collision = collision
        self.origin_xyz = origin_xyz
        self.origin_rpy = origin_rpy
        
    def to_dict(self):
        return {
            "name": self.name,
            "visual": self.visual,
            "collision": self.collision,
            "origin_xyz": self.origin_xyz,
            "origin_rpy": self.origin_rpy,
        }

class Jointnew:

    def __init__(self, name='', origin_xyz = [0, 0, 0],origin_rpy = [0, 0, 0]):
        self.name = name
        self.origin_xyz = origin_xyz
        self.origin_rpy = origin_rpy

    
    def to_dict(self):
        return {
            "name": self.name,
            "origin_xyz": self.origin_xyz,
            "origin_rpy": self.origin_rpy,

        }

link_matrixs = []
joint_matrixs = []
def get_info_fromURDF():
    linksOut = []
    for link in robot.links:
        linkToblender = Linknew()
        if link.name:
            linkToblender.name = link.name

        if link.visuals:
            filename_visual = filenameFront + link.visuals[0].geometry.mesh.filename
            linkToblender.visual = filename_visual
            #get visual geometry mesh filename absolute path
        if link.collisions:
            filename_collision = filenameFront + link.collisions[0].geometry.mesh.filename
            linkToblender.collision = filename_collision
            print(linkToblender.collision)
            #get collision geometry m./franka_description
        if link.inertial.origin.size:
            link_matrixs.append(link.inertial.origin)
        linksOut.append(linkToblender)
        

        
    jointsOut = []
    for joint in robot.joints:
        jointToblender = Jointnew()
        jointToblender.type = joint.joint_type

        if joint.name:
            jointToblender.name = joint.name
        
        if joint.origin.size:
            joint_matrixs.append(joint.origin)
            #jointToblender.origin = joint.origin

        jointsOut.append(jointToblender)

    return linksOut, jointsOut






def main():
    linksOut, jointsOut = get_info_fromURDF()
    #print(link_matrixs)
    data = {
        "links": [link.to_dict() for link in linksOut],
        "joints": [joint.to_dict() for joint in jointsOut],
        }


    with open('/home/haitaoxu/code/data.json', "w") as json_file:
        json.dump(data, json_file, indent=4)
    

    joint_position_matrices = [np.eye(4)]
    for i, joint_matrix in enumerate(joint_matrixs):
        current_joint = joint_position_matrices[-1] @ joint_matrix 
        joint_position_matrices.append(current_joint)
        #print(f"Joint {i+1} position matrix:\n{current_joint}\n")
    # 更新 JSON 文件中的 joint origin_xyz 和 origin_rpy
    with open("data.json", "r") as file:
        data = json.load(file)

    for i, joint in enumerate(data["joints"]):
        if i < len(joint_position_matrices):
            joint_xyz_rpy = urchin.matrix_to_xyz_rpy(joint_position_matrices[i]).tolist()
            joint["origin_xyz"] = joint_xyz_rpy[:3]
            joint["origin_rpy"] = joint_xyz_rpy[3:]

    

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)



if __name__ == '__main__':
    main()


    




    





            

            






