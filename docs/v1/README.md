# V1 - Starting to Observe

## Introduction
The first objective was to be able to track docking and separation of spaceships in each spaceport. The Spaceport 
Observation System (SOS) required that all ships must first request a docking or separation authorization code. They 
must then use this code to dock or separate from the spaceport. 

In V1 the SOS just uses log files to record activity. The GIT insisted that the logs must be in a structured format
and chose to use JSON. 

## Building Docker Images
You can build Docker images for different versions of the services by specifying the version as a build argument.

```sh
docker build --build-arg VERSION=v1 -t spaceport:v1 spaceport/.
docker build --build-arg VERSION=v1 -t spaceship:v1 spaceship/.
```

## Deploying with Helm
You can deploy the services using Helm charts and specify the image version using the --set flag.

```shell
helm upgrade --install endeavour spaceship/spaceship --set image.tag=v1 --set service.nodePort=32000
helm upgrade --install explorer spaceship/spaceship --set image.tag=v1 --set service.nodePort=32001
helm upgrade --install invincible spaceship/spaceship --set image.tag=v1 --set service.nodePort=32002
helm upgrade --install avenger spaceship/spaceship --set image.tag=v1 --set service.nodePort=32003
helm upgrade --install venture spaceship/spaceship --set image.tag=v1 --set service.nodePort=32004
helm upgrade --install pontus spaceport/spaceport --set image.tag=v1 --set service.nodePort=32500
helm upgrade --install zura spaceport/spaceport --set image.tag=v1 --set service.nodePort=32501
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
GIT has started to observe the spaceports. They have started to record the docking and separation of spaceships. They 
can retrieve the logs from each spaceport and see what has happened. They can see where things have gone wrong, but
they are struggling to understand why.

They also have to link log lines together to understand the journey of a spaceship. This is a manual process, and 
they are looking for a better way to do this.

### Example Logs

**spaceport**
```json lines
{"message": "Started server process [1]", "color_message": "Started server process [\u001b[36m%d\u001b[0m]"}
{"message": "Waiting for application startup."}
{"message": "Application startup complete."}
{"message": "Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)", "color_message": "Uvicorn running on \u001b[1m%s://%s:%d\u001b[0m (Press CTRL+C to quit)"}
{"message": "192.168.65.3:60136 - \"GET /docs HTTP/1.1\" 200"}
{"message": "192.168.65.3:60136 - \"GET /openapi.json HTTP/1.1\" 200"}
{"message": "192.168.65.3:60144 - \"GET /docked_ships HTTP/1.1\" 200"}
{"message": "Requesting docking for ship explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:36446 - \"GET /request_docking/explorer-spaceship-666fdd8f57-84crh HTTP/1.1\" 200"}
{"message": "Ship explorer-spaceship-666fdd8f57-84crh docked successfully", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:36456 - \"POST /dock HTTP/1.1\" 200"}
{"message": "192.168.65.3:41956 - \"GET /docked_ships HTTP/1.1\" 200"}
{"message": "Requesting docking for ship invincible-spaceship-74f55bf59f-gh9d6"}
{"message": "10.20.4.237:52990 - \"GET /request_docking/invincible-spaceship-74f55bf59f-gh9d6 HTTP/1.1\" 200"}
{"message": "Ship invincible-spaceship-74f55bf59f-gh9d6 docked successfully", "ship_id": "invincible-spaceship-74f55bf59f-gh9d6"}
{"message": "10.20.4.237:53006 - \"POST /dock HTTP/1.1\" 200"}
{"message": "192.168.65.3:47126 - \"GET /docked_ships HTTP/1.1\" 200"}
{"message": "Requesting separation for ship explorer-spaceship-666fdd8f57-84crh", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:50354 - \"GET /request_separation/explorer-spaceship-666fdd8f57-84crh HTTP/1.1\" 200"}
{"message": "Ship explorer-spaceship-666fdd8f57-84crh separated successfully", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:50360 - \"POST /separate HTTP/1.1\" 200"}
{"message": "Requesting docking for ship explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:50364 - \"GET /request_docking/explorer-spaceship-666fdd8f57-84crh HTTP/1.1\" 200"}
{"message": "Ship explorer-spaceship-666fdd8f57-84crh docked successfully", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:50368 - \"POST /dock HTTP/1.1\" 200"}
{"message": "Requesting separation for ship explorer-spaceship-666fdd8f57-84crh", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:39888 - \"GET /request_separation/explorer-spaceship-666fdd8f57-84crh HTTP/1.1\" 200"}
{"message": "Ship explorer-spaceship-666fdd8f57-84crh separated successfully", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:39894 - \"POST /separate HTTP/1.1\" 200"}
{"message": "Requesting separation for ship explorer-spaceship-666fdd8f57-84crh", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:46738 - \"GET /request_separation/explorer-spaceship-666fdd8f57-84crh HTTP/1.1\" 200"}
{"message": "Ship explorer-spaceship-666fdd8f57-84crh not found", "ship_id": "explorer-spaceship-666fdd8f57-84crh"}
{"message": "10.20.4.236:46742 - \"POST /separate HTTP/1.1\" 400"}
```