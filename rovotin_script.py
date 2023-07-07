from robodk.robolink import Robolink, ITEM_TYPE_ROBOT
import yaml
import socket
HOST = "25.14.146.88"
PORT = 65431
BUFFER_SIZE = 256


def yaml_to_point(yaml_message):
    target = yaml_message["target"]
    position = []
    position.append(target["y"] * 240 + 50)
    position.append(target["x"] * 290)
    position.append(target["z"] * 220 + 50)
    return position

class RobotManipulation():
    def _init_(self):
        self.RDK = None
        self.robot = None
        self.position = []
        self.target = None

    def connect(self):
        self.RDK = Robolink()
        self.robot = self.RDK.ItemUserPick("", ITEM_TYPE_ROBOT)
        self.target = self.RDK.AddTarget("New Target", 0)

    def update_position(self, position):
        self.position = position
        pose_ref = self.robot.Pose()
        pose_ref.setPos(self.position)
        self.target.setPose(pose_ref)

    def force_position(self, position):
        lista_zzz = [0,-5,5,-10,10,-20,20]
        for i in range(len(lista_zzz)):
            for j in range(len(lista_zzz)):
                for k in range(len(lista_zzz)):
                    try:
                        self.position = [position[0] - lista_zzz[k], position[1]- lista_zzz[j], position[2]- lista_zzz[i]]
                        pose_ref = self.robot.Pose()
                        pose_ref.setPos(self.position)
                        self.target.setPose(pose_ref)
                        self.robot.MoveJ(self.target)
                        return
                    except:
                        path_file = "path_log_error"
                        log_f = open(path_file, "a")
                        log_f.write(str(self.position) + '\t')
                        log_f.write(str(k), str(j), str(i), '\n')
                        log_f.close()
                        continue        

    def move(self):
        try:
            self.robot.MoveJ(self.target)
        except Exception as e:
            print(e)




def main():
    # Start point with respect to the robot base frame
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    conn, address = s.accept()

    P_START = [0, -342, 0]
    P_END = [340, 342, 293]
    path_file = "path_log"
    log_file = open(path_file, "w")

    # yaml_messages = ["target: {x: 0.490453064, y: 0.847808182, z: 0.201685429}\nrot: {x: -139.347183, y: 43.2068405, z: 12.337244}",
    #                 "target: {x: 0.135441348, y: 0.990619421, z: 0.0181390364}\nrot: {x: -118.021896, y: 78.2166672, z: 36.8144531}",
    #                 "target: {x: -0.191368371, y: 0.95955503, z: 0.206476301}\nrot: {x: -62.0228653, y: 75.5114594, z: 97.666214}",
    #                 "target: {x: -0.355878741, y: 0.885371506, z: 0.299111545}\nrot: {x: -37.4690361, y: 69.0964203, z: 122.503777}",
    #                 "target: {x: -0.452168912, y: 0.842171669, z: 0.293751717}\nrot: {x: -21.6290474, y: 65.5954132, z: 135.243317}",
    #                 "target: {x: -0.498514742, y: 0.817395031, z: 0.288701415}\nrot: {x: -16.4430122, y: 65.1236038, z: 139.124298}",
    #                 "target: {x: -0.511171877, y: 0.81277442, z: 0.279465646}\nrot: {x: -12.0928097, y: 64.3420181, z: 142.307587}"
    #                 "target: {x: 0.135441348, y: 0.990619421, z: 0.0181390364}\nrot: {x: -118.021896, y: 78.2166672, z: 36.8144531}",
    #                 "target: {x: -0.191368371, y: 0.95955503, z: 0.206476301}\nrot: {x: -62.0228653, y: 75.5114594, z: 97.666214}",
    #                 "target: {x: -0.355878741, y: 0.885371506, z: 0.299111545}\nrot: {x: -37.4690361, y: 69.0964203, z: 122.503777}",
    #                 "target: {x: -0.452168912, y: 0.842171669, z: 0.293751717}\nrot: {x: -21.6290474, y: 65.5954132, z: 135.243317}",
    #                 "target: {x: -0.498514742, y: 0.817395031, z: 0.288701415}\nrot: {x: -16.4430122, y: 65.1236038, z: 139.124298}",
    #                 "target: {x: -0.511171877, y: 0.81277442, z: 0.279465646}\nrot: {x: -12.0928097, y: 64.3420181, z: 142.307587}"
    #                 "target: {x: 0.135441348, y: 0.990619421, z: 0.0181390364}\nrot: {x: -118.021896, y: 78.2166672, z: 36.8144531}",
    #                 "target: {x: -0.191368371, y: 0.95955503, z: 0.206476301}\nrot: {x: -62.0228653, y: 75.5114594, z: 97.666214}",
    #                 "target: {x: -0.355878741, y: 0.885371506, z: 0.299111545}\nrot: {x: -37.4690361, y: 69.0964203, z: 122.503777}",
    #                 "target: {x: -0.452168912, y: 0.842171669, z: 0.293751717}\nrot: {x: -21.6290474, y: 65.5954132, z: 135.243317}",
    #                 "target: {x: -0.498514742, y: 0.817395031, z: 0.288701415}\nrot: {x: -16.4430122, y: 65.1236038, z: 139.124298}",
    #                 "target: {x: -0.511171877, y: 0.81277442, z: 0.279465646}\nrot: {x: -12.0928097, y: 64.3420181, z: 142.307587}"
    #                 "target: {x: 0.135441348, y: 0.990619421, z: 0.0181390364}\nrot: {x: -118.021896, y: 78.2166672, z: 36.8144531}",
    #                 "target: {x: -0.191368371, y: 0.95955503, z: 0.206476301}\nrot: {x: -62.0228653, y: 75.5114594, z: 97.666214}",
    #                 "target: {x: -0.355878741, y: 0.885371506, z: 0.299111545}\nrot: {x: -37.4690361, y: 69.0964203, z: 122.503777}",
    #                 "target: {x: -0.452168912, y: 0.842171669, z: 0.293751717}\nrot: {x: -21.6290474, y: 65.5954132, z: 135.243317}",
    #                 "target: {x: -0.498514742, y: 0.817395031, z: 0.288701415}\nrot: {x: -16.4430122, y: 65.1236038, z: 139.124298}",
    #                 "target: {x: -0.511171877, y: 0.81277442, z: 0.279465646}\nrot: {x: -12.0928097, y: 64.3420181, z: 142.307587}"
    #                 ]
    
    robot_manipulation = RobotManipulation()
    robot_manipulation.connect()
    while True:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data:
            break

        try:
            yaml_obj = yaml.safe_load(data)
            position = yaml_to_point(yaml_obj)

            log_file = open(path_file, "a")
            log_file.write(str(position) + '\n')
            log_file.close()
            
            robot_manipulation.force_position(position)

            log_file.close()
            msg = "OK"
        except Exception as e:
            print(e)
            msg = "ERROR"
        conn.send(msg.encode())
    conn.close()

if __name__ == '__main__':
    main()