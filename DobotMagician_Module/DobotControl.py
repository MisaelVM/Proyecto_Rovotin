import yaml
import socket
import DobotDllType as dType

HOST = "192.168.178.182"
PORT = 65435
BUFFER_SIZE = 256


def yaml_to_point(yaml_message):
    target = yaml_message["target"]
    position = []
    position.append(target["y"] * 240 + 75 if target["y"] > 0 else 0)
    position.append(target["x"] * 300 + 15)
    position.append(target["z"] * 100 + 75)
    return position

def main():
    # Start point with respect to the robot base frame
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    conn, address = s.accept()

    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
        dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
        dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
    }

    # Load Dll and get the CDLL object
    api = dType.load()
    # Connect Dobot
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])

    if (state != dType.DobotConnect.DobotConnect_NoError):
        print("Unable to connect to Dobot!")
        return

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #Async Home
    erick = dType.SetHOMECmd(api, temp = 0, isQueued = 1)
    print("Command first HOME", erick[0])

    #Start to Execute Command Queue
    dType.SetQueuedCmdStartExec(api)

    lastIndex = -1
    while True:
        data = conn.recv(BUFFER_SIZE).decode()
        if not data:
            break

        try:
            yaml_obj = yaml.safe_load(data)
            position = yaml_to_point(yaml_obj)
            msg = "OK"
            print(position)
            x, y, z = position
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0, isQueued=1)[0]
            
        except Exception as e:
            print(e)
            msg = "ERROR"
        conn.send(msg.encode())
    

    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        lastIndex = dType.GetQueuedCmdCurrentIndex(api)[0]

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

    #Disconnect Dobot
    dType.DisconnectDobot(api)

if __name__ == '__main__':
    main()
