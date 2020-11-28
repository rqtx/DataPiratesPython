# import env config

#cnf ?= .env
#include $(cnf)
#export $(shell sed 's/=.*//' $(cnf))

# Get the latest tag
TAG=$(shell git describe --tags --abbrev=0)
GIT_COMMIT=$(shell git log -1 --format=%h)

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

run: ## Run script
	docker run --rm -v $$PWD:/app -w /app --entrypoint "./run.sh" python:3.7-slim

debug: ## Run bash to troubleshooting
	docker run --rm -i -v $$PWD:/app -w /app --entrypoint "bash" python:3.7-slim