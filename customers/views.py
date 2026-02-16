from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer

class RegisterCustomer(APIView):

    def post(self, request):
        data = request.data

        if not data.get("monthly_income"):
            return Response(
                {"error": "monthly_income is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            salary = int(data.get("monthly_income"))

            approved_limit = round((36 * salary) / 100000) * 100000

            customer = Customer.objects.create(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                age=data.get("age"),
                phone_number=data.get("phone_number"),
                monthly_salary=salary,
                approved_limit=approved_limit
            )

            return Response({
                "customer_id": customer.id,
                "name": f"{customer.first_name} {customer.last_name}",
                "age": customer.age,
                "monthly_income": customer.monthly_salary,
                "approved_limit": customer.approved_limit,
                "phone_number": customer.phone_number
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
