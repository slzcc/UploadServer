SHELL := /bin/bash
VERSION := "4"
build:
	@docker build -t slzcc/uploadserver:frontend-v$(VERSION) . --no-cache
push:
	@docker push slzcc/uploadserver:frontend-v$(VERSION)
