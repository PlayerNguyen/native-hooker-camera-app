import threading
from deepface import DeepFace
import logging
import time
from database import FaceMemberDatabase


class Representer:
    def __init__(
        self,
        recognition: str,
        detector: str,
        delay: int,
        recognition_level: float,
    ) -> None:
        self.logger = logging.getLogger("Representer")
        self.frame = None
        self.faces = []
        self.recognition = recognition
        self.detector = detector
        self.delay = delay
        self.database = FaceMemberDatabase()
        self.recognition_level = recognition_level
        self.search_output = []
        pass

    def __load_models__(self):
        self.logger.info(f"Loading models into a memory")
        DeepFace.build_model(self.detector, "face_detector")
        DeepFace.build_model(self.recognition)

    def start(self):
        # Start build a model
        self.__load_models__()
        # Then start a thread
        self.logger.info(f"Spawning a new thread for inference")
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def update(self):
        while True:
            # If frame is none, skip it
            if self.frame is None:
                # print("Skip face recognition since frame is not available")
                continue

            # Perform face recognition and update the frame with the result
            faces = DeepFace.represent(
                self.frame,
                detector_backend=self.detector,
                model_name=self.recognition,
                enforce_detection=False,
                # expand_percentage=10,
                normalization="Facenet",
            )

            self.faces = list(filter(lambda face: face["face_confidence"] != 0, faces))
            self.logger.info(f"Accept {len(self.faces)} faces")

            # Turn faces list into embedding list
            embeddings = list(map(lambda face: face["embedding"], self.faces))
            # self.logger.debug(f"Embeddings: {embeddings}")
            if len(embeddings) == 0:
                self.search_output = []
                continue

            results = self.database.search(
                data=embeddings,
                output_fields=["name", "id"],
                search_params={
                    "params": {
                        "radius": self.recognition_level,
                    }
                },
            )
            self.search_output = results
            self.logger.debug(results)
            time.sleep(self.delay)

    def set_frame(self, frame):
        self.frame = frame

    def get_faces(self):
        return self.faces
