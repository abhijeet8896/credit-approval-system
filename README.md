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

Background ingestion of historical data from Excel files

Fully dockerized setup (application, database, cache, workers)
