# Diffusers Inpainting Worker

[![Github Contributors](https://img.shields.io/github/contributors/ainize-team/diffusers-inpainting-worker)](https://github.com/badges/ainize-team/diffusers-inpainting-worker/contributors)
[![GitHub issues](https://img.shields.io/github/issues/ainize-team/diffusers-inpainting-worker.svg)](https://github.com/ainize-team/diffusers-inpainting-worker/issues)
![Github Last Commit](https://img.shields.io/github/last-commit/ainize-team/diffusers-inpainting-worker)
![Github Repository Size](https://img.shields.io/github/repo-size/ainize-team/diffusers-inpainting-worker)
[![GitHub Stars](https://img.shields.io/github/stars/ainize-team/diffusers-inpainting-worker.svg)](https://github.com/ainize-team/diffusers-inpainting-worker/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/ainize-team/diffusers-inpainting-worker.svg)](https://github.com/ainize-team/diffusers-inpainting-worker/network/members)
[![GitHub Watch](https://img.shields.io/github/watchers/ainize-team/diffusers-inpainting-worker.svg)](https://github.com/ainize-team/diffusers-inpainting-worker/watchers)

![Supported Python versions](https://img.shields.io/badge/python-3.9-brightgreen)
[![Imports](https://img.shields.io/badge/imports-isort-brightgreen)](https://pycqa.github.io/isort/)
[![Code style](https://img.shields.io/badge/code%20style-black-black)](https://black.readthedocs.io/en/stable/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
![Package Management](https://img.shields.io/badge/package%20management-mamba-black)

## Description
Worker Server for [Diffusers](https://huggingface.co/docs/diffusers/index).

## Installation
1. Run RabbitMQ image as a Broker
```
docker run -d \
    --name inpainting-rabbitmq \
    -p 5672:5672 \
    -p 15672:15672 \
    --restart=unless-stopped \
    rabbitmq:3.11.2-management
```

2. Build Docker image
```
git clone https://github.com/ainize-team/diffusers-inpainting-worker
cd diffusers-inpainting-worker
docker build -t inpainting-worker .
```
3. Run Docker Image
```
docker run -d --name inpainting-container-0 \
--gpus='"device=0"' \
-e BROKER_BASE_URI=<BROKER_BASE_URI> \
-e VHOST_NAME=<VHOST_NAME> \
-e APP_NAME=<APP_NAME> \
-e DATABASE_URL=<DATABASE_URL> \
-e STORAGE_BUCKET=<STORAGE_BUCKET>
-v <firebase_credential_path>:/app/key -v <model_local_path>:/app/model \
inpainting-worker
```

or

```
docker run -d --name inpainting-container-0 \
--gpus='"device=0"' \
--env-file .env \
-v <firebase_credential_path>:/app/key -v <model_local_path>:/app/model \
inpainting-worker
```
## Usage
* Check our [diffusers-inpainting-api](https://github.com/ainize-team/diffusers-inpainting-api) Repo.

## License

[![Licence](https://img.shields.io/github/license/ainize-team/diffusers-inpainting-worker.svg)](./LICENSE)