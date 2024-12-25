import firebase_admin
from celery import Celery
from firebase_admin import credentials

import celeryconfig
from config import celery_worker_settings, firebase_settings


app = Celery(
    celery_worker_settings.worker_name,
    broker=f"{celery_worker_settings.broker_uri}",
    include=["tasks"],
)
app.config_from_object(celeryconfig)


cred = credentials.Certificate(firebase_settings.cred_path)
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": firebase_settings.firebase_database_url,
        "storageBucket": firebase_settings.firebase_storage_bucket,
    },
)
