NAME := $(or $(NAME), ecoreuse)
BUILD_DATE := $(shell date "+%Y%m%d")
VERSION := $(or $(VERSION), $(shell python -c "import ya3_collect; print(ya3_collect.__version__)"))
TAG_VERSION := $(VERSION)-$(BUILD_DATE)
BUILD_ARGS := $(or $(BUILD_ARGS), $(shell echo "--platform linux/arm64"))
MAJOR := $(word 1,$(subst ., ,$(TAG_VERSION)))
MINOR := $(word 2,$(subst ., ,$(TAG_VERSION)))

pre-docker-build: ya3_collect
	python setup.py sdist
	cp dist/ya3-collect-$(VERSION).tar.gz docker/ya3-collect.tar.gz

buildx: pre-docker-build
	docker login
	docker buildx build $(BUILD_ARGS) --push --cache-to=$(NAME)/ya3-collect:cache -t $(NAME)/ya3-collect:${TAG_VERSION} docker
	docker buildx build $(BUILD_ARGS) --push --cache-from=$(NAME)/ya3-collect:cache -t $(NAME)/ya3-collect:latest docker
	docker buildx build $(BUILD_ARGS) --push --cache-from=$(NAME)/ya3-collect:cache -t $(NAME)/ya3-collect:$(MAJOR) docker
	docker buildx build $(BUILD_ARGS) --push --cache-from=$(NAME)/ya3-collect:cache -t $(NAME)/ya3-collect:$(MAJOR).$(MINOR) docker

test: mypy unittest

mypy:
	mypy ya3_collect tests

unittest:
	coverage run -m unittest
	coverage html
	coverage report