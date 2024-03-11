import time, threading, pyautogui, cv2, numpy, os
from moviepy.editor import AudioFileClip, VideoFileClip
import soundcard
import soundfile

class ScreenRecorder():
    def __init__(self, 
                file_name=time.strftime("%Y-%m-%d_%H-%M-%S"),
                sample_rate=44100,
                channels=2,
                include_audio=True) -> None:

        self._prefix = file_name
        self._sample_rate = sample_rate
        self._channels = channels
        self._recording = False
        self._include_audio = include_audio
        self._screen_width, self._screen_height = pyautogui.size()
        self._fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self._out = None
        self._num_frames = 0

    def start_recording(self):
        if not os.path.exists("./recordings/"):
            os.makedirs("./recordings/")
        self._recording = True
        if self._include_audio:
            t = threading.Thread(target=self._audio_thread)
            t.start()
        self._out = cv2.VideoWriter(f"./recordings/{self._prefix}.avi", self._fourcc, 30.0, (self._screen_width, self._screen_height))
        t = threading.Thread(target=self._video_thread)
        t.start()
        self._start_time = time.time()

    def stop_recording(self):
        self._recording = False
        self._out.release()
        self._save_video()

    def _video_thread(self):
        while self._recording:
           screenshot = pyautogui.screenshot()
           frame = numpy.array(screenshot)
           frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
           self._out.write(frame)
           self._num_frames += 1

    def _audio_thread(self):
        with soundcard.get_microphone(
            id=str(soundcard.default_speaker().name),
            include_loopback=True).recorder(
                samplerate=self._sample_rate,
                channels=self._channels) as mic:
            
            while self._recording:
                try:
                    buffer, samp = soundfile.read(f"./recordings/{self._prefix}.wav")
                except:
                    buffer = []
                data = mic.record(numframes=self._sample_rate)
                buffer = list(buffer)
                buffer += list(data)
                soundfile.write(file=f"./recordings/{self._prefix}.wav", data=buffer, samplerate=self._sample_rate)
    
    def _save_video(self):
        video_clip = VideoFileClip(f"./recordings/{self._prefix}.avi")
        audio_clip = AudioFileClip(f"./recordings/{self._prefix}.wav")
        actual_frame_rate = self._num_frames / (time.time() - self._start_time)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip = final_clip.set_duration(audio_clip.duration)  
        final_clip = final_clip.set_fps(actual_frame_rate)
        final_clip.write_videofile(f"./recordings/{self._prefix}.mp4", codec="libx264")
