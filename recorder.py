import logging
import cv2
import time
import os

DATA_DIRECTORY = os.path.join("data")


class Recorder:
    def __init__(self, video_capturer: cv2.VideoCapture):
        self.capturer = video_capturer
        self.frame_rate = int(self.capturer.get(cv2.CAP_PROP_FPS))
        self.width = int(self.capturer.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capturer.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.logger = logging.getLogger("Recorder")
        self.recording = False
        self.metadata_writer = None

        # Ensure the data directory
        self.__ensure_dir__(DATA_DIRECTORY)

    def __ensure_dir__(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def start_recording(self):
        if self.recording:
            raise ValueError("Cannot start recording, already recording")

        current_timestamp = int(time.time() * 1000)
        current_dirname = os.path.join(DATA_DIRECTORY, str(current_timestamp))
        self.__ensure_dir__(current_dirname)
        current_pathname = os.path.join(current_dirname, "main.mp4")
        self.video_writer = cv2.VideoWriter(
            current_pathname,
            fourcc=cv2.VideoWriter.fourcc("X", "2", "6", "4"),
            fps=self.frame_rate,
            frameSize=(self.width, self.height),
        )
        current_metadata_pathname = os.path.join(current_dirname, "metadata.txt")
        self.metadata_writer = open(current_metadata_pathname, "a+")
        self.recording = True

    def write(self, image: cv2.typing.MatLike):
        if not self.recording:
            raise ValueError("Cannot write to video, not recording")

        self.video_writer.write(image)

    def write_metadata(self, line: str):
        if not self.recording:
            raise ValueError("Cannot write metadata, not recording")
        self.metadata_writer.write(line + "\n")
        self.metadata_writer.flush()

    def stop_recording(self):
        self.recording = False
        self.video_writer.release()
        self.metadata_writer.close()
        self.logger.info(f"Stopped the recorder.")

    def is_recording(self) -> bool:
        return self.recording
