## VPS Deployment

This section explains how to deploy the project on a remote VPS using Docker Compose.

### Server requirements

- Ubuntu 22.04 or newer
- Docker
- Docker Compose
- Git
- Open ports: 80, 3000, 9090

### 1. Connect to the VPS

```bash
ssh username@server_ip
```

Example:

```bash
ssh root@123.123.123.123
```

### 2. Update the server

```bash
sudo apt update
sudo apt upgrade -y
```

### 3. Install Docker

```bash
sudo apt install -y ca-certificates curl gnupg git
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 4. Check Docker installation

```bash
docker --version
docker compose version
```

### 5. Clone the repository

```bash
git clone https://github.com/Numusohandsome/food-delivery-marketplace.git
cd food-delivery-marketplace
```

### 6. Create environment file

```bash
cp .env.example .env
```

If needed, edit the `.env` file:

```bash
nano .env
```

### 7. Start the application

```bash
docker compose up -d --build
```

### 8. Check running containers

```bash
docker compose ps
```

Expected services:

- postgres
- redis
- backend1
- backend2
- frontend
- nginx
- prometheus
- grafana

### 9. Open the deployed application

Replace `SERVER_IP` with the real VPS IP address.

| Service | URL |
|---|---|
| Frontend through Nginx Gateway | `http://SERVER_IP` |
| Backend Swagger Docs | `http://SERVER_IP/docs` |
| Backend API | `http://SERVER_IP/api/restaurants` |
| Prometheus | `http://SERVER_IP:9090` |
| Grafana | `http://SERVER_IP:3000` |

### 10. Stop the application

```bash
docker compose down
```

### 11. View logs

All services:

```bash
docker compose logs -f
```

Specific service:

```bash
docker compose logs -f nginx
docker compose logs -f backend1
docker compose logs -f backend2
docker compose logs -f postgres
docker compose logs -f redis
```

### 12. Restart after code changes

```bash
git pull origin main
docker compose down
docker compose up -d --build
```

### Deployment notes

- Nginx is the single public entry point for the application.
- Backend traffic is load balanced between `backend1` and `backend2`.
- PostgreSQL data is stored in a named Docker volume.
- Redis data is stored in a named Docker volume.
- Prometheus collects backend metrics from `/metrics`.
- Grafana is used for dashboards and observability.