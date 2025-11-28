# Poker Advisor API


1) Executive Summary
Problem

The Probalem that we are looking to solve here with this app is that there are many poker players who are making the wrong descions or simply want to study the correct poker moves but are unsure. Current poker players are unable to compute all the different outcomes in their head as their are manyranges and different scernarios to acccount for.

Solution

Poker Advisor is a lightweight, easy to use service that will help poker players make the correct descions. This site is able to give players real time reccomendations based on thier hand equity simulatiosn and opppent range modeling. You simply enter youre cards and other varaibles the site is able to show you the correct descions to make based on youre expected value. The result is an easy-to-use tool that brings data-driven poker strategy to anyone, without needing technical or mathematical expertise.

2) System Overview
Course Concept(s)

  Docker/FAST API: Building a reproducible environment for the FastAPI application.

  Cloud (Azure): We deployed a containerized service using the azure Container apps.

  API/Webservices: We ran a https api that can accpet user inputs/ouputs that can run both locally and on cloud.

  Github: managing the workflow codebase using git workflows.


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



