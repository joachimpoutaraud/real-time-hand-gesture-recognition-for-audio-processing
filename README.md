# Real-Time Hand Gesture Recognition for Audio Processing

This program is based on three main Python libraries 

- [OpenCV](https://pypi.org/project/opencv-python/) for video processing 
- [Mediapipe](https://pypi.org/project/mediapipe/) to build world-class ML solutions and applications 
- [Open Sound Control](https://pypi.org/project/python-osc/) for server and client implementations 

This uses [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands) as a high-fidelity hand and finger tracking solution based on machine learning (ML) to infer 21 3D landmarks of a hand from just a single frame. That way, the user can use the webcam's computer and the index finger to process audio data. Moreover, using [Open Sound Control](https://pypi.org/project/python-osc/), it possible to send UDP packets from Python to Pure Data. That way, the hand gestures are used as controller for multi-parameter audio effects (pitch, reverb, delay and modulation).

<p align="center">
  <img src="https://raw.githubusercontent.com/joachimpoutaraud/real-time-hand-gesture-recognition-for-audio-processing/main/webcam.jpg" width="500" title="Real-Time Hand Gesture Recognition with the computer's webcam">
</p>

## Prerequisites

- opencv
- mediapipe
- python-osc





