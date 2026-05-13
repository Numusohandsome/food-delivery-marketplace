# System Architecture Diagram

```mermaid
flowchart LR
    User[Customer / User Browser] --> Frontend[React + Vite Frontend]

    Frontend --> Gateway[Nginx API Gateway]

    Gateway --> Backend1[FastAPI Backend Replica 1]
    Gateway --> Backend2[FastAPI Backend Replica 2]

    Backend1 --> PostgreSQL[(PostgreSQL Database)]
    Backend2 --> PostgreSQL

    Backend1 --> Redis[(Redis Cache)]
    Backend2 --> Redis

    Backend1 --> WebSocket[WebSocket Order Updates]
    Backend2 --> WebSocket

    Backend1 --> RateLimiter[Token Bucket Rate Limiter]
    Backend2 --> RateLimiter

    Backend1 --> BatchPipeline[Daily Settlement Batch Pipeline]
    Backend2 --> BatchPipeline

    BatchPipeline --> PostgreSQL

    Prometheus[Prometheus] --> Backend1
    Prometheus --> Backend2

    Grafana[Grafana Dashboard] --> Prometheus

    Promtail[Promtail] --> Loki[Loki Logs]
    Loki --> Grafana