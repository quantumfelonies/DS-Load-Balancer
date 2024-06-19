# Customizable Load Balancer

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Testing and Performance Analysis](#testing-and-performance-analysis)
7. [Experimental Results](#experimental-results)
8. [Troubleshooting](#troubleshooting)
9. [Contributions](#contributions)
10. [License](#license)

## Introduction
In this project, we have implemented a customizable load balancer that routes asynchronous requests from clients to a set of server instances. The load balancer uses a consistent hashing data structure to efficiently distribute the load among the servers, and it can dynamically scale the system by adding or removing server instances as needed.

## System Architecture
The system consists of the following components:

1. **Server**: A simple web server that accepts HTTP requests on port 5000 and responds to the following endpoints:
   - `/home` (GET): Returns a string with a unique identifier to distinguish among the replicated server containers.
   - `/heartbeat` (GET): Sends an empty response with a valid response code (200) to allow the load balancer to monitor the server's health.

2. **Load Balancer**: The load balancer is responsible for managing the set of server instances and routing client requests to them using the consistent hashing algorithm. It provides the following HTTP endpoints:
   - `/rep` (GET): Returns the status of the replicas managed by the load balancer, including the number of replicas and their hostnames.
   - `/add` (POST): Adds new server instances to the load balancer to scale up with increasing client numbers. Expects a JSON payload with the number of new instances and their preferred hostnames.
   - `/delete` (POST): Removes server instances from the load balancer. Expects a JSON payload with the hostnames of the instances to be removed.
   - `/health` (GET): Returns the health status of the load balancer and the managed server replicas.
   - `/route` (POST): Routes client requests to the appropriate server instance using the consistent hashing algorithm.

3. **Consistent Hashing**: The consistent hashing data structure is used by the load balancer to efficiently distribute the requests among the server instances. It uses the following parameters and hash functions:
   - Number of server containers managed by the load balancer (N) = 3
   - Total number of slots in the consistent hash map (#slots) = 512
   - Number of virtual servers for each server container (K) = log2(512) = 9
   - Hash function for request mapping: `H(i) = i + 2i + 17`
   - Hash function for virtual server mapping: `Φ(i, j) = i^2 + j^2 + 2j + 25`

## Getting Started

### Prerequisites
- Docker version 20.10.23 or above
- Ubuntu 20.04 LTS or above

### Installation
1. Clone the repository:
```
git clone https://github.com/your-username/customizable-load-balancer.git
```
2. Navigate to the project directory:
```
cd customizable-load-balancer
```
3. Build the Docker images:
```
make build
```
4. Run the Docker containers:
```
make run
```

## Usage
Once the system is up and running, you can interact with the load balancer through the provided HTTP endpoints. For example, to route a client request to the appropriate server instance, you can use the `/route` endpoint:

```
curl -X POST -H "Content-Type: application/json" -d '{"request": "some-request-data"}' http://localhost:5000/route
```

The load balancer will respond with the appropriate server instance's hostname.

## Configuration
### Environment Variables
The system can be configured using environment variables. Here are some of the key variables:

- `LOAD_BALANCER_PORT`: Port on which the load balancer listens (default: 5000).
- `HEALTH_CHECK_INTERVAL`: Interval for health check of servers in seconds (default: 30).
- `REPLICA_THRESHOLD`: Number of requests a server should handle before a new instance is added (default: 100).

## Testing and Performance Analysis
We have included a comprehensive set of tests to ensure the correct functioning of the load balancer and the consistent hashing implementation. Additionally, we have performed performance analysis to measure the load distribution, throughput, and response times under various client load conditions.

The details of the testing and performance analysis can be found in the `README.md` file in the project's root directory.

## Experimental Reuslts

![WhatsApp Image 2024-06-15 at 22 36 48 (1)](https://github.com/quantumfelonies/DS-Load-Balancer/assets/122482160/5aea4cb9-9d92-41ee-b2aa-c3d0248c3ae4)

![WhatsApp Image 2024-06-15 at 22 36 48](https://github.com/quantumfelonies/DS-Load-Balancer/assets/122482160/000741a2-c078-41cc-ba24-a145674703fa)

![WhatsApp Image 2024-06-15 at 22 36 47](https://github.com/quantumfelonies/DS-Load-Balancer/assets/122482160/1a3b219e-edef-4b76-a117-c3e86e3bc95d)

![WhatsApp Image 2024-06-15 at 22 36 49](https://github.com/quantumfelonies/DS-Load-Balancer/assets/122482160/c8d392a4-db57-4c18-b447-8e8060a95646) 

![WhatsApp Image 2024-06-15 at 22 55 13 (1)](https://github.com/quantumfelonies/DS-Load-Balancer/assets/122482160/45e58126-9e5a-4d3d-b231-340aab1a06be)

![WhatsApp Image 2024-06-15 at 22 55 13](https://github.com/quantumfelonies/DS-Load-Balancer/assets/122482160/00ee46af-a196-4ab5-83a6-62dfc5fd7225)

## Troubleshooting

Here are some common issues and their solutions:

### Load balancer not responding to requests
**Issue:** The load balancer is not responding to HTTP requests, or clients are unable to reach the load balancer.

**Solution:** 
1. Ensure the load balancer container is running by executing:
    ```bash
    docker ps
    ```
   Look for the container running the load balancer. If it is not running, start it using:
    ```bash
    make run
    ```

2. Check that the ports are correctly exposed. Use the following command to inspect the container:
    ```bash
    docker inspect <container_id>
    ```
   Verify that the correct port (default 5000) is being mapped and is open on your firewall.

3. Review the load balancer logs for any errors or issues:
    ```bash
    docker logs <container_id>
    ```
   Look for any error messages that may indicate why the load balancer is not functioning correctly.

### Health checks failing for a server
**Issue:** One or more servers are not passing health checks, and the load balancer is marking them as unhealthy.

**Solution:**
1. Verify that the server is running and accessible by checking its status:
    ```bash
    docker ps
    ```
   Ensure the server container is listed and running.

2. Test the `/heartbeat` endpoint directly to confirm it is responding correctly:
    ```bash
    curl http://<server_host>:5000/heartbeat
    ```
   You should receive a `200 OK` response. If not, check the server logs for any issues:
    ```bash
    docker logs <server_container_id>
    ```

3. Ensure there are no network issues preventing the load balancer from reaching the server. Check firewall settings and network configurations.

### Load is not evenly distributed among servers
**Issue:** The load is unevenly distributed, causing some servers to be overloaded while others are underutilized.

**Solution:**
1. Review the consistent hashing algorithm parameters in your load balancer configuration. Ensure that the number of virtual nodes is sufficient for a balanced load distribution.

2. Verify the load balancer's configuration file (`config.json` or environment variables) to ensure it is correctly set up for the number of servers and slots:
    ```json
    {
      "load_balancer_port": 5000,
      "health_check_interval": 30,
      "replica_threshold": 100
    }
    ```

3. Check the load balancer logs to identify any anomalies or errors in request routing:
    ```bash
    docker logs <load_balancer_container_id>
    ```

4. Perform a health check and review the status of all servers to ensure they are operating correctly:
    ```bash
    curl http://<load_balancer_host>:5000/health
    ```

### Docker-related issues
**Issue:** Docker containers are not starting, or there are issues with Docker itself.

**Solution:**
1. Ensure Docker is installed and running. Start Docker if it is not running:
    ```bash
    sudo systemctl start docker
    ```

2. If Docker containers are not starting as expected, check for any errors in the Docker logs:
    ```bash
    sudo journalctl -u docker
    ```

3. Verify that there is enough disk space and memory available for Docker to run the containers:
    ```bash
    df -h
    free -m
    ```

4. If all else fails, try restarting Docker and your containers:
    ```bash
    sudo systemctl restart docker
    make run
    ```

## Contributions
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open a new issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
