# Makefile for SciPy Docker CI/CD Project

# Variables
IMAGE_NAME = scipy-app
CONTAINER_NAME = scipy-container
VERSION = latest

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

# Run the Docker container interactively
run:
	docker run -it --rm --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME):$(VERSION)

# Run tests inside the Docker container
test:
	docker run --rm $(IMAGE_NAME):$(VERSION) python -m pytest tests/ -v --cov=src

# Run linting checks
lint:
	docker run --rm $(IMAGE_NAME):$(VERSION) flake8 src/

# Run code formatting
format:
	docker run --rm $(IMAGE_NAME):$(VERSION) black src/

# Run code formatting check
format-check:
	docker run --rm $(IMAGE_NAME):$(VERSION) black --check --diff src/

# Run all quality checks
quality: lint test format-check

# Start development environment with docker-compose
dev:
	docker-compose up

# Start development environment in background
dev-bg:
	docker-compose up -d

# Stop the development environment
dev-stop:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Run tests with docker-compose
test-compose:
	docker-compose run test

# Start Jupyter Notebook
jupyter:
	docker-compose up jupyter

# Clean up Docker resources
clean:
	docker system prune -f
	docker image prune -f

# Push to GitHub Container Registry (requires login)
push:
	docker tag $(IMAGE_NAME):$(VERSION) ghcr.io/$(GITHUB_USER)/$(GITHUB_REPO):$(VERSION)
	docker push ghcr.io/$(GITHUB_USER)/$(GITHUB_REPO):$(VERSION)

# Pull from GitHub Container Registry
pull:
	docker pull ghcr.io/$(GITHUB_USER)/$(GITHUB_REPO):$(VERSION)

# Login to GitHub Container Registry
login-ghcr:
	echo ${GITHUB_TOKEN} | docker login ghcr.io -u $(GITHUB_USER) --password-stdin

# # Push to registry (requires login)
# push:
# 	docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)
# 	docker push $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)

# # Pull from registry
# pull:
# 	docker pull $(DOCKER_USERNAME)/$(IMAGE_NAME):$(VERSION)

# Help
help:
	@echo "Makefile commands:"
	@echo "  build          - Build the Docker image"
	@echo "  run            - Run the Docker container interactively"
	@echo "  test           - Run tests inside the Docker container"
	@echo "  lint           - Run linting checks"
	@echo "  format         - Run code formatting"
	@echo "  format-check   - Check code formatting"
	@echo "  quality        - Run all quality checks"
	@echo "  dev            - Start development environment with docker-compose"
	@echo "  dev-bg         - Start development environment in background"
	@echo "  dev-stop       - Stop the development environment"
	@echo "  logs           - View logs"
	@echo "  test-compose   - Run tests with docker-compose"
	@echo "  jupyter        - Start Jupyter Notebook"
	@echo "  clean          - Clean up Docker resources"
	@echo "  push		    - Push to registry"
	@echo "  pull		    - Pull from registry"
	@echo "  help           - Show this help message"

.PHONY: build run test lint format format-check quality dev dev-bg dev-stop logs test-compose jupyter push pull clean help