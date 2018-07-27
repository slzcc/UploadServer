SHELL := /bin/bash
VERSION := "3"
build:
	@docker build -t slzcc/django:upload-uwsgi-v$(VERSION) . --no-cache
