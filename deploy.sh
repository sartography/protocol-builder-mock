#!/bin/bash

# Build and push Docker image to Docker Hub
echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build --no-cache -t sartography/protocol-builder-mock:latest . || exit 1;
docker push sartography/protocol-builder-mock:latest || exit 1;

# Notify UVA DCOS that Docker image has been updated
aws sqs send-message --queue-url 'https://queue.amazonaws.com/474683445819/dcos-refresh' --message-body 'crconnect/pb' || exit 1;
