# Customizable Load Balancer

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

## Testing and Performance Analysis
We have included a comprehensive set of tests to ensure the correct functioning of the load balancer and the consistent hashing implementation. Additionally, we have performed performance analysis to measure the load distribution, throughput, and response times under various client load conditions.

The details of the testing and performance analysis can be found in the `README.md` file in the project's root directory.

##Experimental Reuslts
![Alt text]("C:\Users\Christine\Downloads\WhatsApp Image 2024-06-15 at 22.55.13.jpeg")

## Contributions
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open a new issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
