# Real-Time Hand Gesture Recognition for Audio Processing

This program uses the programming language Python for video processing and hand gesture recognition as well as the visual programming environment [Pure Data](https://puredata.info/) for audio processing. This is based on three main Python libraries: 

- [OpenCV](https://pypi.org/project/opencv-python/) for video processing 
- [Mediapipe](https://pypi.org/project/mediapipe/) to build world-class ML solutions and applications 
- [Open Sound Control](https://pypi.org/project/python-osc/) for server and client implementations 

This uses [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands) as a high-fidelity hand and finger tracking solution based on machine learning (ML) to infer 21 3D landmarks of a hand from just a single frame. That way, the user can use the webcam's computer and the index finger to process audio data. Moreover, using [Open Sound Control](https://pypi.org/project/python-osc/), it possible to send UDP packets from Python to Pure Data. That way, the hand gestures are used as controller for multi-parameter audio effects (pitch, reverb, delay and modulation).

<p align="center">
  <img src="https://raw.githubusercontent.com/joachimpoutaraud/real-time-hand-gesture-recognition-for-audio-processing/main/webcam.jpg" width="500" title="Real-Time Hand Gesture Recognition with the computer's webcam"></p>

## Prerequisites

- opencv-python
- mediapipe
- python-osc

(see requirements.txt. Install with `pip install -r requirements.txt`)

## Installation

Download [Anaconda](https://www.anaconda.com/products/distribution) and prepare your environment using the command line

```
conda create --name webcam
conda activate webcam
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraires

```
conda install -c anaconda pip
pip install -r requirements.txt
``` 
## Usage

Download and install [Pure Data](https://puredata.info/downloads) on your computer and download the repository. 
Open a terminal in the repository folder and run the following command line.

```
python gesture_recognition.py
```




