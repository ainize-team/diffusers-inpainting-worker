import gc
import os
import shutil
from typing import Dict

import torch
from firebase_admin import db, storage
from PIL import Image
from pydantic import HttpUrl

from config import firebase_settings, model_settings
from schemas import ImageGenerationResponse


app_name = firebase_settings.firebase_app_name


def download_image_from_storage(task_id: str, filename: str) -> Image.Image:
    bucket = storage.bucket()
    blob = bucket.blob(f"{app_name}/results/{task_id}/{filename}")
    image_path = f"{task_id}/{filename}"
    os.makedirs(task_id, exist_ok=True)

    blob.download_to_filename(image_path)

    return Image.open(image_path).convert("RGB")


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


def update_response(task_id: str, response: ImageGenerationResponse):
    db.reference(f"{app_name}/tasks/{task_id}").update(response.dict())


def clear_memory() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
