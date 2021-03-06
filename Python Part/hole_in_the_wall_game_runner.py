import cv2
import numpy as np
from pose_estimation import PoseDetector
from connect_with_unity import UnityConnector
import time

if __name__ == "__main__":
    pose_detector = PoseDetector()
    unity_connector = UnityConnector(mode='WEB_CAM')
    unity_connector.connect()

    cap = cv2.VideoCapture(0)
    i = 0
    while (True):
        time.sleep(0.1)
        # image = unity_connector.recieve_data()
        success, image = cap.read()  # Comment this and uncomment the line above to recieve the camera data from Unity.
        results, results_to_display = pose_detector.getPoseEvaluation(image)
        pose_detector.draw(image, results_to_display)
        pose_detector.displayImage(image)
        unity_connector.send_data(image, results)
