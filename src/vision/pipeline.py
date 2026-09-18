from pathlib import Path
import cv2
from .models import Detection
from .tracker import TrackStore
from .confidence import classify_confidence
from ..core.repository import save_detection, create_review, add_event

class VisionPipeline:
    def __init__(self, model_path="yolo11n.pt", confidence=0.25, job_id=None):
        self.model_path, self.confidence, self.job_id = model_path, confidence, job_id
        self._model = None

    def _load(self):
        if self._model is None:
            from ultralytics import YOLO
            self._model = YOLO(self.model_path)
        return self._model

    def process(self, video_path, output_path=None, sample_every=1):
        model=self._load()
        capture=cv2.VideoCapture(video_path)
        if not capture.isOpened(): raise FileNotFoundError(video_path)
        fps=capture.get(cv2.CAP_PROP_FPS) or 25.0
        width,height=int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer=None
        if output_path:
            Path(output_path).parent.mkdir(parents=True,exist_ok=True)
            writer=cv2.VideoWriter(output_path,cv2.VideoWriter_fourcc(*"mp4v"),fps,(width,height))
        store=TrackStore(); frame_index=0
        try:
            while True:
                ok,frame=capture.read()
                if not ok: break
                if frame_index % sample_every:
                    frame_index += 1; continue
                results=model.track(frame,persist=True,conf=self.confidence,verbose=False)
                if writer: writer.write(results[0].plot())
                boxes,names=results[0].boxes,results[0].names
                if boxes is not None:
                    for box in boxes:
                        xyxy=box.xyxy[0].tolist(); conf=float(box.conf[0]); cls=int(box.cls[0])
                        track_id=int(box.id[0]) if box.id is not None else None
                        detection=Detection(frame=frame_index,track_id=track_id,label=str(names[cls]),
                                             confidence=conf,bbox=tuple(float(x) for x in xyxy))
                        store.add(detection)
                        detection_id=save_detection(detection,self.job_id)
                        action=classify_confidence(conf)
                        add_event(self.job_id,"detection",{"detection_id":detection_id,"action":action})
                        if action=="human_review": create_review(detection_id,f"confidence={conf:.3f}")
                frame_index += 1
        finally:
            capture.release()
            if writer: writer.release()
        return store.summary()
