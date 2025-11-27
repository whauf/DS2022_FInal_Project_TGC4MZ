# Poker Advisor API


1) Executive Summary
Problem

Most new and intermediate poker players struggle to make mathematically sound decisions during preflop and postflop situations. Human intuition is unreliable, and existing tools are either too complex or require expensive subscriptions. The problem is providing fast, accurate, and accessible probability-based poker advice for players who want to improve their game without needing to understand deep game theory.

Solution

Poker Advisor is a lightweight web application that uses simulated equity analysis, hand-range modeling, and probability calculations to give players real-time betting recommendations. The backend is built with FastAPI, packaged using Docker, and deployed as a cloud-hosted Azure Container App with a public, stable URL. Users enter their hole cards, opponent type, and betting situation, and the system returns win probability, expected value (EV), and an actionable “Fold / Call / Raise” recommendation. The project demonstrates system design, containerization, deployment, and cloud compute concepts in a beginner-friendly, production-style workflow.

2) System Overview
Course Concept(s)

This project uses several concepts from Systems I:

APIs & Microservices – FastAPI backend serving JSON responses

Containerization (Docker) – Reproducible runtime environments

Cloud Deployment – Azure Container Apps (managed environment + ACR)

Simulation & Modeling – Monte-Carlo equity simulations

Version Control & Reproducibility – GitHub repo hosting all files

                         ┌────────────────────────┐
                         │      User Browser      │
                         │ (poker-app URL on ACA) │
                         └───────────┬────────────┘
                                     │
                                     ▼
                        ┌───────────────────────────┐
                        │   Azure Container App      │
                        │  (FastAPI + Poker Logic)   │
                        └───────────┬────────────────┘
                                     │ pulls image
                                     ▼
                   ┌─────────────────────────────────────┐
                   │ Azure Container Registry (ACR)       │
                   │ pokerregistrywh.azurecr.io           │
                   └─────────────────────────────────────┘
                                     │ built from
                                     ▼
                     ┌────────────────────────────────┐
                     │       Docker Image (Local)      │
                     │ docker build → docker push      │
                     └────────────────────────────────┘
                                     │ uses
                                     ▼
                 ┌─────────────────────────────────────────┐
                 │ Poker Advisor Codebase                  │
                 │ FastAPI, equity sim, ranges, utils      │
                 └─────────────────────────────────────────┘


3) How to Run (Local)

Per the assignment template on page 2 of the PDF ("Choose Docker or Apptainer and provide a single command"

docker build -t poker-advisor .
docker run --rm -p 8000:8000 poker-advisor
curl http://localhost:8080/health

4) Design Decisions

(Only include if required—your assignment page shows “4) Design Decisions” on the next page.)

Key choices:

FastAPI for speed and interactive docs (/docs)

Monte-Carlo simulation instead of full GTO solver for speed/compute limits

Docker to ensure reproducibility across Macs and Azure’s Linux environment

Azure Container Apps over VM hosting for simplicity and automatic scaling

ACR + system-assigned identity for secure container pulls

5) Cloud Deployment (Extra Credit)

   az group create --name poker-rg --location northcentralus
az acr create --resource-group poker-rg --name pokerregistrywh --sku Basic
az acr login --name pokerregistrywh

docker build -t poker-advisor .
docker tag poker-advisor pokerregistrywh.azurecr.io/poker-advisor:v1
docker push pokerregistrywh.azurecr.io/poker-advisor:v1

az provider register --namespace Microsoft.App --wait
az provider register --namespace Microsoft.OperationalInsights --wait

az containerapp env create \
  --name poker-env \
  --resource-group poker-rg \
  --location northcentralus

az containerapp create \
  --name poker-app \
  --resource-group poker-rg \
  --environment poker-env \
  --image pokerregistrywh.azurecr.io/poker-advisor:v1 \
  --target-port 8000 \
  --ingress external \
  --registry-server pokerregistrywh.azurecr.io \
  --registry-identity system



