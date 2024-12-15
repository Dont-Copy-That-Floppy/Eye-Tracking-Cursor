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

| Feature                              | Status | Notes                                                                               |
| ------------------------------------ | ------ | ----------------------------------------------------------------------------------- |
| Calibration with 3x3 grid            | ✅     | Accurate gaze-to-screen mapping with multi-monitor support.                         |
| Real-time cursor control             | ✅     | Smooth cursor movement using OpenCV and Dlib.                                       |
| Blink detection for left/right-click | ✅     | Single blink (left-click) and double blink (right-click) implemented via Pyautogui. |
| Long blink for drag-and-drop         | ✅     | Drag-and-drop functionality added with Pyautogui.                                   |
| Multi-monitor support                | ✅     | Detects and calibrates each monitor independently.                                  |
| Voice feedback                       | ✅     | Accessibility option using Pyttsx3 for text-to-speech.                              |
| System tray integration              | ✅     | Runs in the background with menu options for tracking and quitting.                 |

---

### **Remaining Improvements**

| Feature                             | Status | Notes                                                                             |
| ----------------------------------- | ------ | --------------------------------------------------------------------------------- |
| Deep learning-based gaze estimation | ❌     | Implement advanced models for better tracking accuracy (e.g., Gaze360).           |
| Custom gestures for mouse actions   | ❌     | Add scrolling and app-switching triggered by gaze gestures or patterns.           |
| Dynamic calibration                 | ❌     | Enable live calibration updates without restarting the app.                       |
| Cross-platform compatibility        | ❌     | Test and refine compatibility on macOS and Linux.                                 |
| Performance optimization            | ❌     | Further reduce latency, especially on lower-spec devices.                         |
| Edge case improvements              | ❌     | Enhance tracking for users wearing glasses or under variable lighting conditions. |

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

**Steps to Set Up the Model**:

1. **Download**:

   - ~~[shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)~~ _(Deprecated: Use the updated model below for better performance)_
   - [Click here to download `shape_predictor_5_face_landmarks.dat`](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2)

2. **Unpack the File**:

   - On Linux/macOS:
     ```bash
     bzip2 -d shape_predictor_5_face_landmarks.dat.bz2
     ```
   - On Windows:
     - Use an extraction tool like **7-Zip** or **WinRAR** to unpack the `.bz2` file and extract the `.dat` file.

3. **Move the File**:
   - Place the extracted `.dat` file into the `models/` directory of your project:

---

### **Setup**

1. Clone this repository:
   ```bash
   git clone https://github.com/Dont-Copy-That-Floppy/Eye-Tracking-Cursor.git
   cd Eye-Tracking-Cursor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place the downloaded Dlib model (`shape_predictor_5_face_landmarks.dat`) in the `models/` directory.

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

## **Running Tests**

### **Unit Testing**

This project includes comprehensive unit tests for all major modules. The tests ensure that the calibration, eye tracking, blink detection, and accessibility features work as intended.

### **How to Run Tests**

1. Navigate to the root directory of the project.
2. Run the following command to discover and execute all tests in the `tests/` directory:

   ```bash
   python -m unittest discover tests
   ```

3. If all tests pass, you will see an output similar to this:

   ```
   ----------------------------------------------------------------------
   Ran 4 tests in 0.123s

   OK
   ```

### **Run Specific Tests**

To run a specific test file (e.g., `test_calibration.py`), use:

```bash
python -m unittest tests.test_calibration
```

### **Test Coverage**

To ensure all modules are thoroughly tested, consider using a test coverage tool like `coverage.py`:

1. Install `coverage.py`:
   ```bash
   pip install coverage
   ```
2. Run the tests with coverage tracking:
   ```bash
   coverage run -m unittest discover tests
   ```
3. Generate a coverage report:
   ```bash
   coverage report
   ```

---

## **Historical Origins**

This project is built on a foundation of open-source tools and research contributions. Below is a list of the key projects and their original authors:

| **Project Name**                   | **Authors**        | **Original Source**                                                      |
| ---------------------------------- | ------------------ | ------------------------------------------------------------------------ |
| **OpenCV**                         | Intel Research     | [GitHub](https://github.com/opencv/opencv)                               |
| **Dlib**                           | Davis E. King      | [GitHub](https://github.com/davisking/dlib)                              |
| **Pyautogui**                      | Al Sweigart        | [GitHub](https://github.com/asweigart/pyautogui)                         |
| **Eye Aspect Ratio (EAR)**         | Soukupová & Čech   | [Paper](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)  |
| **Pyttsx3**                        | Natesh M. Bhat     | [GitHub](https://github.com/nateshmbhat/pyttsx3)                         |
| **ScreenInfo**                     | Rafael Reis        | [GitHub](https://github.com/rr-/screeninfo)                              |
| **Torch and PyTorch**              | Adam Paszke et al. | [GitHub](https://github.com/pytorch/pytorch)                             |
| **TensorFlow**                     | Google Brain Team  | [GitHub](https://github.com/tensorflow/tensorflow)                       |
| **Transformers**                   | Hugging Face       | [GitHub](https://github.com/huggingface/transformers)                    |
| **Dlib 68-point Facial Landmarks** | Davis E. King      | [Model](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) |
| **Dlib 5-point Facial Landmarks**  | Davis E. King      | [Model](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2)  |

---
