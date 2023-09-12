.PHONY: help docker-build docker-run

help:
	@cat Makefile | grep -E "^\w+$:"

docker-build:
	docker build . -t deez_$(notdir $(shell pwd))

docker-run: docker-build
	docker run -v $(shell pwd)/videos:/deez/videos -p 5000:5000 -t deez_$(notdir $(shell pwd)) -e OPENAI_API_KEY -e FAKEYOU_USERNAME -e FAKEYOU_PASSWORD

fmt: # Format code
	poetry run isort app/
	poetry run black app/
