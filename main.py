import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
import cv2
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import socket

class GestureRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # ... (same initialization code as before)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverAddressPort = ("127.0.0.1", 5052)
        self.tipIds = [4, 8, 12, 16, 20]

        self.worker = Worker()
        self.worker.frame_update.connect(self.update_frame)
        self.worker.start()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gesture Recognition App")
        self.setGeometry(100, 100, 1200, 800)  # Adjust the window size as needed

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        upper_layout = QHBoxLayout()
        webcam_frame = self.create_webcam_frame()
        instructions_frame = self.create_instructions_frame()
        upper_layout.addWidget(webcam_frame, 2)
        upper_layout.addWidget(instructions_frame, 2)
        main_layout.addLayout(upper_layout, 6)

        count_layout = QHBoxLayout()
        self.count_label = QLabel("Left hand: 0   Right hand: 0")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label.setFont(QFont("Arial", 18))
        count_layout.addWidget(self.count_label)
        main_layout.addLayout(count_layout, 1)

    def create_webcam_frame(self):
        webcam_frame = QWidget()
        #webcam_frame.setStyleSheet("border: 2px solid red; background-color: black;")

        self.webcam_label = QLabel(self)
        layout = QVBoxLayout(webcam_frame)
        layout.addWidget(self.webcam_label)
        return webcam_frame

    def create_instructions_frame(self):
        instructions_frame = QWidget()
        #instructions_frame.setStyleSheet("border: 2px solid red; background-color: #f0f0f0;")

        instructions_text = """
        
        
        Gesture Recognition Instructions:
        1. Position both hands within the frame.
        2. App detects 0 fingers if no fingers are visible.
        3. App recognizes 1 for the first finger shown (excluding thumb).
        4. App recognizes 2 for the first two fingers shown (excluding thumb).
        5. App recognizes 3 for the first three fingers shown (excluding thumb).
        6. App recognizes 4 for the first four fingers shown (excluding thumb).
        7. App recognizes 5 for all fingers, including the thumb.
        8. Ensure a suitable background for accurate recognition.
        """

        self.instructions_label = QLabel(instructions_text)

        layout = QVBoxLayout(instructions_frame)
        layout.addWidget(self.instructions_label)
        return instructions_frame

    def update_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hands, _ = self.detector.findHands(frame)  # with draw

            if len(hands) == 2:
                if len(hands) == 2:
                    hand1 = hands[0]
                    hand2 = hands[1]

                    # Your gesture recognition logic here
                    # ...
                    lmList1 = hand1["lmList"]
                    lmList2 = hand2["lmList"]

                    rList = []
                    lList = []
                    # print(lmList1[4][0], " : ", lmList1[20][0])
                    if (lmList1[4][0] > lmList1[20][0]):
                        rList = lmList1
                        lList = lmList2
                    else:
                        rList = lmList2
                        lList = lmList1

                    # Right Hand
                    rfingers = []

                    # Thumb
                    if rList[self.tipIds[0]][0] > rList[self.tipIds[1]][0]:
                        rfingers.append(1)
                    else:
                        rfingers.append(0)

                    # 4 Fingers
                    for id in range(1, 5):
                        if rList[self.tipIds[id]][1] < rList[self.tipIds[id] - 2][1]:
                            rfingers.append(1)
                        else:
                            rfingers.append(0)

                    # print(fingers)
                    rdata = rfingers.count(1)

                    # Left Hand
                    lfingers = []

                    # Thumb
                    if lList[self.tipIds[0]][0] < lList[self.tipIds[1]][0]:
                        lfingers.append(1)
                    else:
                        lfingers.append(0)

                    # 4 Fingers
                    for id in range(1, 5):
                        if lList[self.tipIds[id]][1] < lList[self.tipIds[id] - 2][1]:
                            lfingers.append(1)
                        else:
                            lfingers.append(0)

                    # print(fingers)
                    ldata = lfingers.count(1)

                    #rdata = ...  # Calculate right hand gesture count
                    #ldata = ...  # Calculate left hand gesture count

                    self.count_label.setText(f"Left hand: {ldata}   Right hand: {rdata}")

        image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.webcam_label.setPixmap(pixmap)

class Worker(QThread):
    frame_update = pyqtSignal(object)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            self.frame_update.emit(frame)
            self.msleep(30)  # Update frame every 30 ms

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GestureRecognitionApp()
    window.show()
    sys.exit(app.exec_())





























# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
# import cv2
# import mediapipe as mp
# from cvzone.HandTrackingModule import HandDetector
# import socket
#
# class GestureRecognitionApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         # ... (same initialization code as before)
#
#         self.mp_hands = mp.solutions.hands
#         self.hands = self.mp_hands.Hands()
#         self.detector = HandDetector(detectionCon=0.8, maxHands=2)
#
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.serverAddressPort = ("127.0.0.1", 5052)
#         self.tipIds = [4, 8, 12, 16, 20]
#
#         self.worker = Worker()
#         self.worker.frame_update.connect(self.update_frame)
#         self.worker.start()
#
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle("Gesture Recognition App")
#         self.setGeometry(100, 100, 1000, 600)  # Adjust the window size as needed
#
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         main_layout = QHBoxLayout(central_widget)
#
#         webcam_frame = self.create_webcam_frame()
#         instructions_frame = self.create_instructions_frame()
#
#         main_layout.addWidget(webcam_frame, 2)  # Use stretch factor to adjust sizes
#         main_layout.addWidget(instructions_frame, 2)  # Use stretch factor to adjust sizes
#
#         count_layout = QHBoxLayout()
#
#         self.count_label = QLabel("Left hand: 0   Right hand: 0")
#         count_layout.addWidget(self.count_label, alignment=Qt.AlignmentFlag.AlignCenter)
#
#         main_layout.addLayout(count_layout, 1)  # Use stretch factor to adjust sizes
#
#     def create_webcam_frame(self):
#         webcam_frame = QWidget()
#         webcam_frame.setStyleSheet("border: 2px solid red;")
#
#         self.webcam_label = QLabel(self)
#         layout = QVBoxLayout(webcam_frame)
#         layout.addWidget(self.webcam_label)
#
#         return webcam_frame
#
#     def create_instructions_frame(self):
#         instructions_frame = QWidget()
#         instructions_frame.setStyleSheet("border: 2px solid red;")
#
#         self.instructions_label = QLabel("Instructions:\n\n- Show your hand in the camera frame\n- Gesture recognition will be displayed here")
#         layout = QVBoxLayout(instructions_frame)
#         layout.addWidget(self.instructions_label)
#
#         return instructions_frame
#
#     def update_frame(self, frame):
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = self.hands.process(frame_rgb)
#
#         if results.multi_hand_landmarks:
#             hands, _ = self.detector.findHands(frame)  # with draw
#
#             if len(hands)>1:
#                 if len(hands) == 2:
#                     hand1 = hands[0]
#                     hand2 = hands[1]
#
#                     # Your gesture recognition logic here
#                     # ...
#                     lmList1 = hand1["lmList"]
#                     lmList2 = hand2["lmList"]
#
#                     rList = []
#                     lList = []
#                     # print(lmList1[4][0], " : ", lmList1[20][0])
#                     if (lmList1[4][0] > lmList1[20][0]):
#                         rList = lmList1
#                         lList = lmList2
#                     else:
#                         rList = lmList2
#                         lList = lmList1
#
#                     # Right Hand
#                     rfingers = []
#
#                     # Thumb
#                     if rList[self.tipIds[0]][0] > rList[self.tipIds[1]][0]:
#                         rfingers.append(1)
#                     else:
#                         rfingers.append(0)
#
#                     # 4 Fingers
#                     for id in range(1, 5):
#                         if rList[self.tipIds[id]][1] < rList[self.tipIds[id] - 2][1]:
#                             rfingers.append(1)
#                         else:
#                             rfingers.append(0)
#
#                     # print(fingers)
#                     rdata = rfingers.count(1)
#
#                     # Left Hand
#                     lfingers = []
#
#                     # Thumb
#                     if lList[self.tipIds[0]][0] < lList[self.tipIds[1]][0]:
#                         lfingers.append(1)
#                     else:
#                         lfingers.append(0)
#
#                     # 4 Fingers
#                     for id in range(1, 5):
#                         if lList[self.tipIds[id]][1] < lList[self.tipIds[id] - 2][1]:
#                             lfingers.append(1)
#                         else:
#                             lfingers.append(0)
#
#                     # print(fingers)
#                     ldata = lfingers.count(1)
#                     # print("Left hand : ", ldata, "    Right Hand : ", rdata)
#
#                     # rdata = ...  # Calculate right hand gesture count
#                     # ldata = ...  # Calculate left hand gesture count
#
#                     self.count_label.setText(f"Left hand: {ldata}   Right hand: {rdata}")
#
#
#
#
#         image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)
#         pixmap = QPixmap.fromImage(image)
#         self.webcam_label.setPixmap(pixmap)
#
# class Worker(QThread):
#     frame_update = pyqtSignal(object)
#
#     def run(self):
#         cap = cv2.VideoCapture(0)
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 continue
#
#             self.frame_update.emit(frame)
#             self.msleep(30)  # Update frame every 30 ms
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = GestureRecognitionApp()
#     window.show()
#     sys.exit(app.exec_())
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

