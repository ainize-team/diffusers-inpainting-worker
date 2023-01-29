from typing import Dict, Optional

from pydantic import BaseModel, Field, HttpUrl

from enums import ResponseStatusEnum


class InpaintRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="Your prompt (what you want to add in place of what you are removing)",
    )
    image_url: HttpUrl
    mask_image_url: HttpUrl
    seed: int = Field(default=42, ge=0, le=4294967295)
    num_images_per_prompt: int = Field(2, ge=1, le=4, description="How many images you wish to generate")
    guidance_scale: float = Field(7.5, ge=0, le=50, description="how much the prompt will influence the results")


class Error(BaseModel):
    status_code: int
    error_message: str


class InpaintResponse(BaseModel):
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    response: Optional[Dict[str, HttpUrl]]
    seed: int = 42
    error: Optional[Error]
    updated_at: int = 0
