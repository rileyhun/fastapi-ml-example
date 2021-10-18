from app.core.config import settings
from app.core.errors import CustomException, ModelLoadException
from app.models.schemas import Prediction, Features, feature_names
import joblib
from fastapi import status
from loguru import logger
import rollbar
import os
import numpy as np

class MachineLearningModelHandlerScore(object):
    def __init__(self) -> None:
        self._load_model()

    def _load_model(self) -> None:
        if not os.path.exists(settings.REMOTE_MODEL_NAME):
            message = f"ML model at {settings.REMOTE_MODEL_NAME} doesn't exist"
            logger.error(message)
            rollbar.report_message(f"FileNotFoundError: {message}")
            raise FileNotFoundError(message)
        logger.info(f"load model in {settings.REMOTE_MODEL_NAME}")
        self.model = joblib.load(settings.REMOTE_MODEL_NAME)
        if not self.model:
            message = f"Model could not load!"
            logger.error(message)
            rollbar.report_message(f"ModelLoadException: {message}")
            raise ModelLoadException(message)
        logger.info("initialized model")

    def predict(self, input: Features, method="predict_proba"):
        if input is None:
            msg = "{} is not a valid payload"
            raise CustomException(msg=msg,
                                  code='400',
                                  status_code=status.HTTP_400_BAD_REQUEST)
        if hasattr(self.model, method):
            logger.debug('Starting model prediction')
            sample_dict = input.dict(by_alias=True)
            features = np.array([sample_dict[f] for f in feature_names]).reshape(1, -1)
            pred_proba = self.model.predict_proba(features)[0]
            label = np.argmax(pred_proba)
            prediction_response = Prediction(label=label, confidence=pred_proba[label])
            logger.debug('Completed model prediction')
            return prediction_response
        msg = f"Unable to make prediction - {method}' attribute is missing"
        logger.error(msg)
        rollbar.report_message(f"PredictionError: {msg}")
        raise CustomException(msg=msg,
                              code='423',
                              status_code=status.HTTP_423_LOCKED)