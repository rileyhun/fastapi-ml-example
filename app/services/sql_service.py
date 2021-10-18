from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.models import PredictionMetrics
from app.core.errors import CustomException
from loguru import logger
from fastapi import status
import json
import rollbar

async def get_cached_response(
        session: AsyncSession,
        content_identifier: str,
        version: str,
):
    try:
        query_result = await session.execute(select(PredictionMetrics).filter_by(content_identifier=content_identifier,
                                                                           version=version).limit(1))
        response = query_result.scalars().first()
    except:
        await session.rollback()
        raise

    if response and response.response_json:
        try:
            return json.loads(response.response_json)
        except Exception as e:
            rollbar.report_message(str(e))
            logger.error(str(e))
    return None

async def add_model_metrics(
        session: AsyncSession,
        job_id: str,
        content_identifier: str,
        version: str,
        model_predict: float,
        model_proba: float,
        request_json: str,
        response_json: str
):
    metrics = PredictionMetrics(
        job_id=job_id,
        content_identifier=content_identifier,
        version=version,
        model_predict=model_predict,
        model_proba=model_proba,
        request_json=request_json,
        response_json=response_json
    )

    session.add(metrics)

    try:
        await session.flush()
        await session.commit()
    except IntegrityError as e:
        logger.info(f'Duplicate: Document {content_identifier} already stored')
        await session.rollback()
    except Exception as e:
        print(str(e))
        await session.rollback()
        raise CustomException(msg='Error persisting model metrics to database',
                              code='422',
                              status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)