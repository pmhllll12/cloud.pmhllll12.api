from __future__ import annotations

from vision.adapter.outbound.local_face_dataset_adapter import LocalFaceDatasetAdapter
from vision.app.ports.input.face_training_use_case import FaceTrainingUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.use_cases.face_training_interactor import FaceTrainingInteractor


def get_face_dataset_port() -> FaceDatasetPort:
    return LocalFaceDatasetAdapter()


def get_face_training_use_case() -> FaceTrainingUseCase:
    return FaceTrainingInteractor(dataset_port=get_face_dataset_port())
