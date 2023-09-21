include ../infra/.env


IMAGE_NAME ?= frontend
IMAGE=${DOCKER_USERNAME}/${APPLICATION_NAME}_${IMAGE_NAME}

.PHONY: all build clean

build:
	docker build -t ${IMAGE} .

push:
	docker push ${IMAGE}
