-> Project Overview

This repository contains the backend service for BusBee, a smart bus discovery and booking platform designed to help users find buses in unfamiliar locations.

The backend is responsible for:

. Handling business logic

. Managing authentication

. Communicating with MongoDB Atlas

. Exposing REST APIs for the frontend

. Built using Flask with a modular blueprint architecture, and deployed on Render.

Key Features

. JWT-based authentication

. Bus search and listing APIs

. Ticket booking management

. Payment handling endpoints

. Chatbot integration APIs

. Translation support

. Notification handling

. MongoDB Atlas database integration

. Health check endpoint for monitoring

 Tech Stack

Language: Python 3

Framework: Flask

Database: MongoDB Atlas

Authentication: JWT

Server: Gunicorn

Deployment Platform: Render

📂 Project Structure
backend/
├── routes/
│   ├── auth.py
│   ├── bus.py
│   ├── booking.py
│   ├── payment.py
│   ├── chatbot.py
│   ├── translate.py
│   └── notification.py
├── models/
├── utils/
├── uploads/
├── app.py
├── requirements.txt
├── .env
└── .gitignore

 API Endpoints Overview
Method	Endpoint	Description
GET	/api/health	Backend health check
POST	/api/auth/*	Authentication routes
GET	/api/buses	Fetch available buses
POST	/api/bookings	Create and manage bookings
POST	/api/payments	Handle payments
POST	/api/chatbot	Chatbot interactions
POST	/api/translate	Translation service
POST	/api/notifications	User notifications

 Environment Variables
Required (Render)

Add the following in Render → Environment Variables:

MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/busbee
JWT_SECRET=your_secure_random_string
TRANSLATION_API_KEY=your_translation_api_key

Optional (Recommended)
JWT_EXPIRE_MINUTES=60
PDF_STORAGE_PATH=/opt/render/project/src/uploads
FLASK_ENV=production
DEBUG=False


-> Never commit .env to GitHub

 Run Backend Locally
git clone <backend-repo-url>
cd backend
pip install -r requirements.txt
python app.py


Backend will run at:

http://127.0.0.1:5000

 Deployment (Render)
Build Command
pip install -r requirements.txt

Start Command
gunicorn app:app


Render automatically:

Detects Python

Runs Gunicorn

Exposes public API URL

 Testing

Check backend status using:

GET /api/health


Expected response:

{
  "status": "ok"
}



-> License

This project is developed for academic, learning, and demonstration purposes.
