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

## How to start
### Using docker-compose(recommended)
1. Create RabbitMQ and FastAPI container(refer to [diffusers-inpainting-api](https://github.com/ainize-team/diffusers-inpainting-api))

2. Clone repository
```shell
git clone https://github.com/ainize-team/diffusers-inpainting-worker
cd diffusers-inpainting-worker
```

3. Edit [docker-compose.yml](./docker-compose.yml) and [.env file](./.env.sample) for your project.
- Vhost for each worker is in [docker-compose.yml](./docker-compose.yml) and common RabbitMQ config is in [.env file](./.env.sample).

4. Run worker container
```shell
docker-compose up -d

# If you want to run a specific worker container, write service name.
docker-compose up -d <service name>
```

### Using docker
1. Run RabbitMQ comtainer as a broker
```shell
docker run -d --name diffusers-inpainting-rabbitmq -p 5672:5672 -p 15672:15672 --restart=unless-stopped rabbitmq:3.11.2-management
```

2. Clone repository
```shell
git clone https://github.com/ainize-team/diffusers-inpainting-worker
cd diffusers-inpainting-worker
```

3. Build docker image
```shell
docker build -t diffusers-inpainting-worker .
```

4. Run docker container
```
docker run -d --name diffusers-inpainting-worker \
--gpus='"device=0"' \
-e BROKER_URI=<broker_uri> \
-e FIREBASE_APP_NAME=<firebase_app_name> \
-e FIREBASE_DATABASE_URL=<firebase_database_urlL> \
-e FIREBASE_STORAGE_BUCKET=<firebase_storage_bucket>
-v <firebase_credential_path>:/app/key -v <model_local_path>:/app/model \
diffusers-inpainting-worker
```

or

```
docker run -d --name diffusers-inpainting-worker \
--gpus='"device=0"' \
--env-file .env \
-v <firebase_credential_path>:/app/key -v <model_local_path>:/app/model \
diffusers-inpainting-worker
```

## Usage
* Check our [diffusers-inpainting-api](https://github.com/ainize-team/diffusers-inpainting-api) Repo.

## License

[![Licence](https://img.shields.io/github/license/ainize-team/diffusers-inpainting-worker.svg)](./LICENSE)