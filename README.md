# Socket Checker
A simple REST API that allows you to check whether sockets are open by asynchronously attempting to start connections.

# Usage with Docker
1. Edit `docker-compose.yaml` file
  - Replace the value for `SOCKET_CHECKER_SECRET` with your own secret
  - Change the port mapping from `4045:4045` to `<port you want to expose the API on>:4045` (host port <-- container port)
2. Build the Docker image: `docker build -t socket-checker .`
3. Run the container: `docker-compose up`. To run in detached mode, add the option `-d`.


# API
### Request
#### URL: `/checker`

#### Method: `GET`

#### Header: `HTTP_AUTHORIZATION` 
- Should contain the secret that matches the secret you chose and placed in your `docker-compose.yaml` file.

#### JSON payload
```json
{
	"sockets": [
		["0.0.0.0", 5050],
		["178.239.166.155", 22],
		["185.16.206.10", 22],
	],
	"timeout": 3
}
``` 
Note: `timeout` is optional, the API will default the connection timeout to 3 seconds.
### Response
#### Success (`HTTP 200`)
```json
{
  "results": [
    ["0.0.0.0", 22, false ],
    ["178.239.166.155", 22, false ],
    ["185.16.206.10", 22, false ]],
  "total_duration_seconds": 4.0100345611572266,
  "open": 1,
  "closed": 9,
  "total": 10,
  "timeout_seconds": 3
}
```
#### Failure – incorrect `HTTP_AUTHORIZATION` secret (`HTTP 401`)
```json
{
  "detail": "Unauthorised"
}
```