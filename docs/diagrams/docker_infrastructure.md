# Docker Infrastructure Diagram

```mermaid
flowchart TB
    Internet[User Browser] --> Nginx[Nginx API Gateway<br/>Public Port: 80]

    Nginx --> Frontend[React Frontend Container<br/>Port: 5173]
    Nginx --> Backend1[FastAPI Backend Replica 1<br/>Port: 8001 -> 8000]
    Nginx --> Backend2[FastAPI Backend Replica 2<br/>Port: 8002 -> 8000]

    Backend1 --> Postgres[(PostgreSQL Container<br/>Host Port: 5433<br/>Container Port: 5432)]
    Backend2 --> Postgres

    Backend1 --> Redis[(Redis Container<br/>Port: 6379)]
    Backend2 --> Redis

    Prometheus[Prometheus Container<br/>Port: 9090] --> Backend1
    Prometheus --> Backend2

    Grafana[Grafana Container<br/>Port: 3000] --> Prometheus
    Grafana --> Loki

    Promtail[Promtail Container] --> Loki[Loki Container<br/>Port: 3100]

    subgraph DockerCompose[Docker Compose Network]
        Nginx
        Frontend
        Backend1
        Backend2
        Postgres
        Redis
        Prometheus
        Grafana
        Loki
        Promtail
    end
```

## Description

This diagram shows the Docker Compose infrastructure of the food-delivery marketplace. The system is started with Docker Compose and contains frontend, backend replicas, database, cache, gateway, and observability containers. Nginx is used as the single public entry point on port 80. It routes frontend, REST API, and WebSocket traffic. PostgreSQL uses host port 5433 because port 5432 was occupied on the local machine, while inside Docker it still uses port 5432.