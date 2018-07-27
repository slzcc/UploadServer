SHELL := /bin/bash
VERSION := "2"
build:
	@docker build -t slzcc/django:upload-uwsgi-v$(VERSION) .
