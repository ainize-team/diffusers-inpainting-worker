# import firebase_admin
from celery import Celery

import celeryconfig
from config import celery_worker_settings


# from firebase_admin import credentials


app = Celery(
    celery_worker_settings.worker_name,
    broker=f"{celery_worker_settings.broker_base_uri}/{celery_worker_settings.vhost_name}",
    include=["tasks"],
)
app.config_from_object(celeryconfig)


# cred = credentials.Certificate(firebase_settings.cred_path)
# firebase_admin.initialize_app(
#     cred,
#     {
#         "databaseURL": firebase_settings.database_url,
#         "storageBucket": firebase_settings.storage_bucket,
#     },
# )
