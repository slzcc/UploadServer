SHELL := /bin/bash
VERSION := "2"
build:
	@docker build -t slzcc/uploadserver:backend-v$(VERSION) . --no-cache
push:
	@docker push slzcc/uploadserver:backend-v$(VERSION)