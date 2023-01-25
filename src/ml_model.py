import os
from typing import List, Union

import torch
from diffusers import StableDiffusionInpaintPipeline
from loguru import logger
from PIL import Image
from torch import autocast

from config import model_settings
from schemas import ImageGenerationRequest
from utils import download_image_from_storage


class InpaintModel:
    def __init__(self):
        self.inpaint_pipeline = Union[StableDiffusionInpaintPipeline, None] = None
        os.makedirs(model_settings.model_output_path, exist_ok=True)

    def load_model(self) -> None:
        if self.inpaint_pipeline is not None:
            return
        if torch.cuda.is_available():
            self.inpaint_pipeline = StableDiffusionInpaintPipeline.from_pretrained(
                model_settings.model_name_or_path,
                torch_dtype=torch.float16,
            )
        else:
            logger.error("CPU Mode is not Supported")
            exit(1)

    def generate(self, task_id: str, data: ImageGenerationRequest) -> None:
        if self.inpaint_pipeline is None:
            raise Exception("Model is not loaded completely.")

        generator = torch.cuda.manual_seed(data.seed)
        image = download_image_from_storage(task_id, "image.png")
        mask_image = download_image_from_storage(task_id, "mask_image.png")
        with torch.inference_mode():
            with autocast("cuda"):
                images: List[Image.Image] = self.diffusion_pipeline(
                    prompt=data.prompt,
                    image=image,
                    mask_image=mask_image,
                    guidance_scale=data.guidance_scale,
                    generator=generator,
                    num_images_per_prompt=data.num_images_per_prompt,
                ).images
        output_path = os.path.join(model_settings.model_output_path, task_id)
        os.makedirs(output_path, exist_ok=True)
        for idx, image in enumerate(images):
            image.save(os.path.join(output_path, f"{idx}.png"))
