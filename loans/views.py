from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import date, timedelta

from customers.models import Customer
from .models import Loan
from .services import calculate_credit_score, calculate_emi


# ================================
# 🔹 Utility Function (Reusable)
# ================================

def evaluate_loan(customer, loan_amount, interest_rate, tenure):
    """
    Common loan approval logic used by both
    CheckEligibility and CreateLoan
    """

    credit_score = calculate_credit_score(customer)

    corrected_interest_rate = interest_rate
    approval = False

    if credit_score > 50:
        approval = True

    elif 30 < credit_score <= 50:
        approval = True
        corrected_interest_rate = max(interest_rate, 12)

    elif 10 < credit_score <= 30:
        approval = True
        corrected_interest_rate = max(interest_rate, 16)

    # EMI Burden Rule
    active_loans = Loan.objects.filter(customer=customer, is_active=True)
    current_emi_sum = sum(loan.monthly_installment for loan in active_loans)

    if current_emi_sum > 0.5 * customer.monthly_salary:
        approval = False

    if not approval:
        return False, None, None

    emi = calculate_emi(loan_amount, corrected_interest_rate, tenure)

    return True, corrected_interest_rate, emi


# =====================================
# 🔹 Check Loan Eligibility
# =====================================

class CheckEligibility(APIView):

    def post(self, request):

        try:
            customer_id = request.data.get("customer_id")
            loan_amount = float(request.data.get("loan_amount"))
            interest_rate = float(request.data.get("interest_rate"))
            tenure = int(request.data.get("tenure"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid or missing input fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        customer = get_object_or_404(Customer, id=customer_id)

        approval, corrected_rate, emi = evaluate_loan(
            customer, loan_amount, interest_rate, tenure
        )

        return Response({
            "customer_id": customer.id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_rate,
            "tenure": tenure,
            "monthly_installment": emi
        })


# =====================================
# 🔹 Create Loan
# =====================================

class CreateLoan(APIView):

    def post(self, request):

        try:
            customer_id = request.data.get("customer_id")
            loan_amount = float(request.data.get("loan_amount"))
            interest_rate = float(request.data.get("interest_rate"))
            tenure = int(request.data.get("tenure"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid or missing input fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        customer = get_object_or_404(Customer, id=customer_id)

        approval, corrected_rate, emi = evaluate_loan(
            customer, loan_amount, interest_rate, tenure
        )

        if not approval:
            return Response({
                "loan_id": None,
                "customer_id": customer.id,
                "loan_approved": False,
                "message": "Loan not approved",
                "monthly_installment": None
            })

        start_date = date.today()
        end_date = start_date + timedelta(days=30 * tenure)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=corrected_rate,
            tenure=tenure,
            monthly_installment=emi,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )

        customer.current_debt += loan_amount
        customer.save()

        return Response({
            "loan_id": loan.id,
            "customer_id": customer.id,
            "loan_approved": True,
            "message": "Loan approved successfully",
            "monthly_installment": emi
        }, status=status.HTTP_201_CREATED)


# =====================================
# 🔹 View Single Loan
# =====================================

class ViewLoan(APIView):

    def get(self, request, loan_id):

        loan = get_object_or_404(Loan, id=loan_id)
        customer = loan.customer

        return Response({
            "loan_id": loan.id,
            "customer": {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "tenure": loan.tenure,
            "start_date": loan.start_date,
            "end_date": loan.end_date
        })


# =====================================
# 🔹 View Customer Loans
# =====================================

class ViewCustomerLoans(APIView):

    def get(self, request, customer_id):

        loans = Loan.objects.filter(
            customer_id=customer_id,
            is_active=True
        )

        response_data = []

        for loan in loans:
            repayments_left = loan.tenure - loan.emis_paid_on_time

            response_data.append({
                "loan_id": loan.id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": repayments_left
            })

        return Response(response_data)
