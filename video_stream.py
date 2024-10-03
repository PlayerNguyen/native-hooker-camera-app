import cv2
from threading import Thread
import logging


class VideoStream:
    def __init__(self, video_source: str) -> None:
        try:
            self.video_source = int(video_source)
        except ValueError:
            self.video_source = video_source

        self.video_capture = cv2.VideoCapture(self.video_source)
        self.stopped = False
        self.grabbed = False
        self.frame = None
        self.logger = logging.getLogger("video_stream")

    def start(self):
        # Spawn a new thread
        self.logger.debug(f"Starting video stream in new thread, deamon = true")
        self.thread = Thread(target=self._update, args=())
        self.thread.setName("video_stream_thread")
        self.thread.daemon = True
        self.logger.debug(
            f"Thread started, name: {self.thread.name}, ident: {self.thread.ident}"
        )
        self.thread.start()

        return self

    def _update(self):
        while True:
            # If we stop
            if self.stopped:
                break

            # Read the next frame from the video
            ret, frame = self.video_capture.read()

            self.frame = frame
            self.grabbed = ret

    def read(self):
        return self.frame

    def has_grabbed(self):
        return self.grabbed

    def stop(self):
        self.stopped = True
        self.video_capture.release()
        self.logger.debug(
            f"Stopped video stream, is_thread_alive: {self.thread.is_alive()}"
        )
