# Tiendify - Shops Backend REST API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![Prisma](https://img.shields.io/badge/Prisma-3982CE?style=for-the-badge&logo=Prisma&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

FastAPI application to serve as Shop-specific API backend for Tiendify project. This is the API that [Tiendify Backend](https://github.com/L2G-Solutions/tiendify-backend) forwards requests to, and also the backend that is integrated by customer own web pages.

## Developed by

![GitHub contributors](https://img.shields.io/github/contributors/L2G-Solutions/tiendify-shop-backend?style=for-the-badge)

- [Daniel Lujan Agudelo](https://github.com/daniel-lujan)
- [Jose David Gómez Muñetón](https://github.com/josegmez)

## Quickstart

> [!IMPORTANT]
> You need to have Docker installed on your machine.

### Step 1. Clone the repository

```bash
git clone https://github.com/L2G-Solutions/tiendify-shop-backend.git
cd tiendify-shop-backend
```

### Step 2. Create an Environment File

Create the file:

```bash
touch .env
```

Then, populate it with the required [Environment Variables](#environment-variables).

### Step 3. Start the application

```bash
docker-compose up --env-file .env -d
```

### Step 4. Access the API

The API will be available at `http://localhost:8000`. Check health status by running:

```bash
curl http://localhost:8000/health
```

Or access the Swagger UI at `http://localhost:8000/docs`.

## Environment Variables

The following environment variables are required to run the application:

- `PROJECT_NAME`
- `DATABASE_URL`
- `AZURE_STORAGE`
- `AZURE_PUBLIC_CONTAINER`
- `SECRET_KEY`
- `KEYCLOAK_URL`
- `KEYCLOAK_CLIENT_ID`
- `KEYCLOAK_REALM`
- `KEYCLOAK_CLIENT_SECRET`
