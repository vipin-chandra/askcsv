# CSV → PostgreSQL AI App

## Features
- Drag & drop CSV upload
- AI-based schema generation
- Automatic PostgreSQL table creation
- Bulk data insertion

## Setup

### Backend
cd backend
pip install -r requirements.txt

Run:
uvicorn main:app --reload

### Frontend
Open frontend/index.html in browser

## DB Setup
Create database in PostgreSQL:
CREATE DATABASE csv_ai;

Update credentials in db.py
``


 How to Run
1. Start PostgreSQL
Make sure DB exists:
CREATE DATABASE csv_ai;


2. Start Backend
cd backend 
uvicorn main:app --reload

3. Open Frontend
Just open:
frontend/index.html