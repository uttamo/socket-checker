# 🔌 Socket Checker
A simple REST API that allows you to check whether sockets are open by asynchronously attempting to start connections.

# Usage with Docker
1. Edit `docker-compose.yaml` file with the following changes
   * Replace the value for `SOCKET_CHECKER_SECRET` with your own secret.
   * [Change the port mapping](https://docs.docker.com/compose/compose-file/#ports) `<host port>:<container port>` (host port <-- container port).
2. Build the Docker image: `docker build -t socket-checker .`
3. Run the container: `docker-compose up`. To run in detached mode, add the option `-d`.


# API
### Request
#### Endpoint: `GET /check_sockets`
#### JSON request body
```json
{
  "api_secret": "<secret-from-docker-compose-file>",
  "sockets": [
          ["0.0.0.0", 5050],
          ["178.239.166.155", 22],
          ["185.16.206.10", 22]
  ],
  "timeout": 4
}
``` 
Note: `timeout` is optional, the API will default the connection timeout to 3 seconds if not provided.
### Response
#### ✅ Success (`HTTP 200`)
```json
{
  "results": [
    ["0.0.0.0", 22, true],
    ["178.239.166.155", 22, true],
    ["185.16.206.10", 22, false]
],
  "total_duration_seconds": 4.0100345611572266,
  "open": 1,
  "closed": 9,
  "total": 10,
  "timeout_seconds": 4
}
```
#### ⚠️ Failure – incorrect `api_secret` value (`HTTP 401`)
```json
{
  "detail": "Unauthorised."
}
```