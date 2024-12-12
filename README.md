# Kubernetes Spaceport and Spaceship Services

This repository contains two FastAPI services: `spaceport` and `spaceship`. These services demonstrate interactions 
between Kubernetes pods, focusing on observability and instrumentation.

## Services

### Spaceport

The `spaceport` service manages docking and separation of spaceships. It provides endpoints to request docking, dock, 
request separation, and separate ships.

### Spaceship

The `spaceship` service interacts with the `spaceport` service. It obtains the ship ID from the container's hostname 
and uses it to request docking and separation authorizations.

## Building Docker Images

You can build Docker images for different versions of the services by specifying the version as a build argument.

```sh
cd spaceport
docker build --build-arg VERSION=v1 -t spaceport:v1 .
docker build --build-arg VERSION=v2 -t spaceport:v2 .
```

## Deploying with Helm
You can deploy the services using Helm charts and specify the image version using the --set flag.

### Example Helm Command
```sh
helm upgrade --install enterprise spaceship/spaceship --set image.tag=v1 --set service.type=NodePort
helm upgrade --install voyager spaceship/spaceship --set image.tag=v1 --set service.type=NodePort
helm upgrade --install deepspace9 spaceport/spaceport --set image.tag=v1
```
