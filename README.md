# AI Chatbot using Flask & Gemini AI

An AI-powered chatbot built using **Python**, **Flask**, **Google Gemini AI API**, **HTML**, **CSS**, and **JavaScript**. The chatbot accepts user queries through a web interface and generates intelligent responses using Google's Gemini AI model.

---

## Features

- AI-powered chatbot using Gemini AI
- Flask backend
- Responsive web interface
- REST API communication
- Docker support
- Ready for AWS EC2 deployment
- Easy to customize

---

## Technologies Used

- Python 3.12
- Flask
- HTML5
- CSS3
- JavaScript
- Google Gemini AI API
- Docker

---

# Installation

## Step 1: Clone the Repository

git clone https://github.com/your-username/AI-Chatbot.git

cd AI-Chatbot


---

## Step 2: Install Dependencies

ext
pip install -r requirements.txt


---

## Step 3: Configure Gemini API Key

Open **app.py**

Replace

python
API_KEY = "YOUR_GEMINI_API_KEY"
with
python
API_KEY = "YOUR_API_KEY"

---

## Step 4: Run the Flask Application

python app.py

---

## Step 5: Open the Application

Open your browser and visit

http://127.0.0.1:5000
or
http://localhost:5000


---

# Docker Deployment

## 1.Build Docker Image

docker build -t ai-chatbot .

---

## 2.Verify Docker Image

docker images

---

## 3.Run Docker Container

docker run -d -p 5000:5000 --name ai-chatbot-container ai-chatbot

---

## 4.Verify Running Container

docker ps

Expected output:

CONTAINER ID   IMAGE        STATUS       PORTS
xxxxxxxxxxxx   ai-chatbot   Up           0.0.0.0:5000->5000/tcp

---

## 5.View Container Logs

docker logs ai-chatbot-container

---

## 6.Stop Container

docker stop ai-chatbot-container

---

## 7.Remove Container

docker rm ai-chatbot-container

---

## 8.Remove Docker Image

docker rmi ai-chatbot


---

# AWS EC2 Deployment

1. Launch an Ubuntu EC2 Instance.
2. Connect using SSH.
3. Install Docker.
4. Copy the project to the EC2 instance.
5. Build the Docker image.
6. Run the Docker container.
7. Allow **Port 5000** in the EC2 Security Group.
8. Open your browser and visit: http://EC2-Public-IP:5000

---

# Application Workflow

User

   ↓

HTML + CSS + JavaScript

   ↓

Flask Backend (app.py)

   ↓

Google Gemini AI API

   ↓

Gemini AI Response

   ↓

Flask

   ↓

Browser Chat Interface


---

# Requirements

- Python 3.12+
- Flask
- Requests
- Gunicorn
- Docker Desktop
- Google Gemini API Key

---

# Output

The chatbot provides:

- Real-time AI conversations
- Responsive web interface
- Intelligent responses using Gemini AI
- Dockerized deployment
- Flask backend integration


