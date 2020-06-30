SHELL := /bin/bash
VERSION := "4"
build:
	@docker build -t slzcc/uploadserver:backend-v$(VERSION) -f docker/Dockerfile . --no-cache
push:
	@docker push slzcc/uploadserver:backend-v$(VERSION)

