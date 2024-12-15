# **Eye Tracking Cursor Control**

## **Project Overview**
The **Eye Tracking Cursor Control** application allows hands-free computer interaction using eye tracking and blink detection via a standard webcam. This project leverages cutting-edge computer vision and AI technologies to provide accessibility and productivity enhancements.

### **Key Features**
- **Real-Time Cursor Control**: Move the cursor using eye movements.
- **Blink Detection**: Perform mouse actions with:
  - Single blink: Left-click.
  - Double blink: Right-click.
  - Long blink: Drag-and-drop.
- **Multi-Monitor Support**: Seamless tracking across multiple screens.
- **Voice Feedback**: Accessibility feature with audio prompts for key actions.
- **System Tray Integration**: Run in background mode for minimal interference.

---

## **Current Development**

### **Implemented Features**
| Feature                             | Status   | Notes                                                                                 |
|-------------------------------------|----------|---------------------------------------------------------------------------------------|
| Calibration with 3x3 grid           | ✅        | Accurate gaze-to-screen mapping with multi-monitor support.                           |
| Real-time cursor control            | ✅        | Smooth cursor movement using OpenCV and Dlib.                                         |
| Blink detection for left/right-click| ✅        | Single blink (left-click) and double blink (right-click) implemented via Pyautogui.   |
| Long blink for drag-and-drop        | ✅        | Drag-and-drop functionality added with Pyautogui.                                     |
| Multi-monitor support               | ✅        | Detects and calibrates each monitor independently.                                    |
| Voice feedback                      | ✅        | Accessibility option using Pyttsx3 for text-to-speech.                                |
| System tray integration             | ✅        | Runs in the background with menu options for tracking and quitting.                  |

---

### **Remaining Improvements**
| Feature                             | Status   | Notes                                                                                 |
|-------------------------------------|----------|---------------------------------------------------------------------------------------|
| Deep learning-based gaze estimation | ❌        | Implement advanced models for better tracking accuracy (e.g., Gaze360).               |
| Custom gestures for mouse actions   | ❌        | Add scrolling and app-switching triggered by gaze gestures or patterns.               |
| Dynamic calibration                 | ❌        | Enable live calibration updates without restarting the app.                           |
| Cross-platform compatibility        | ❌        | Test and refine compatibility on macOS and Linux.                                     |
| Performance optimization            | ❌        | Further reduce latency, especially on lower-spec devices.                             |
| Edge case improvements              | ❌        | Enhance tracking for users wearing glasses or under variable lighting conditions.     |

---

## **Installation and Startup**

### **Requirements**
#### **Hardware**
- Webcam (720p resolution or higher recommended).
- PC/Laptop with at least:
  - **CPU**: Intel i5 or equivalent.
  - **RAM**: 4GB (minimum).

#### **Software**
- Python 3.8 or higher.

### **Dependencies**
Install the following Python libraries:
```bash
pip install opencv-python dlib pyautogui numpy scipy pyttsx3 keyboard pystray screeninfo pillow
```
Additionally, download the Dlib pre-trained model:
- [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

### **Setup**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/eye-tracking-cursor-control.git
   cd eye-tracking-cursor-control
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place the downloaded Dlib model (`shape_predictor_68_face_landmarks.dat`) in the `models/` directory.

### **Running the Application**
1. Start the application:
   ```bash
   python main.py
   ```
2. Use the GUI or shortcuts to perform actions:
   - **Ctrl+Alt+T**: Start tracking.
   - **Ctrl+Alt+B**: Start blink detection.
   - **Ctrl+Alt+C**: Calibrate.
   - **Ctrl+Alt+S**: Stop tracking.

3. Minimize to the tray for background operation. Use the tray icon menu to manage the application.

---

## **Historical Origins**

This project stands on decades of research, open-source contributions, and advancements in AI. Below is a detailed list of the technologies and resources it builds upon:

### **1. OpenCV (Computer Vision)**
- **Repository**: [OpenCV GitHub](https://github.com/opencv/opencv)
- **Reference Paper**: [OpenCV: Open Source Computer Vision Library](https://ieeexplore.ieee.org/document/9093366)
- **Description**: Core library for face and eye detection.

### **2. Dlib (Facial Landmark Detection)**
- **Repository**: [Dlib GitHub](https://github.com/davisking/dlib)
- **Pre-Trained Model**: [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
- **Reference Paper**: [Dlib Facial Landmark Detection](http://dlib.net/files/face_landmark_detection.py.html)

### **3. Pyautogui (Mouse Automation)**
- **Repository**: [Pyautogui GitHub](https://github.com/asweigart/pyautogui)

### **4. Eye Aspect Ratio (EAR) for Blink Detection**
- **Reference Paper**: [Real-Time Eye Blink Detection Using Facial Landmarks](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)

### **5. Pyttsx3 (Voice Feedback)**
- **Repository**: [Pyttsx3 GitHub](https://github.com/nateshmbhat/pyttsx3)

### **6. Multi-Monitor Management**
- **Library**: [ScreenInfo GitHub](https://github.com/rr-/screeninfo)

### **7. Transformers and Neural Networks**
- **Torch/PyTorch**: [PyTorch GitHub](https://github.com/pytorch/pytorch)
- **TensorFlow**: [TensorFlow GitHub](https://github.com/tensorflow/tensorflow)
- **Reference Paper**: [Attention Is All You Need (Transformers)](https://arxiv.org/abs/1706.03762)

### **8. Foundational Research**
#### **Convolutional Neural Networks**
- **Reference Paper**: [Gradient-Based Learning Applied to Document Recognition (1998)](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)
#### **Transformers**
- **Reference Paper**: [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762)

### **9. Generative AI Influence**
- **Stable Diffusion**: [Stable Diffusion GitHub](https://github.com/CompVis/stable-diffusion)

---

## **Acknowledgments**
This project would not have been possible without the contributions of the open-source community and the foundational research in AI and computer vision. Special thanks to the developers and researchers who made these tools and techniques accessible to everyone.

---
