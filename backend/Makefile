ifneq (,$(wildcard ../infra/.env))
    include ../infra/.env
endif

IMAGE_NAME ?= backend
IMAGE=${DOCKER_USERNAME}/${APPLICATION_NAME}_${IMAGE_NAME}

build:
	docker build -t ${IMAGE} .

push:
	docker push ${IMAGE}

run:
	gunicorn --bind 0.0.0.0:${BACKEND_PORT} ${APPLICATION_NAME}_${IMAGE_NAME}.wsgi
