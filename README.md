# Keep Them Alive 🌱

![CI/CD Status](https://github.com/yezcohen/keepthemalive/actions/workflows/ci.yml/badge.svg)

A full-stack, cloud-native web application designed to help people monitor and manage their home plants. The system features an automated, asynchronous notification system to remind users when and how much to water their plants, ensuring they stay healthy even when their owners are away.

**Live Demo:** [Link to be added once deployed]

---

## Core Features

* **Secure User Authentication:** Complete user registration and login system using a JWT-based authentication flow.
* **Plant Management:** A full CRUD (Create, Read, Update, Delete) API for managing a user's personal collection of plants.
* **Asynchronous Notifications:** An event-driven notification pipeline built with Kafka. A dedicated microservice checks watering schedules and publishes events, which are consumed by another service responsible for sending alerts.
* **Containerized Environment:** All application services (backend, frontend, database, message broker) are fully containerized with Docker for consistent and portable development and deployment.

---

## Tech Stack & Architecture

This project is built as a distributed system with a microservices-oriented architecture, leveraging a modern DevOps toolchain.

* **Backend:** Python, FastAPI, JWT (for authentication)
* **Frontend:** React
* **Database:** PostgreSQL
* **DevOps & Cloud:**
    * **Containerization:** Docker, Docker Compose
    * **Message Broker:** Apache Kafka
    * **CI/CD:** GitHub Actions (for automated linting and testing)
    * **Orchestration & Deployment:** Kubernetes, AWS (EKS, ECR)
* **Version Control:** Git

---

## Running the Project Locally

The entire application stack is orchestrated by Docker Compose, allowing you to run it with a single command.

### Prerequisites

* Git
* Docker Desktop

### Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yezcohen/keepthemalive.git](https://github.com/yezcohen/keepthemalive.git)
    cd keepthemalive
    ```

2.  **Create an environment file:**
    Create a `.env` file in the root directory and add a secret key for JWT signing. You can generate one with the following command:
    ```bash
    python -c 'import secrets; print(f"SECRET_KEY={secrets.token_hex(32)}")' > .env
    ```

3.  **Build and run the application:**
    ```bash
    docker compose up --build
    ```

4.  **Access the application:**
    * **Frontend:** `http://localhost:5173`
    * **Backend API (Swagger UI):** `http://localhost:8000/docs`

---

## Deployment & Architecture Strategy

This project was designed not only as a functional application but also as a learning platform to implement and demonstrate enterprise-grade deployment patterns.

#### Stage 1: Demonstration with Kubernetes (AWS EKS)

The initial deployment target is a managed **Kubernetes cluster on AWS (EKS)**. The goal of this stage is to:
* Demonstrate proficiency in container orchestration in a production-like environment.
* Manage a complex, multi-service application with industry-standard tooling.
* Implement best practices for scalability, resilience, and infrastructure as code.

All Kubernetes manifest files and deployment scripts used in this stage are included in the repository.

#### Stage 2: Cost-Optimized Live Version (Serverless)

While EKS is powerful, running a cluster 24/7 for a portfolio project is not cost-effective. Therefore, for the publicly accessible live version, the same container images are deployed to a **serverless container platform like AWS App Runner**.

This hybrid strategy demonstrates both the ability to handle complex, enterprise-level orchestration (Kubernetes) and the practical wisdom to choose cost-effective, "right-sized" solutions for a given use case.

---

## Project Roadmap

- [x] Backend API with user authentication.
- [x] Dockerization of all services.
- [x] CI pipeline with GitHub Actions.
- [x] Asynchronous notification system with Kafka.
- [ ] **(In Progress)** Initial deployment to AWS EKS cluster.
- [ ] Connect custom domain from GoDaddy.
- [ ] Implement WhatsApp notification service in the Kafka consumer.
- [ ] Develop frontend UI for user registration and login.
- [ ] Final, cost-optimized deployment for the live portfolio.