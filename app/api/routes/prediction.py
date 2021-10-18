from fastapi import APIRouter, Response, Depends, status
from starlette.requests import Request
from app.services.predict import MachineLearningModelHandlerScore
from app.models.schemas import Features
from app.core.security import check_authentication_header
from app.core.errors import CustomException
import uuid

router = APIRouter()

@router.post("/predict", name="predict")
async def predict(
    request: Request,
    response: Response,
    input: Features = None,
    authenticated: bool = Depends(check_authentication_header),
):
    if not input:
        raise CustomException(msg='No input provided to model',
                              code='400',
                              status_code=status.HTTP_400_BAD_REQUEST)

    job_id = str(uuid.uuid4())

    try:
        request.app.logger.info("loading ml model from state")
        model: MachineLearningModelHandlerScore = request.app.state.model
    except AttributeError:
        request.app.logger.info("loading ml model from remote s3 bucket")
        model = MachineLearningModelHandlerScore()

    request.app.logger.info("run prediction...")
    prediction = model.predict(input)

    response.headers['X-model-proba'] = "%.2f" % prediction.confidence
    response.headers['X-model-predict'] = str(prediction.label)
    request.app.logger.info(f"{job_id}:{prediction}")
    return prediction