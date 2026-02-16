import math
from .models import Loan
from customers.models import Customer
from datetime import datetime

def calculate_emi(principal, annual_interest_rate, tenure_months):
    monthly_rate = annual_interest_rate / (12 * 100)
    
    emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months) / \
          (math.pow(1 + monthly_rate, tenure_months) - 1)
    
    return round(emi, 2)
def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)

    score = 100

    # 1️⃣ If current debt exceeds approved limit → score = 0
    if customer.current_debt > customer.approved_limit:
        return 0

    total_loans = loans.count()

    if total_loans > 5:
        score -= 20

    # 2️⃣ Past EMIs paid on time
    for loan in loans:
        if loan.emis_paid_on_time < loan.tenure:
            score -= 5

    # 3️⃣ Loan activity this year
    current_year = datetime.now().year
    recent_loans = loans.filter(start_date__year=current_year).count()
    if recent_loans > 2:
        score -= 10

    # 4️⃣ Loan volume
    total_loan_amount = sum([loan.loan_amount for loan in loans])
    if total_loan_amount > customer.approved_limit:
        score -= 20

    return max(score, 0)
def evaluate_loan(customer, loan_amount, interest_rate, tenure):
    credit_score = calculate_credit_score(customer)

    approval = False
    corrected_interest_rate = interest_rate

    if credit_score > 50:
        approval = True

    elif 30 < credit_score <= 50:
        approval = True
        corrected_interest_rate = max(interest_rate, 12)

    elif 10 < credit_score <= 30:
        approval = True
        corrected_interest_rate = max(interest_rate, 16)

    else:
        approval = False

    if not approval:
        return {
            "approved": False,
            "corrected_interest_rate": None,
            "emi": None
        }

    emi = calculate_emi(loan_amount, corrected_interest_rate, tenure)

    return {
        "approved": True,
        "corrected_interest_rate": corrected_interest_rate,
        "emi": emi
    }
