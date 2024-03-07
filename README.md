# ScreenRecorder.py

A simple python3 module to record the screen with desktop audio

--------------------------------------------------------------------

**Requirements**

*You can install the dependencies by running:*

```console
python3 -m pip install -r requirements.txt
```

--------------------------------------------------------------------

**Usage**

*A simple usage case*

```python
import screenrecorder as s

sc = s.ScreenRecorder()
sc.start_recording()

# do some stuff or set a timeout to record until the end of the timeout

sc.stop_recording() # this is needed to stop the recording and process audio and video into a file.mp4

```
