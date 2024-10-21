from main.models import Users
from decimal import Decimal

Users.objects.create(
    name='admins',
    balance=Decimal('100.00'),
    password="123321",
    age=18
)

print("Complete")