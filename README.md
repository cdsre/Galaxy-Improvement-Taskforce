# Space Port Authority (SPA) Observability Journey

## Introduction
In a Galaxy far, far away, in the DevOps Quadrant, spaceports were independently operated and each had their own processes
and ways of working, with some being better than others. A Galaxy Improvement Taskforce (GIT) was formed to try to 
standardise and provide a central space ledger to record spaceport activity. 

The starting point for the GIT was to provide observability into the spaceports. This would allow them to understand 
where things were going wrong and why. The GIT decided to use OpenTelemetry to provide this observability. 

The first objective was to be able to track docking and separation of spaceships in each spaceport. v1 of the Spaceport
Observation System (SOS) focuses on tracking the docking and separation of spaceships.

## SOS Architecture

This repository contains two FastAPI services: [spaceport](./spaceport) and [spaceship](./spaceship). These services
are created as container images and deployed into a kubernetes cluster.

This repo was built for a local demo on my laptop so is utilising Docker Desktop Kubernetes. This allows the docker 
images to be built locally and docker shim will allow kubernetes to get these from the local Docker Desktop image cache.
The heml charts default to NodePort as the service type to allow us to set fixed ports for each instance of spaceships
and spaceports. This is to allow us to easily switch between versions of the services and see the differences in the
observability.


## SOS Journey

* [v1](v1/README.md) - Initial version of the Spaceport Observation System (SOS)





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
