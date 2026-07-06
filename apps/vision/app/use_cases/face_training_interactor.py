from __future__ import annotations

import logging

from ultralytics import YOLO
from vision.app.dtos.face_training_dto import TrainFaceRecognizerCommand, TrainFaceRecognizerResult
from vision.app.ports.input.face_training_use_case import FaceTrainingUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort

logger = logging.getLogger(__name__)

_BASE_WEIGHTS = "yolo11n-cls.pt"


class FaceTrainingInteractor(FaceTrainingUseCase):
    def __init__(self, dataset_port: FaceDatasetPort) -> None:
        self.dataset_port = dataset_port

    def train(self, command: TrainFaceRecognizerCommand) -> TrainFaceRecognizerResult:
        dataset_root = self.dataset_port.get_dataset_root_path()

        model = YOLO(_BASE_WEIGHTS)
        model.train(
            data=dataset_root,
            epochs=command.epochs,
            batch=command.batch_size,
            imgsz=command.image_size,
        )
        weights_path = str(model.trainer.best)

        logger.info(
            "[FaceTrainingInteractor] train epochs=%s weights_path=%s",
            command.epochs,
            weights_path,
        )
        return TrainFaceRecognizerResult(
            ok=True, weights_path=weights_path, epochs=command.epochs
        )
