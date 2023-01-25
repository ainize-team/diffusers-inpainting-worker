from functools import partialmethod
from typing import Dict

from celery.signals import celeryd_init
from loguru import logger
from tqdm import tqdm

from enums import ErrorStatusEnum, ResponseStatusEnum
from ml_model import InpaintModel
from schemas import Error, InpaintRequest, InpaintResponse
from utils import clear_memory, get_now_timestamp, update_response, upload_output_images
from worker import app


inpaint_model = InpaintModel()


@celeryd_init.connect
def load_model(**kwargs):
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
    logger.info("Start loading model...")
    inpaint_model.load_model()
    logger.info("Loading model is done!")


@app.task(name="inpaint")
def inpaint(task_id: str, data: Dict) -> str:
    response = InpaintResponse(status=ResponseStatusEnum.ASSIGNED, updated_at=get_now_timestamp())
    update_response(task_id, response)
    try:
        user_request: InpaintRequest = InpaintRequest(**data)
        inpaint_model.inpaint(task_id, user_request)
        response.seed = user_request.seed
        response.response = upload_output_images(task_id, user_request.num_images_per_prompt)
        response.status = ResponseStatusEnum.COMPLETED
        response.updated_at = get_now_timestamp()
        update_response(task_id, response)
        logger.info(f"task_id: {task_id} is done")
    except ValueError as e:
        error = Error(status_code=ErrorStatusEnum.UNPROCESSABLE_ENTITY, error_message=str(e))
        error_response = InpaintResponse(status=ResponseStatusEnum.ERROR, error=error, updated_at=get_now_timestamp())
        update_response(task_id, error_response)
    except Exception as e:
        error = Error(status_code=ErrorStatusEnum.INTERNAL_SERVER_ERROR, error_message=str(e))
        error_response = InpaintResponse(status=ResponseStatusEnum.ERROR, error=error, updated_at=get_now_timestamp())
        update_response(task_id, error_response)
    finally:
        clear_memory()
