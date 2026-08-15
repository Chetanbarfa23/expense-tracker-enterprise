# Expense Tracker Enterprise

A production-grade, containerized backend service demonstrating a complete cloud-native DevOps workflow — from source control to a live, auto-scaled deployment on AWS.

Built with **Flask**, containerized with **Docker**, provisioned with **Terraform**, and deployed to **Amazon EKS** through a fully automated, **test-gated Jenkins CI/CD pipeline**.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?logo=amazonaws&logoColor=white)](https://aws.amazon.com/)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [AWS Infrastructure](#aws-infrastructure)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Security](#security)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Health Check & Verification](#health-check--verification)
- [Key Concepts Demonstrated](#key-concepts-demonstrated)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

**Expense Tracker Enterprise** is a Flask-based REST API for tracking personal or organizational expenses, built to showcase real-world DevOps and cloud infrastructure practices rather than just application code.

The application handles:

- User registration and login
- JWT-based authentication and authorization
- Creating and retrieving expense records
- MySQL persistence via Amazon RDS
- File storage integration with Amazon S3

The focus of this repository is the **infrastructure and delivery pipeline** around the application: a push to `main` triggers Jenkins, which runs the automated test suite, and only on a passing suite does it build, containerize, and roll the change out to a live Kubernetes cluster on AWS.

---

## Architecture

```
Developer
   │  git push
   ▼
GitHub  ──(webhook)──▶  Jenkins
                            │
                         pytest
                            │
                     docker build
                            ▼
                       Amazon ECR
                            │
                       image pull
                            ▼
                       Amazon EKS
                            │
                     ┌──────┴──────┐
                     │             │
               Deployment         HPA
                     │
                     ▼
            LoadBalancer Service
                     │
                     ▼
                   User
                     │
                     ▼
               Amazon RDS
```

**Flow summary:** a push to GitHub triggers a webhook to Jenkins, which checks out the code, runs the pytest suite, and — only if all tests pass — builds and pushes a versioned Docker image to ECR, then rolls it out to EKS via a Kubernetes Deployment behind a LoadBalancer, with the Horizontal Pod Autoscaler managing capacity and RDS handling persistence.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL (Amazon RDS) |
| Authentication | JWT, bcrypt |
| Testing | pytest |
| Containerization | Docker |
| Container Registry | Amazon ECR |
| Orchestration | Kubernetes (Amazon EKS) |
| CI/CD | Jenkins |
| Infrastructure as Code | Terraform |
| Cloud Provider | AWS |
| Object Storage | Amazon S3 |
| Version Control | Git, GitHub |
| Load Balancing | Kubernetes Service / AWS ELB |
| Autoscaling | Kubernetes HPA |

---

## CI/CD Pipeline

Every push to `main` triggers the following automated sequence, with test execution gating the build and deployment stages:

| Step | Action |
|---|---|
| 1 | Developer pushes code to `main` |
| 2 | GitHub sends a push event through the configured webhook |
| 3 | Jenkins detects the change via the Multibranch Pipeline |
| 4 | Jenkins checks out the latest code |
| 5 | Jenkins verifies required tools |
| 6 | Jenkins runs the pytest automated test suite |
| 7 | Pipeline stops if any test fails |
| 8 | Jenkins builds the Docker image |
| 9 | Jenkins logs in to Amazon ECR |
| 10 | Jenkins pushes the versioned image to ECR |
| 11 | Jenkins updates the Kubernetes Secret |
| 12 | Jenkins applies the Kubernetes manifests |
| 13 | Jenkins updates the EKS Deployment with the new image |
| 14 | Kubernetes performs a rolling deployment |
| 15 | Jenkins waits for rollout completion |
| 16 | Jenkins performs a post-deployment health check |

**Test-gated builds:** if pytest fails, the pipeline stops immediately and the Docker build/deployment stages do not run. Only a passing test suite allows the pipeline to proceed to Docker build, ECR push, and EKS deployment.

**Image versioning example:**

```
Jenkins Build #28 → expense-tracker:28 → Amazon ECR → Amazon EKS
```

Each build is tagged with the Jenkins `BUILD_NUMBER`, enabling straightforward identification and rollback to any previous version.

---

## Testing

Automated testing is implemented with **pytest** and is enforced as a required gate in the Jenkins pipeline — the pipeline will not proceed to Docker build or deployment unless the full suite passes.

**Test directory:**

```
tests/
├── test_app.py
├── test_auth.py
└── test_expense.py
```

**Current coverage:**

- Application home endpoint
- Health endpoint
- Protected add-expense endpoint without JWT
- Protected get-expenses endpoint without JWT
- Protected update-expense endpoint without JWT
- Protected delete-expense endpoint without JWT
- User registration (success)
- User login (success)
- Get expenses (success)
- Add expense (success)
- Update expense (success)
- Delete expense (success)

The suite currently contains **12 tests**, all passing:

```bash
python -m pytest -v
```

```
12 passed
```

> Code coverage has not been measured for this project; no coverage percentage is claimed.

**Test-gated pipeline flow:**

```
Code Push
   ↓
Jenkins
   ↓
pytest
   ↓
Tests Pass?
  ↙       ↘
NO        YES
↓          ↓
STOP    Docker Build
```

If tests fail, Jenkins halts the pipeline before any Docker image is built or deployed, preventing untested code from reaching Amazon EKS.

---

## AWS Infrastructure

All infrastructure is provisioned and managed as code using **Terraform**, located in `terraform/`.

**Provisioned resources:**

- VPC with public and private subnets
- Internet Gateway and NAT Gateway
- Route tables and security groups
- Amazon EKS cluster and node groups
- Amazon ECR repository
- Amazon RDS (MySQL) instance
- Amazon S3 bucket
- IAM roles and policies

```bash
cd terraform
terraform init       # Initialize providers and backend
terraform validate   # Validate configuration syntax
terraform plan        # Preview infrastructure changes
terraform apply        # Provision infrastructure
```

> **Note:** Terraform state files and `.tfvars` files containing secrets are excluded from version control via `.gitignore`.

---

## Kubernetes Deployment

The application runs on Amazon EKS, defined by the manifests in `kubernetes/`:

```
kubernetes/
├── deployment.yaml               # Application Deployment spec
├── service.yaml                  # LoadBalancer Service
├── configmap.yaml                # Non-sensitive configuration
├── hpa.yaml                      # Horizontal Pod Autoscaler
├── persistent-volume.yaml        # Storage volume
└── persistent-volume-claim.yaml  # Volume claim binding
```

Kubernetes handles pod scheduling, service discovery, load balancing, configuration and secrets management, horizontal autoscaling, and rolling updates with zero downtime.

---

## Security

Security is treated as a first-class concern throughout the pipeline, not an afterthought.

**Secrets management flow:**

```
Jenkins Credentials → Jenkins Pipeline → Kubernetes Secret → Application Pod
```

- No credentials, API keys, or secrets are ever committed to GitHub
- `.env` is git-ignored; `.env.example` provides a safe reference template
- Terraform state files (`*.tfstate`) are git-ignored
- Terraform `.tfvars` files are git-ignored
- Python virtual environment directories are git-ignored
- Python cache files (`__pycache__`, `.pyc`) are git-ignored
- Database credentials and the JWT signing key are stored in Jenkins Credentials and injected at deploy time via Kubernetes Secrets
- AWS access is scoped through IAM roles

**Jenkins credentials used:**

```
github-pat
MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DB
JWT_SECRET_KEY
```

```bash
cp .env.example .env   # Set up local environment (never commit this file)
```

---

## Project Structure

```
expense-tracker-enterprise/
├── app/
│   ├── routes/                       # API route definitions
│   ├── services/                     # Business logic
│   └── models/                       # Database models
├── database/                         # DB schema / migrations
├── tests/                            # Automated pytest suite
│   ├── test_app.py
│   ├── test_auth.py
│   └── test_expense.py
├── kubernetes/                       # K8s manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── hpa.yaml
│   ├── persistent-volume.yaml
│   └── persistent-volume-claim.yaml
├── terraform/                        # Infrastructure as Code
│   ├── vpc.tf
│   ├── subnet.tf
│   ├── route-table.tf
│   ├── igw.tf
│   ├── nat-gateway.tf
│   ├── security-group.tf
│   ├── ec2.tf
│   ├── eks.tf
│   ├── ecr.tf
│   ├── rds.tf
│   └── iam.tf
├── Dockerfile
├── Jenkinsfile
├── docker-compose.yml
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

| Tool | Purpose |
|---|---|
| Python 3.11+ | Application runtime |
| Docker | Containerization |
| Git | Version control |
| AWS CLI | AWS resource management |
| kubectl | Kubernetes cluster interaction |
| Terraform | Infrastructure provisioning |

You will also need an AWS account with an ECR repository, an EKS cluster, an RDS database, and appropriate IAM permissions.

### Run Locally with Docker

```bash
# Build the image
docker build -t expense-tracker .

# Run the container
docker run -p 5000:5000 expense-tracker
```

### Run Tests Locally

Automated tests should pass locally before pushing code, since the same suite is enforced in Jenkins prior to deployment:

```bash
python -m pytest -v
```

Expected output:

```
12 passed
```

---

## Deployment

The normal deployment flow is fully automated through:

```
GitHub Webhook → Jenkins → pytest → Docker Build → Amazon ECR → Amazon EKS
```

Once the AWS infrastructure and Jenkins pipeline are configured, a push to `main` is sufficient to trigger the full pipeline:

```bash
git add .
git commit -m "Update application"
git push origin main
```

The GitHub webhook triggers the Jenkins Multibranch Pipeline, which checks out the code, runs the pytest suite, and — only if all tests pass — builds, publishes, and deploys the new image through the stages described above. If the test suite fails, the pipeline stops and no Docker image is built or deployed, so no untested code reaches Amazon EKS.

### Jenkins Configuration

The pipeline is defined in `Jenkinsfile` and requires access to GitHub, Docker, AWS CLI, ECR, kubectl, and EKS.

**Required Jenkins credentials:**

```
github-pat
MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DB
JWT_SECRET_KEY
```

---

## Health Check & Verification

Verify the deployment status directly through `kubectl`:

```bash
kubectl get pods
kubectl get deployment
kubectl get svc
kubectl get hpa
```

Once exposed via the AWS Load Balancer, confirm the application is live:

```bash
curl http://<LOAD_BALANCER_URL>
```

**Expected response:**

```json
{
  "message": "Expense Tracker Enterprise is running"
}
```

---

## Key Concepts Demonstrated

- Git & GitHub workflows with webhook-triggered automation
- Jenkins Multibranch CI/CD pipeline design
- Automated Testing with pytest
- Test-Gated CI/CD (deployment blocked on test failure)
- Docker image build and versioning strategy
- Amazon ECR image registry management
- Amazon EKS cluster operations
- Kubernetes Deployments, Services, ConfigMaps, and Secrets
- Rolling deployments with zero downtime
- Horizontal Pod Autoscaling
- Amazon RDS and Amazon S3 integration
- Terraform-based Infrastructure as Code
- IAM and Jenkins Credentials-based secrets management
- VPC networking (public/private subnets, NAT, IGW)
- AWS Load Balancer configuration
- Automated, test-gated deployment pipelines

---

## Future Improvements

The following are potential enhancements and are **not currently implemented**:

- Code coverage measurement and reporting
- Static code analysis (e.g. SonarQube)
- Container image vulnerability scanning (e.g. Trivy)
- Monitoring and observability (e.g. Prometheus, Grafana, CloudWatch)
- HTTPS/TLS termination
- Custom domain routing (e.g. Route 53)
- Blue/Green or Canary deployment strategies
- Automated rollback on failed health checks

---

## Author

**Chetan Barfa**

Electronics & Telecommunication Engineering Student

Focus areas: Cloud Computing · DevOps · AWS · Kubernetes · Terraform · CI/CD · IoT