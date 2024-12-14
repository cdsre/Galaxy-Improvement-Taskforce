# Kubernetes Spaceport and Spaceship Services

This repository contains two FastAPI services: `spaceport` and `spaceship`. These services demonstrate interactions 
between Kubernetes pods, focusing on observability and instrumentation.

This repo was built for a local demo on my laptop so is utilising Docker Desktop Kuberenetes. This allows the docker 
images to be built locally and docker shim will allow kubernetes to get these from the local Docker Desktop image cache

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
helm upgrade --install enterprise spaceship/spaceship --set image.tag=v1 --set service.nodePort=32001
helm upgrade --install voyager spaceship/spaceship --set image.tag=v1 --set service.nodePort=32002
helm upgrade --install deepspace9 spaceport/spaceport --set image.tag=v1 --set service.nodePort=32000
```

## Versions

### v1
v1 is the initial version of the services. It has no logging and just relies on the auto-intstrumentation from the OTEL
operator. This version shows how its easy to see where something failed but hard to tell why it failed.

### v2
v2 adds logging to the services. This version shows how logging can help to understand why something failed. It starts 
off as just logging and users have to find the trace ID in the backend and then grep for it in the logs to find the errors. 
This is an improvement on v1 as we can now understand why it failed. But it still needs manual correlation of logs and
traces.

As an additional part of V2 we then introduce the python auto-instrumentation for logging to link logs to spans.
