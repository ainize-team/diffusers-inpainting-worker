from pydantic import BaseSettings


class CeleryWorkerSettings(BaseSettings):
    worker_name: str = "Celery Worker"
    broker_base_uri: str = "amqp://guest:guest@localhost:5672/"
    vhost_name: str = "/"


class ModelSettings(BaseSettings):
    model_name_or_path: str = "./model"
    model_output_path: str = "./outputs"


class FirebaseSettings(BaseSettings):
    cred_path: str = "/app/key/serviceAccountKey.json"
    database_url: str
    storage_bucket: str
    app_name: str = "diffusers-inpainting"


celery_worker_settings = CeleryWorkerSettings()
model_settings = ModelSettings()
firebase_settings = FirebaseSettings()
