# Poker Advisor API


1) Executive Summary
Problem

The ploblem that we are looking to solve here with this app is that there are many poker players who are making the wrong decisions or simply want to study the correct poker moves but are unsure. Current poker players are unable to compute all the different outcomes in their head as their are many ranges and different scenarios to acccount for.

Solution

Poker Advisor is a lightweight, easy to use service that will help poker players make the correct decisions. This site is able to give players real time recomendations based on their hand equity simulations and oppenent range modeling. You simply enter youre cards and other variables the site is able to show you the correct decisions to make based on your expected value. The result is an easy-to-use tool that brings data-driven poker strategy to anyone, without needing technical or mathematical expertise.

2) System Overview
Course Concept(s)

  Docker/FAST API: Building a reproducible environment for the FastAPI application.

  Cloud (Azure): We deployed a containerized service using the azure Container apps.

  API/Webservices: We ran a https api that can accept user inputs/outputs that can run both locally and on cloud.

  Github: managing the workflow codebase using git workflows.

 DATA:
   PreFlop hand ranges (Data/ranges/*json): this proves categorized hand groups, JSON, ~5 KB total

   Simulation assets(random/*tests/*): Used for equity testing and opponent range, JSON plus Python scripts used, simulation < 10 KB

  Card images: Local image used for display and testing, PNG/JPG used, < 100 KB

  There were not external datasets used. All the game logic was programmed generated.

MODELS:
  eval7 Poker engine: Computes card equity, hand strength, and simulates outcomes using Monte-Carlo permutation. Used python, MIT License

  Custom preflop decision model: Uses grouping logic + equity simulation to recommend fold/call/raise. Uses python, self developed 

  Range loader: Cleans card inputs, validates rank/suit, loads JSON range files. It uses python, self developed

  Equity Simulation: Runs random opponent simulations to estimate win probability. Uses a mix of eval7 backend and python, MIT with a mix of self development

SERVICES:

  FastAPI on the backend: Reproved rest for endpoints: hand input, equity, calculations, preflop advice

  Azure Container Apps: Cloud deployment environment for the containerized API

  Azure Container Registry (ACR): Stores Docker image (poker-advisor:v1) built from project Dockerfile

  HTML Front-End UI: Simple web interface for sending hand input to API

  Docker Runtime: Provides reproducible environment, dependencies, and server configuration

  
3) How to Run (Local)

Before Running code make sure youre Docker app is open.

docker build -t poker-advisor:latest .
docker run -p 8000:8000 poker-advisor:latest

You should see 
http://localhost:8000
Once you see this you can copy into browser to use locally.

Health test (Optional)
Visit this page but typing into local browser
http://localhost:8000/docs


4) Design Decisions

(Only include if required—your assignment page shows “4) Design Decisions” on the next page.)

Key choices:

FastAPI for speed and interactive docs (/docs)

Monte-Carlo simulation instead of full GTO solver for speed/compute limits

Docker to ensure reproducibility across Macs and Azure’s Linux environment

Azure Container Apps over VM hosting for simplicity and automatic scaling

ACR + system-assigned identity for secure container pulls

5) Cloud Deployment (Extra Credit)

Log Into Azure 
  az login

Create Resource Group
  az group create --name poker-test-rg --location northcentralus

Create Azure Container Registry (ACR)

  az acr create \
    --resource-group poker-test-rg \
    --name pokerregistrytestwh \
    --sku Basic \
    --location northcentralus
    
Log in to the new registry

  az acr login --name pokerregistrytestwh

Build + Tag + Push Docker image

  docker build -t poker-advisor-test .

  docker tag poker-advisor-test pokerregistrytestwh.azurecr.io/poker-advisor:v2

  docker push pokerregistrytestwh.azurecr.io/poker-advisor:v2

Ensure required Azure providers

  az provider register --namespace Microsoft.App --wait
  az provider register --namespace Microsoft.OperationalInsights --wait

Create a NEW Container App environment

  az containerapp env create \
    --name poker-test-env \
    --resource-group poker-test-rg \
    --location northcentralus

Deploy the app
  az containerapp create \
    --name poker-test-app \
    --resource-group poker-test-rg \
    --environment poker-test-env \
    --image pokerregistrytestwh.azurecr.io/poker-advisor:v2 \
    --target-port 8000 \
    --ingress external \
    --registry-server pokerregistrytestwh.azurecr.io \
    --registry-identity system

Get the Pulbic URL
    az containerapp show \
      --name poker-test-app \
      --resource-group poker-test-rg \
      --query properties.configuration.ingress.fqdn \
      --output tsv

Will Output Something like this
  poker-test-app.redcoast-xxxxxx.northcentralus.azurecontainerapps.io





  

