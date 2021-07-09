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
            # See : https://google.github.io/mediapipe/solutions/pose.html for more info.
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

    def draw(self, image, results):
        """
        Receives pose evaluations.
        """
        if (results.pose_landmarks):
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                # You can also skip indices to highlight the ones you didn't skip.
                # (The skipped ones will still appear but in smaller circles and different colors (red by default))
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(image, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return image

    def displayImage(self, image, pTimeReset=False, show_fps=True, window_size=(300, 250)):
        if (pTimeReset):
            self.pTime = 0
        fps_text = ''
        if (show_fps):
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            fps_text = str(int(fps))
        cv2.putText(img=image, text=fps_text, org=(70, 50), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=3, color=(255, 0, 0), thickness=3)
        # Control Window size
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', window_size[0], window_size[1])
        # Mirror image
        cv2.imshow("image", cv2.flip(image, 1))
        cv2.waitKey(1)


if __name__ == "__main__":
    # cap =cv2.VideoCapture( 'C:\\Users\\anism\\OneDrive\\Desktop\\Perceptual\\vids\\1.mp4')
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    while (True):
        success, image = cap.read()
        # With unity_mode =False to test out the pose detection and draw on your own camera
        _, results_to_display = detector.getPoseEvaluation(image, unity_mode=False)
        detector.draw(image, results_to_display)
        detector.displayImage(image, window_size=(300, 250))
