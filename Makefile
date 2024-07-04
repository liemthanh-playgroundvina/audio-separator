download_model:
	mkdir ./models
	git clone https://huggingface.co/seanghay/uvr_models ./models
	rm -rf /models/.git

config:
	mkdir -p logs && touch logs/celery.log
	cp configs/env.example configs/.env
	# And add params ...

# Docker
build:
	docker pull nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04
	docker build -t audio-separator -f Dockerfile .

start:
	docker compose -f docker-compose.yml down
	docker compose -f docker-compose.yml up -d

start-prod:
	docker compose -f docker-compose-prod.yml down
	docker compose -f docker-compose-prod.yml up -d

stop:
	docker compose -f docker-compose.yml down

stop-prod:
	docker compose -f docker-compose-prod.yml down

# Checker
cmd-image:
	docker run -it --gpus all --rm -v .:/app audio-separator /bin/bash

cmd-worker:
	docker compose exec worker-audio-separator /bin/bash

log-worker:
	cat logs/celery.log
