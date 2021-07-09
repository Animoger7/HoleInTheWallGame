import cv2  # for image processing
import mediapipe as mp  # to get pose estimation - It uses RGB
import time
import numpy as np

"""
This class extends Pose utilites.
"""


class PoseDetector(mp.solutions.pose.Pose):
    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        super().__init__(static_image_mode, model_complexity, smooth_landmarks, min_detection_confidence,
                         min_tracking_confidence)
        self.pTime = 0

    def getPoseEvaluation(self, image, color_conversion=cv2.COLOR_BGR2RGB, unity_mode=True):
        """
        Recieves an image and evalutaes the pose.
        """
        results_data = super().process(cv2.cvtColor(image, color_conversion))
        if (unity_mode):
            if (not results_data.pose_landmarks):
                return ([], results_data)
            return (results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]

                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW]
                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]

                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]


                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP]
                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_HIP]

                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_KNEE]
                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_KNEE]

                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ANKLE]
                    , results_data.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE]), results_data
        else:
            return (results_data, results_data)

    # //up =60 3ade 0 (bs bteje down
    def draw(self, image, results):
        """
        Receives pose evaluations.
        """
        if (results.pose_landmarks):
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks,
                                                      mp.solutions.pose.POSE_CONNECTIONS)  # to do the connections

            for id, lm in enumerate(results.pose_landmarks.landmark):
                # if(id in range(11) or id in range(17,23) or id in range(29,33)):
                # #First range is the face, second range are for the fists ,third range is for the feet
                # # See : https://google.github.io/mediapipe/solutions/pose.html
                #     continue
                lm_str = str(lm.x) + ',' + str(lm.y) + ',' + str(lm.z) + ',' + str(lm.visibility)
                h, w, c = image.shape  # c for channel
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(image, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                # cv2.putText(image, str(lm), org=(cx, cy), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                #             color=(255, 0, 0), thickness=3)
        return image

    def displayImage(self, image, pTimeReset=False, show_fps=True):
        if (pTimeReset):
            self.pTime = 0
        fps_text = ''
        if (show_fps):
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            fps_text = str(int(fps))
        cv2.putText(img=image, text=fps_text, org=(70, 50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3,
                    color=(255, 0, 0), thickness=3)
        cv2.imshow("image", image)
        cv2.waitKey(1)


if __name__ == "__main__":
    # cap =cv2.VideoCapture( 'C:\\Users\\anism\\OneDrive\\Desktop\\Perceptual\\vids\\1.mp4')
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    while (True):
        success, image = cap.read()
        results,b = detector.getPoseEvaluation(image)
        detector.draw(image, results)
        detector.displayImage(image)
