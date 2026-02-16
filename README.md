# Overview

This project is a backend implementation of a Credit Approval System designed to evaluate customer creditworthiness and manage loan approvals based on historical and real-time financial data.
The system is built using Django and Django Rest Framework, uses PostgreSQL as the primary database, supports asynchronous background data ingestion, and is fully containerized using Docker.
All services can be started using a single Docker Compose command, as required by the assignment.
The application exposes REST APIs only; no frontend is included.

# Key Capabilities

Customer registration with automatic credit limit calculation
Credit score computation based on historical loan behavior
Loan eligibility evaluation with rule-based interest correction
Loan creation and customer debt tracking
Retrieval of individual loan details
Retrieval of all active loans for a customer

# Technology Stack

Python 3.11
Django 5+
Django Rest Framework
PostgreSQL
Celery & Redis (background processing)
Pandas (Excel ingestion)
Docker & Docker Compose

# System Architecture

Customers App
Handles customer registration and stores customer financial profiles.

Loans App
Contains all loan logic, including credit score calculation, eligibility evaluation, loan creation, and retrieval APIs.

Ingestion App
Handles asynchronous ingestion of historical customer and loan data using background workers.

Services Layer
Business logic such as credit scoring, EMI calculation, and loan evaluation is isolated from views to ensure clean architecture and maintainability.

# Data Models

Customer
Stores customer identity and financial profile.

Fields:
first_name
last_name
age
phone_number
monthly_salary
approved_limit
current_debt

Approved credit limit is calculated as:
approved_limit = round(36 × monthly_salary to the nearest lakh)

# Loan

Represents a loan issued to a customer.

Fields:
customer (foreign key)
loan_amount
interest_rate
tenure (months)
monthly_installment
emis_paid_on_time
start_date
end_date
is_active

# Credit Score and Eligibility Logic

Each customer is assigned a credit score out of 100, computed using:
Past EMIs paid on time
Number of loans taken historically
Loan activity in the current year
Total approved loan volume
Current debt exceeding approved credit limit (score becomes 0)
EMI burden exceeding 50% of monthly salary (automatic rejection)

# Interest Rate Rules

 Credit Score Range   Decision                           

 > 50                 Loan approved                      
 30 – 50              Approved with minimum 12% interest 
 10 – 30              Approved with minimum 16% interest 
 < 10                 Loan rejected                      

If the requested interest rate does not match the required slab, the system automatically corrects it and returns the corrected rate in the response.

# API Endpoints

# Register Customer

POST /register
Registers a new customer and calculates the approved credit limit.

# Check Loan Eligibility

POST /check-eligibility
Evaluates whether a customer is eligible for a loan based on credit score and EMI burden.
This endpoint does not create a loan record.

# Create Loan

POST /create-loan
Creates a loan only if eligibility criteria are satisfied and updates the customer’s current debt.

# View Loan by ID

GET /view-loan/<loan_id>
Returns loan details along with basic customer information.

# View Loans by Customer

GET /view-loans/<customer_id>
Returns all active loans for a customer, including remaining repayments.

# Background Data Ingestion

Historical data provided in Excel format is ingested asynchronously using Celery background workers.
customer_data.xlsx
loan_data.xlsx
This ensures that large data ingestion does not block the application startup and follows scalable backend design principles.

# Dockerized Setup

The entire system is containerized, including:
Django application
PostgreSQL database
Redis
Celery worker

Run the Application
From the project root:

docker compose up --build

This single command:
Builds the application image
Starts the database and cache
Runs migrations
Starts the web server and background workers

The API becomes available at:
http://localhost:8000

# Project Quality and Design Notes

Business logic is separated from views using a service layer.
APIs follow REST principles with proper error handling.
The system is designed to be scalable and production-ready.
Docker Compose ensures consistent setup across environments.

# Author
Abhijeet Bagal
https://github.com/abhijeet8896
