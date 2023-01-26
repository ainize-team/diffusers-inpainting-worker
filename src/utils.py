import datetime
import gc
import os
import shutil
from io import BytesIO
from typing import Dict

import requests
import torch
from firebase_admin import db, storage
from PIL import Image
from pydantic import HttpUrl

from config import firebase_settings, model_settings
from schemas import InpaintResponse


app_name = firebase_settings.app_name


def download_image(url: HttpUrl) -> Image.Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGB")


def upload_output_images(task_id: str, num_images_per_prompt: int) -> Dict[str, HttpUrl]:
    bucket = storage.bucket()
    output_path = os.path.join(model_settings.model_output_path, task_id)
    result = {}
    for idx in range(num_images_per_prompt):
        image_path = os.path.join(output_path, f"{idx}.png")
        blob = bucket.blob(f"{app_name}/results/{task_id}/{idx}.png")
        blob.upload_from_filename(image_path)
        blob.make_public()
        url = blob.public_url
        result[str(idx)] = url
    shutil.rmtree(output_path, ignore_errors=True)
    return result


def update_response(task_id: str, response: InpaintResponse):
    db.reference(f"{app_name}/tasks/{task_id}").update(response.dict())


def clear_memory() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def get_now_timestamp() -> int:
    return int(datetime.utcnow().timestamp() * 1000)
