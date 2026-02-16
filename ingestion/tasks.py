import pandas as pd
from celery import shared_task
from customers.models import Customer
from loans.models import Loan

@shared_task
def ingest_customers(file_path):
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        Customer.objects.get_or_create(
            id=row["customer_id"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone_number": row["phone_number"],
                "monthly_salary": row["monthly_salary"],
                "approved_limit": row["approved_limit"],
                "current_debt": row["current_debt"]
            }
        )

@shared_task
def ingest_loans(file_path):
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        Loan.objects.create(
            id=row["loan_id"],
            customer_id=row["customer_id"],
            loan_amount=row["loan_amount"],
            tenure=row["tenure"],
            interest_rate=row["interest_rate"],
            monthly_installment=row["monthly_repayment"],
            emis_paid_on_time=row["EMIs paid on time"],
            start_date=row["start date"],
            end_date=row["end date"]
        )
