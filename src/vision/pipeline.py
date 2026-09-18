from pathlib import Path
import cv2

from .models import Detection
from .tracker import TrackStore

class VisionPipeline:
    def __init__(self, model_path: str = "yolo11n.pt", confidence: float = 0.25):
        self.model_path = model_path
        self.confidence = confidence
        self._model = None

    def _load(self):
        if self._model is None:
            from ultralytics import YOLO
            self._model = YOLO(self.model_path)
        return self._model

    def process(self, video_path: str, output_path: str | None = None, sample_every: int = 1):
        model = self._load()
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            raise FileNotFoundError(video_path)

        fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = None
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            writer = cv2.VideoWriter(
                output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
            )

        store = TrackStore()
        frame_index = 0
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame_index % sample_every:
                frame_index += 1
                continue

            results = model.track(frame, persist=True, conf=self.confidence, verbose=False)
            annotated = results[0].plot()
            if writer:
                writer.write(annotated)

            boxes = results[0].boxes
            names = results[0].names
            if boxes is not None:
                for i, box in enumerate(boxes):
                    xyxy = box.xyxy[0].tolist()
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    track_id = int(box.id[0]) if box.id is not None else None
                    store.add(Detection(
                        frame=frame_index,
                        track_id=track_id,
                        label=str(names[cls]),
                        confidence=conf,
                        bbox=tuple(float(x) for x in xyxy),
                    ))
            frame_index += 1

        capture.release()
        if writer:
            writer.release()
        return store.summary()
