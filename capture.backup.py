# import typing
# import cv2
# from recorder import Recorder
# import logging
# from deepface import DeepFace
# import json


# class Capture:
#     def __init__(
#         self,
#         video_source: str,
#         factor: float,
#         detector: str,
#         recognition: str,
#         stride: int,
#         hide_preview: bool,
#     ):
#         self.factor = factor
#         self.detector = detector
#         self.recognition = recognition
#         self.stride = stride
#         self.hide_preview = hide_preview
#         self.logger = logging.getLogger("Capture")

#         # Convert video source to integer if possible
#         try:
#             self.video_source = int(video_source)
#         except ValueError:
#             self.video_source = video_source

#             # Initialize the video capture
#         self.logger.info(
#             f"Start open video streaming from video source {self.video_source}"
#         )
#         self.capture = cv2.VideoCapture(self.video_source)
#         self.recorder = Recorder(self.capture)

#     def start_application(self):
#         try:

#             # Internal event variables
#             current_frame = 0
#             captured_faces: typing.List = []
#             previous_face_count = 0
#             current_captured_frame_count = 0

#             while True:

#                 # Read the next frame from the video
#                 ret, frame = self.capture.read()
#                 current_frame += 1

#                 # If the frame is not available, break the loop
#                 if not ret:
#                     break

#                 if self.recorder.is_recording():
#                     self.recorder.write(frame)

#                 # Resize the frame
#                 frame = cv2.resize(frame, (0, 0), fx=self.factor, fy=self.factor)

#                 if current_frame >= self.stride:
#                     # Reset current frame variable before inference
#                     current_frame = 0

#                     # Perform object detection and recognition
#                     faces = DeepFace.represent(
#                         frame,
#                         detector_backend=self.detector,
#                         model_name=self.recognition,
#                         enforce_detection=False,
#                         expand_percentage=5,
#                     )
#                     # print(faces)
#                     captured_faces = list(
#                         filter(lambda face: face["face_confidence"] != 0, faces)
#                     )

#                     current_face_count = len(captured_faces)
#                     if previous_face_count == 0 and current_face_count > 0:
#                         self.logger.info("Start a new record session")
#                         self.recorder.start_recording()
#                         current_captured_frame_count = 0

#                     if previous_face_count != 0 and current_face_count == 0:
#                         self.logger.info("Stop the current record session")
#                         self.recorder.stop_recording()

#                     previous_face_count = current_face_count

#                     for index, face in enumerate(captured_faces):
#                         # Turns dict[x, y, w, h] into tuple with 4 elements
#                         area = face["facial_area"]
#                         self.logger.debug(f"Face {index+1}: {area}")

#                 # Display bounding box
#                 for index, face in enumerate(captured_faces):
#                     # Turns dict[x, y, w, h] into tuple with 4 elements
#                     area = face["facial_area"]
#                     x, y, w, h = (area["x"], area["y"], area["w"], area["h"])
#                     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)

#                 if self.recorder.is_recording():
#                     current_captured_frame_count += 1
#                     self.recorder.write_metadata(f"{current_captured_frame_count} -")

#                 # Display the results
#                 if not self.hide_preview:
#                     cv2.imshow("Stream preview", frame)

#                 if cv2.waitKey(1) & 0xFF == ord("q"):
#                     break
#         except KeyboardInterrupt:
#             self.logger.info("Capture interrupted by user")
#         finally:
#             if self.recorder.is_recording():
#                 self.recorder.stop_recording()

#             self.capture.release()
#             cv2.destroyAllWindows()
#             self.logger.info("Capture stopped")
