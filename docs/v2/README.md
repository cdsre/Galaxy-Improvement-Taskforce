# V1 - Starting to Trace

## Introduction
The SOS were grateful to now have insight into the spaceport's activity. However, trying to piece together information from
the spaceport and spaceship logs was difficult. It was not clear which event in the spaceport logs was related to which event
in the spaceship logs.

They found it difficult to understand the journey of a spaceship requesting authorisation to docker or separate, then 
performing the action. The GIT decided to add tracing to the SOS to help them understand the journey of a spaceship.

In V2 the SOS enables auto-instrumentation using the OTEL Operator. The core services are still the same, but now they are
instrumented to provide traces. The GIT can now see the journey of a spaceship from requesting authorisation to docking or
separating from the spaceport.

## Building Docker Images
You can build Docker images for different versions of the services by specifying the version as a build argument.

```sh
docker build --build-arg VERSION=v2 -t spaceport:v2 spaceport/.
docker build --build-arg VERSION=v2 -t spaceship:v2 spaceship/.
```

## Deploying OpenTelemetry Instrumentation
We will use the opentelemetry operator and install it via helm with a self-signed certificate. You can read more about 
this in the [otel README.md](../otel/README.md).

Once installed deploy the OpenTelemetry Collector and Instrumentation.

```shell
kubectl apply -f otel/v2/
```

## Deploying with Helm
You can deploy the services using Helm charts and specify the image version using the --set flag.

```shell
helm upgrade --install endeavour spaceship/spaceship --set image.tag=v2 --set service.nodePort=32000
helm upgrade --install explorer spaceship/spaceship --set image.tag=v2 --set service.nodePort=32001
helm upgrade --install invincible spaceship/spaceship --set image.tag=v2 --set service.nodePort=32002
helm upgrade --install avenger spaceship/spaceship --set image.tag=v2 --set service.nodePort=32003
helm upgrade --install venture spaceship/spaceship --set image.tag=v2 --set service.nodePort=32004
helm upgrade --install pontus spaceport/spaceport --set image.tag=v2 --set service.nodePort=32500
helm upgrade --install zura spaceport/spaceport --set image.tag=v2 --set service.nodePort=32501
```

## Testing
We have set up each pod as a NodePort service so you can test the services by using curl to send a POST request to the
spaceship, and it will interact with the spaceport. 

### Dock
```shell
curl -X 'POST' \
  'http://localhost:32001/dock/pontus-spaceport' \
  -H 'accept: application/json' \
  -d ''
```

### Separate
```shell
curl -X 'POST' \
  'http://localhost:32001/separate/pontus-spaceport' \
  -H 'accept: application/json' \
  -d ''
```

## Conclusion
GIT was excited to see the traces in the backend. They could now see the journey of a spaceship from requesting authorisation
to docking or separating from the spaceport. They could see the journey of a spaceship in the backend and could now understand
why things went wrong.

They also had a better understanding of timing and how events correlated with each other as a single trace without all 
the manual work of joining up the log lines. However when things went wrong it was still difficult to understand why just
from the trace.

However even the logs were being intrumented to the operations team could narrow done the relavant log events.

### Example Log - Filtered with traceID
```shell
$ k logs pontus-spaceport-85cbfcc54f-nn9xd spaceport | grep 380933d83077d65b2876aa9470c98a27
{"message": "Requesting docking for ship endeavour-spaceship-8475997dcd-2jl9b", "otelSpanID": "f14bbacbbc8c043c", "otelTraceID": "380933d83077d65b2876aa9470c98a27", "otelTraceSampled": true, "otelServiceName": "pontus-spaceport"}
{"message": "10.20.4.243:40854 - \"GET /request_docking/endeavour-spaceship-8475997dcd-2jl9b HTTP/1.1\" 200", "otelSpanID": "b68a88396a22da4d", "otelTraceID": "380933d83077d65b2876aa9470c98a27", "otelTraceSampled": true, "otelServiceName": "pontus-spaceport"}
{"message": "Docking limit '3' reached, Dock is full", "otelSpanID": "7c8bfa42de6ec394", "otelTraceID": "380933d83077d65b2876aa9470c98a27", "otelTraceSampled": true, "otelServiceName": "pontus-spaceport", "ship_id": "endeavour-spaceship-8475997dcd-2jl9b"}
{"message": "10.20.4.243:40862 - \"POST /dock HTTP/1.1\" 400", "otelSpanID": "0017fa6f91ac76bd", "otelTraceID": "380933d83077d65b2876aa9470c98a27", "otelTraceSampled": true, "otelServiceName": "pontus-spaceport"}
```

### Example Traces

**Traces**
![Traces](./traces.png)
![Success](./successful_dock.png)
![Failure](./failed_dock.png)