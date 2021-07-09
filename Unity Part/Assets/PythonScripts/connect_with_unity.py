import cv2
import numpy as np
import socket

class UnityConnector():

    def __init__(self, host="127.0.0.1", port=25001, mode='WEB_CAM'):
        """

        :param host: the host ip
        :param port: the port for the connection
        :param mode: I've implemented only a single mode currently ,which is a WEB_CAM
                    (that is the camera screenshot that I'm going to receive from Unity)
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.width = 1000
        self.height = 1000
        self.pixel_size = 4
        self.recieved_data_length = self.width * self.height * self.pixel_size
        # self.range_convertor = interp1d([0, 1], [-1, 1])
        if (mode == 'WEB_CAM'):
            self.__case_recieving_camera_images()

    def __case_recieving_camera_images(self):
        cap = cv2.VideoCapture(0)
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.pixel_size = 3
        self.recieved_data_length = self.width * self.height * self.pixel_size

    def connect(self):
        self.sock.connect((self.host, self.port))

    def send_data(self,image, results_data):
        """
        Encodes the given results_data in the following format:
        lm1.x,lm1.y,lm1.z,lm1.visibility#...#lmi.x,lmi.y,lmi.z,lmi.visibility where i is the number of landmarks (33)
        and sends it to Unity.
        :param results_data: the results calculated
        """
        encoded_results_data = ''
        lm_str_lst = []
        if (results_data):
            # data_proceessed = []
            # 0 left_shoulder_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 1 right_shoulder_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 2 left_elbow_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 3 right_elbow_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 4 left_wrist_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 5 right_wrist_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 6 left_hip_croods = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 7 right_hip_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 8 left_knee_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 9 right_knee_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 10 left_ankle_coords = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            # 11 right_ankle_croods = results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]

            # for id, lm in enumerate(results_data.pose_landmarks.landmark):
            #     if (id in range(11) or id in range(17, 23) or id in range(27, 33)):
            #         # First range is the face, second range are for the fists ,third range is for the feet
            #         # See : https://google.github.io/mediapipe/solutions/pose.html
            #         continue
            #     lm_str = str(lm.x) + ',' + str(lm.y) + ',' + str(lm.z)  # + ',' + str(lm.visibility)
            #     lm_str_lst.append(lm_str)
            # encoded_results_data = '#'.join(lm_str_lst)
            # v1_direction_a = str(results_data[0].x -results_data[2].x)+','+str(results_data[0].y -results_data[2].y)
            # v1_direction_b = str(results_data[0].x -results_data[6].x)+','+str(results_data[0].y -results_data[6].y)
            # print(v1_direction_a, v1_direction_b)
            #
            # v2_direction_a = str(results_data[1].y -results_data[3].y)+','+str(results_data[1].y -results_data[3].y)
            # v2_direction_b = str(results_data[1].y -results_data[7].y)+','+str(results_data[1].y -results_data[7].y)

            # lm_str_lst=[v1_direction_a,v1_direction_b,v2_direction_a,v2_direction_b]

            #Upper left
            left_upper_arm_start = str(results_data[0].x) + ',' + str(results_data[0].y)
            left_upper_arm_end_forearm_start = str(results_data[2].x) + ',' + str(results_data[2].y)
            left_forearm_end = str(results_data[4].x) + ',' + str(results_data[4].y)

            #Upper right
            right_upper_arm_start = str(results_data[1].x) + ',' + str(results_data[1].y)
            right_upper_arm_end_forearm_start = str(results_data[3].x) + ',' + str(results_data[3].y)
            right_forearm_end = str(results_data[5].x) + ',' + str(results_data[5].y)

            #Lower left
            left_thigh_start = str(results_data[6].x) + ',' + str(results_data[6].y)
            left_thigh_end_shin_start = str(results_data[8].x) + ',' + str(results_data[8].y)
            left_shin_end = str(results_data[10].x) + ',' + str(results_data[10].y)

            #Lower right
            right_thigh_start = str(results_data[7].x) + ',' + str(results_data[7].y)
            right_thigh_end_shin_start = str(results_data[9].x) + ',' + str(results_data[9].y)
            right_shin_end = str(results_data[11].x) + ',' + str(results_data[11].y)
            #img_as_string = ''.join(image.reshape(-1).astype(str))
            lm_str_lst = [left_upper_arm_start, left_upper_arm_end_forearm_start, left_forearm_end,
                          right_upper_arm_start, right_upper_arm_end_forearm_start,right_forearm_end,
                          left_thigh_start,left_thigh_end_shin_start,left_shin_end,
                          right_thigh_start,right_thigh_end_shin_start,right_shin_end]

            # for lm in results_data:
            #     # if(lm)
            #     lm_str = str((lm.x)) + ',' + str((lm.y))   # + ',' + str(lm.visibility)
            #     lm_str_lst.append(lm_str)
        encoded_results_data = '#'.join(lm_str_lst)
        self.sock.sendall(encoded_results_data.encode("UTF-8"))

        # print(len(encoded_results_data.encode("UTF-8")))
        # What I send is in the following order (These are the ones I need):
        # left_shoulder,right_shoulder,left_elbow,right_elbow,left_wrist,right_wrist,left_hip,right_hip,left_knee,right_knee,left_ankle,right_ankle
        # print(len(''.join(image.reshape(-1).astype(str))))
        # self.sock.sendall(image)

        # B-upper_arm_L,B-upper_arm_R,B-forearm_L,B-forearm_R,B-hand_R,B-hand_L,B-thigh_L,B-thigh_R,B-shin_L,B-shin_R,B-foot_R,B-foot_L

    def recieve_data(self):
        receivedData = self.sock.recv(self.recieved_data_length)  # my default resolution 640*480
        ls =list(receivedData)
        img = np.array(ls)

        return img.reshape((self.width, self.height, self.pixel_size))
