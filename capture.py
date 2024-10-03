import typing
import cv2
from recorder import Recorder
import logging
from deepface import DeepFace
import json
import imutils
from representer import Representer
from video_stream import VideoStream


class Capture:
    def __init__(
        self,
        video_source: str,
        width: int,
        detector: str,
        recognition: str,
        delay: int,
        hide_preview: bool,
        recognition_level: float,
    ):
        self.width = width
        self.detector = detector
        self.recognition = recognition
        self.delay = delay
        self.hide_preview = hide_preview
        self.logger = logging.getLogger("Capture")
        self.recognition_level = recognition_level

        # Convert video source to integer if possible
        try:
            self.video_source = int(video_source)
        except ValueError:
            self.video_source = video_source

            # Initialize the video capture
        self.logger.info(
            f"Start open video streaming from video source {self.video_source}"
        )
        self.representer = Representer(
            recognition=self.recognition,
            detector=self.detector,
            delay=self.delay,
            recognition_level=self.recognition_level,
        )
        self.stream = VideoStream(video_source=self.video_source)
        self.stream.start()

    def start_application(self):
        self.representer = self.representer.start()
        try:

            while True:
                frame = self.stream.read()
                frame = imutils.resize(frame, width=self.width)

                # Perform object detection and recognition
                self.representer.set_frame(frame)

                # Draw faces if available
                faces = self.representer.get_faces()

                # Display the results if enabled
                if not self.hide_preview and frame is not None:

                    # Display bounding box
                    for idx, face in enumerate(faces):
                        area = face["facial_area"]
                        (x, y, w, h) = [area["x"], area["y"], area["w"], area["h"]]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

                        if len(self.representer.search_output) > 0:
                            # current search output represents a list of possibly members
                            current_search_output = self.representer.search_output[idx]
                            if len(current_search_output) == 0:
                                cv2.putText(
                                    frame,
                                    "Unknown",
                                    (x, (y - 10)),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,
                                    (0, 0, 255),
                                    2,
                                )
                            # put text for all possible members
                            for idx, result in enumerate(current_search_output):
                                name = result["entity"]["name"]
                                # id = result["entity"]["id"]
                                distance = result["distance"]
                                # print(f"{id}\t{name}\t{distance}")
                                cv2.putText(
                                    frame,
                                    f"{name} {distance:.2f}",
                                    (x, (y - 16) + ((16 * idx))),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.7,
                                    (255, 255, 255),
                                    2,
                                )

                    cv2.imshow("Stream preview", frame)

                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break
        except KeyboardInterrupt:
            self.logger.info("Capture interrupted by user")
        finally:

            self.stream.stop()
            cv2.destroyAllWindows()
            self.logger.info("Capture stopped")
