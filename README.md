# GestureMaster - Hand Gesture Recognition App

GestureMagic is an interactive Python application that uses computer vision and machine learning to recognize hand gestures and perform actions based on those gestures.

## Features

- Real-time hand gesture recognition using the power of OpenCV, Mediapipe, and PyQt.
- Recognizes a variety of hand gestures, including finger counting.
- Easy-to-use graphical user interface (GUI) for a user-friendly experience.
- Intuitive instructions to guide users on performing recognized gestures.
- Customizable gestures and actions for enhanced usability.

## Getting Started

### Dependencies

To run GestureMagic, you need the following dependencies:

- PyQt5
- OpenCV
- Mediapipe
- cvzone

### Installing Dependencies

You can install the required dependencies using `pip`:

```bash
pip install PyQt5 opencv-python mediapipe
```

### Running the Application
Clone the repository to your local machine:
```bash

Change into the project directory::
```bash
cd Gesture-Master
```

Run the application using Python:
```bash
python main.py
```


## Instructions

- Launch the application and position both hands within the frame.
- The app recognizes gestures in real-time, displaying the count of visible fingers on each hand.
- Follow the on-screen instructions to perform recognized gestures.
- Experiment with different hand poses to explore the range of gestures supported.

## Types of Gestures Recognized
- Zero Fingers: No fingers visible.
- One Finger: First finger visible (excluding thumb).
- Two Fingers: First two fingers visible (excluding thumb).
- Three Fingers: First three fingers visible (excluding thumb).
- Four Fingers: First four fingers visible (excluding thumb).
- Five Fingers: All fingers, including the thumb, visible.

