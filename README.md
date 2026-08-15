# Expense Tracker Enterprise

[![CI](https://github.com/Chetanbarfa23/expense-tracker-enterprise/actions/workflows/ci.yml/badge.svg)](https://github.com/Chetanbarfa23/expense-tracker-enterprise/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CD-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?logo=amazonaws&logoColor=white)](https://aws.amazon.com/)

A containerized Flask backend demonstrating a real cloud-native DevOps workflow: **GitHub Actions** runs continuous integration (automated tests) on every push, and **Jenkins** handles continuous delivery — building the Docker image, pushing it to Amazon ECR, and deploying it to Amazon EKS.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Testing / Automated Testing](#testing--automated-testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [GitHub Actions CI](#github-actions-ci)
- [Jenkins CD Pipeline](#jenkins-cd-pipeline)
- [AWS Infrastructure](#aws-infrastructure)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Security](#security)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Local Testing](#local-testing)
- [Docker](#docker)
- [Deployment](#deployment)
- [Health Check & Verification](#health-check--verification)
- [Key DevOps Concepts Demonstrated](#key-devops-concepts-demonstrated)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

**Expense Tracker Enterprise** is a Flask-based REST API for tracking expenses, built primarily to demonstrate a production-style CI/CD and cloud infrastructure workflow rather than as a feature-heavy application.

The application provides:

- User registration and login
- JWT-based authentication and authorization
- Password hashing with bcrypt
- Creating, retrieving, updating, and deleting expense records
- MySQL persistence via Amazon RDS
- File storage integration with Amazon S3

The repository is structured around two separate, purpose-built automation systems: **GitHub Actions** validates every code change through automated testing, and **Jenkins** owns the actual build-and-deploy pipeline to AWS.

---

## Architecture

```
Developer
   │  git push
   ▼
GitHub ──(webhook)──▶ Jenkins
   │                     │
   ▼                  pytest
GitHub Actions            │
   │                Docker Build
 pytest                   │
                     Amazon ECR
                           │
                     Amazon EKS
                           │
                 Kubernetes Rolling
                     Deployment
                           │
                    LoadBalancer
                           │
                   Flask Application
                           │
                      Amazon RDS
```

**Flow summary:** every push to GitHub triggers two independent things — GitHub Actions runs the pytest suite as a CI check on the commit, and a webhook separately notifies Jenkins, which runs the same test suite as a deployment gate before building the Docker image, pushing it to ECR, and rolling it out to EKS behind a LoadBalancer, with RDS handling persistence.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MySQL (Amazon RDS) |
| Authentication | JWT, bcrypt |
| Testing | pytest |
| Continuous Integration | GitHub Actions |
| Continuous Delivery | Jenkins |
| Containerization | Docker |
| Container Registry | Amazon ECR |
| Orchestration | Kubernetes (Amazon EKS) |
| Infrastructure as Code | Terraform |
| Cloud Provider | AWS |
| Object Storage | Amazon S3 |
| Version Control | Git, GitHub, GitHub Webhooks |
| Load Balancing | Kubernetes Service / AWS ELB |
| Autoscaling | Kubernetes HPA |

---

## Testing / Automated Testing

Automated tests are written with **pytest** and live in `tests/`. They are executed both as a CI check (GitHub Actions) and as a deployment gate (Jenkins) before any Docker image is built.

**Test directory:**

```
tests/
├── test_app.py
├── test_auth.py
└── test_expense.py
```

**Coverage includes:**

- Flask home endpoint
- Health endpoint
- JWT-protected expense endpoints
- Authentication-related behavior (registration, login)
- Expense operations (create, read, update, delete)

**Run locally:**

```bash
python -m pytest -v
```

**Current result:**

```
12 passed
```

> Code coverage has not been measured; no coverage percentage is claimed.

---

## CI/CD Pipeline

This project intentionally separates **CI** from **CD** using two different tools:

| System | Responsibility |
|---|---|
| **GitHub Actions** | Continuous Integration — validates every push by running automated tests. Does **not** build or deploy anything. |
| **Jenkins** | Continuous Delivery — re-runs tests as a gate, then builds the Docker image, pushes it to ECR, and deploys it to EKS. |

GitHub Actions and Jenkins are not deploying the application independently — GitHub Actions is a validation check on the code, while Jenkins is the only system that actually builds, publishes, and deploys it.

---

## GitHub Actions CI

Defined in `.github/workflows/ci.yml`, this workflow runs on every push and pull request.

**Steps:**

1. Checkout repository (`actions/checkout@v5`)
2. Set up Python 3.11 (`actions/setup-python@v6`)
3. Install dependencies from `requirements.txt`
4. Run the pytest suite
5. Run a Python syntax check with `compileall`

The workflow currently passes successfully and does not build or push any Docker image — its sole purpose is fast feedback on code correctness.

---

## Jenkins CD Pipeline

Defined in `Jenkinsfile`, this pipeline owns the actual build and deployment process and runs after a GitHub webhook notifies Jenkins of a push to `main`.

| Step | Action |
|---|---|
| 1 | Verify workspace |
| 2 | Print build information |
| 3 | Verify required tools |
| 4 | Run automated pytest tests |
| 5 | Build the Docker image |
| 6 | Verify the built Docker image |
| 7 | Log in to Amazon ECR |
| 8 | Push the Docker image to Amazon ECR |
| 9 | Create or update Kubernetes Secrets |
| 10 | Apply Kubernetes manifests |
| 11 | Update the EKS Deployment image |
| 12 | Perform a rolling deployment |
| 13 | Check rollout status |
| 14 | Run a Kubernetes health check |
| 15 | Clean up local Docker images |

**Test-gated builds:** if pytest fails at step 4, the pipeline stops and no Docker image is built, pushed, or deployed.

**Image versioning example:**

```
Jenkins Build #28 → expense-tracker:28 → Amazon ECR → Amazon EKS
```

Each build is tagged with the Jenkins `BUILD_NUMBER`, enabling straightforward identification and rollback to any previous version.

---

## AWS Infrastructure

All infrastructure is provisioned as code with **Terraform**, located in `terraform/`.

**Services used:**

- VPC with public and private subnets
- Internet Gateway and NAT Gateway
- Route tables and security groups
- Amazon EC2
- Amazon EKS
- Amazon ECR
- Amazon RDS (MySQL)
- Amazon S3
- IAM

```bash
cd terraform
terraform init       # Initialize providers and backend
terraform validate   # Validate configuration syntax
terraform plan        # Preview infrastructure changes
terraform apply        # Provision infrastructure
```

> Terraform state files and `.tfvars` files containing sensitive values are excluded from version control via `.gitignore`.

---

## Kubernetes Deployment

The application runs on Amazon EKS using the manifests in `kubernetes/`:

```
kubernetes/
├── deployment.yaml               # Application Deployment
├── service.yaml                  # LoadBalancer Service
├── configmap.yaml                # Non-sensitive configuration
├── hpa.yaml                      # Horizontal Pod Autoscaler
├── persistent-volume.yaml        # Storage volume
└── persistent-volume-claim.yaml  # Volume claim binding
```

Application secrets (database credentials, JWT key) are managed through a Kubernetes **Secret**, created and updated by the Jenkins pipeline rather than committed to the repository.

Kubernetes handles pod scheduling, service discovery, load balancing, configuration/secret injection, horizontal autoscaling, and rolling updates.

---

## Security

- `.env` is used for local secrets and is excluded from Git via `.gitignore`
- `.env.example` is committed as a safe configuration template
- Terraform state files (`*.tfstate`) and `.tfvars` files are excluded from Git
- Python virtual environment directories are git-ignored
- Python cache files (`__pycache__`, `.pyc`) are git-ignored
- Database credentials and the JWT signing key are stored in **Jenkins Credentials** and injected at deploy time
- Application secrets at runtime are managed through **Kubernetes Secrets**
- AWS access is scoped through **IAM**

**Secrets flow:**

```
Jenkins Credentials → Jenkins Pipeline → Kubernetes Secret → Application Pod
```

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
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI workflow
├── app/
│   ├── routes/                       # API route definitions
│   ├── services/                     # Business logic
│   └── models/                       # Database models
├── database/                         # DB schema / migrations
├── tests/                            # pytest test suite
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

### Local Setup

```bash
git clone https://github.com/Chetanbarfa23/expense-tracker-enterprise.git
cd expense-tracker-enterprise
cp .env.example .env
pip install -r requirements.txt
python run.py
```

---

## Local Testing

Tests should pass locally before pushing, since the same suite runs in both GitHub Actions and Jenkins:

```bash
python -m pytest -v
```

Expected output:

```
12 passed
```

---

## Docker

```bash
# Build the image
docker build -t expense-tracker .

# Run the container
docker run -p 5000:5000 expense-tracker
```

---

## Deployment

Deployment to AWS is automated through Jenkins after a push to `main`:

```bash
git add .
git commit -m "Update application"
git push origin main
```

This triggers two things:

1. **GitHub Actions** runs automated tests as a CI check on the commit.
2. **The GitHub webhook** notifies **Jenkins**, which independently re-runs the tests, then — only if they pass — builds the Docker image, pushes it to Amazon ECR, and deploys it to Amazon EKS.

If tests fail in Jenkins, the pipeline stops before any image is built or deployed.

---

## Health Check & Verification

The application exposes two endpoints used for verification:

- `GET /` — application root
- `GET /health` — health check

**Verify the Kubernetes deployment:**

```bash
kubectl get pods
kubectl get deployment
kubectl get svc
kubectl get hpa
```

**Verify the running application** (replace with your current LoadBalancer URL, as this changes whenever the infrastructure is redeployed):

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

## Key DevOps Concepts Demonstrated

- Git, GitHub, and GitHub Webhooks
- Continuous Integration with GitHub Actions
- Continuous Delivery with Jenkins
- Separation of CI and CD responsibilities across tools
- Automated testing with pytest as a deployment gate
- Docker image build and versioning strategy
- Amazon ECR image registry management
- Amazon EKS cluster operations
- Kubernetes Deployments, Services, ConfigMaps, Secrets
- Rolling deployments
- Horizontal Pod Autoscaling
- Amazon RDS and Amazon S3 integration
- Terraform-based Infrastructure as Code
- IAM and Jenkins Credentials-based secrets management
- VPC networking (public/private subnets, NAT, IGW)
- AWS Load Balancer configuration

---

## Future Improvements

The following are realistic next steps and are **not currently implemented**:

- Frontend application (currently backend/API only)
- HTTPS with a custom domain name
- Monitoring and observability (e.g. Prometheus, Grafana, CloudWatch)
- Advanced security scanning (e.g. Trivy, SonarQube)
- More advanced deployment strategies (e.g. Blue/Green, Canary)
- Infrastructure delivery via ArgoCD or Helm

---

## Author

**Chetan Barfa**

Electronics & Telecommunication Engineering Student

Focus areas: Cloud Computing · DevOps · AWS · Kubernetes · Terraform · CI/CD · IoT