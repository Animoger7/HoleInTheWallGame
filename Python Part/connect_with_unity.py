import cv2
import numpy as np
import socket


class UnityConnector():

    def __init__(self, host="127.0.0.1", port=25001, mode='WEB_CAM'):
        """

        :param host: the host ip
        :param port: the port for the connection
        :param mode: I've implemented only a single mode currently ,which is a WEB_CAM
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.width = 1000
        self.height = 1000
        self.pixel_size = 4
        self.recieved_data_length = self.width * self.height * self.pixel_size
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

    def send_data(self, image, results_data):
        """
        Encodes the given results_data and sends it to unity:
        :param results_data: the results calculated
        """
        lm_str_lst = []
        if (results_data):
            # for lm in results_data:
            #     # if(lm)
            #     lm_str = str((lm.x)) + ',' + str((lm.y))   # + ',' + str(lm.visibility)
            #     lm_str_lst.append(lm_str)

            # Upper left
            left_upper_arm_start = str(results_data[0].x) + ',' + str(results_data[0].y)
            left_upper_arm_end_forearm_start = str(results_data[2].x) + ',' + str(results_data[2].y)
            left_forearm_end = str(results_data[4].x) + ',' + str(results_data[4].y)

            # Upper right
            right_upper_arm_start = str(results_data[1].x) + ',' + str(results_data[1].y)
            right_upper_arm_end_forearm_start = str(results_data[3].x) + ',' + str(results_data[3].y)
            right_forearm_end = str(results_data[5].x) + ',' + str(results_data[5].y)

            # Lower left
            left_thigh_start = str(results_data[6].x) + ',' + str(results_data[6].y)
            left_thigh_end_shin_start = str(results_data[8].x) + ',' + str(results_data[8].y)
            left_shin_end = str(results_data[10].x) + ',' + str(results_data[10].y)

            # Lower right
            right_thigh_start = str(results_data[7].x) + ',' + str(results_data[7].y)
            right_thigh_end_shin_start = str(results_data[9].x) + ',' + str(results_data[9].y)
            right_shin_end = str(results_data[11].x) + ',' + str(results_data[11].y)
            # img_as_string = ''.join(image.reshape(-1).astype(str))
            lm_str_lst = [left_upper_arm_start, left_upper_arm_end_forearm_start, left_forearm_end,
                          right_upper_arm_start, right_upper_arm_end_forearm_start, right_forearm_end,
                          left_thigh_start, left_thigh_end_shin_start, left_shin_end,
                          right_thigh_start, right_thigh_end_shin_start, right_shin_end]

        encoded_results_data = '#'.join(lm_str_lst)
        self.sock.sendall(encoded_results_data.encode("UTF-8"))

    def recieve_data(self):
        """
        Currently irrelevant in Hole In The Wall Game, but this basically controls the data recieved from the socket.
        IF you want to recieve the camera data as well from Unity (to avoid using the camer ain python) ,
        choose mode = WEB_CAM in the constructor, or create other modes and adjust the sizes accordingly.
        """
        receivedData = self.sock.recv(self.recieved_data_length)  # my default resolution 640*480
        ls = list(receivedData)
        img = np.array(ls)
        return img.reshape((self.width, self.height, self.pixel_size))
