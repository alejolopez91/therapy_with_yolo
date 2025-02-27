import cv2
import numpy as np
import ultralytics
import math
import sqlite3

# RIGHT_SHOULDER = [8, 6, 5]
# LEFT_SHOULDER = [6, 5, 7]
# routine = {
#   init: [{ joint: RIGHT_SHOULDER, angle: 340, operation: >= }, { joint: LEFT_SHOULDER, angle: 340, operation: >= }],
#   middle: [{ joint: RIGHT_SHOULDER, angle: 35, operation: <= }, { joint: LEFT_SHOULDER, angle: 35, operation: <= }],
#   end: [{ joint: RIGHT_SHOULDER, angle: 340, operation: >= }, { joint: LEFT_SHOULDER, angle: 340, operation: >= }]
# }
# Connect to the SQLite database (or create it if it doesn't exist)
def create_db_connection():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('yolo_pose_estimation.db')
    # Create a cursor object
    cursor = conn.cursor()

def compute_angle(start, middle, end):
    vector1 = middle - start
    vector2 = end - middle
    dot_product = np.dot(vector1, vector2)
    magnitude_v1 = np.linalg.norm(vector1)
    magnitude_v2 = np.linalg.norm(vector2)
    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)

    # Determine the sign of the angle
    cross_product = np.cross(vector1, vector2)
    if cross_product < 0:
        angle_deg = 360 - angle_deg

    return angle_deg

class PoseEstimation:
    def __init__(self):
        self.model = ultralytics.YOLO("yolo11n-pose.pt")
        self.active_keypoints = [10, 8, 6, 5, 7, 9]
        self.scale = 1/2
        current_fps = 24
        desired_fps = 10
        self.rep_count = 0
        self.rep_status = 0
        self.skip_factor = current_fps // desired_fps

    def analyze_pose(self, show_angle=False):
        # if show_angle:

        frame_count = 0
        color = (255, 255, 0)

        cv2.namedWindow("Pose estimation live", cv2.WINDOW_NORMAL)
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % self.skip_factor != 0:
                continue
            height, width, _ = frame.shape
            window_width = int(frame.shape[1] * self.scale)
            window_height  = int(frame.shape[0] * self.scale)
            cv2.resizeWindow("Pose estimation live", window_width, window_height)

            results = self.model(frame)
            keypoints = results[0].keypoints.xy.cpu().numpy()[0]

            # Draw
            if len(keypoints) > 0:
                for i in range(len(self.active_keypoints) - 1):
                    pt1 = tuple(keypoints[self.active_keypoints[i]].astype(int))
                    pt2 = tuple(keypoints[self.active_keypoints[i+1]].astype(int))
                    cv2.line(frame, pt1, pt2, color, 8)
                    cv2.circle(frame, pt1, 5, color, -1)

                if show_angle:
                    angle_right = compute_angle(
                        keypoints[self.active_keypoints[1]],
                        keypoints[self.active_keypoints[2]],
                        keypoints[self.active_keypoints[3]]
                    )
                    angle_left = compute_angle(
                        keypoints[self.active_keypoints[2]],
                        keypoints[self.active_keypoints[3]],
                        keypoints[self.active_keypoints[4]]
                    )
                    if not math.isnan(angle_right):
                        cv2.putText(frame, f"{round(angle_right)}", (270, 270), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5, cv2.LINE_AA)
                    if not math.isnan(angle_left):
                        cv2.putText(frame, f"{round(angle_left)}", (270, 720), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5, cv2.LINE_AA)

                    if (angle_left >= 340 and angle_right >= 340) and self.rep_status == 0:
                        self.rep_status = 1
                    if (angle_left <= 35 and angle_left <= 35) and self.rep_status == 1:
                        self.rep_status = 2
                    if (angle_left >= 340 and angle_right >= 340) and self.rep_status == 2:
                        self.rep_status = 0
                        self.rep_count += 1
                    if not math.isnan(angle_right):
                        cv2.putText(frame, f"Count: {round(self.rep_count)}", (820, 270), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5, cv2.LINE_AA)

            cv2.imshow("Pose estimation live", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

def run_analyze_pose(show_angle):
    pe = PoseEstimation()
    pe.analyze_pose(show_angle=show_angle)

if __name__ == '__main__':
    run_analyze_pose(show_angle=True)


