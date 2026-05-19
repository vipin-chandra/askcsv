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



## DB Setup
Create database in PostgreSQL:
CREATE DATABASE <db name>;

Update credentials in db.py



 How to Run
1. Start PostgreSQL
Make sure DB exists:
CREATE DATABASE <db name>;


2. Start Backend
cd backend 
uvicorn main:app --reload

