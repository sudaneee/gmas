from django.db import models
from src.models import Subject, StudentClass, Term, Student, Session
from djmoney.models.fields import MoneyField
import datetime

MODE_OF_PAYMENT = (
    ('NILL', 'NILL'),
    ('Bank-Transfer', 'Bank-Transfer'),
    ('Bank-Deposit', 'Bank-Deposit'),
    ('Cash-Deposit', 'Cash-Deposit')
)

GENDER = (
    ('NILL', 'NILL'),
    ('Male', 'Male'),
    ('Female', 'Female')
)

SECTION = (
    ('NILL', 'NILL'),
    ('Nursery', 'Nursery'),
    ('Primary', 'Primary'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior')
)

class FeesRecord(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    session = models.ForeignKey(Session, null=True, on_delete=models.SET_NULL)
    term = models.ForeignKey(Term, null=True, on_delete=models.SET_NULL)
    student_class = models.ForeignKey(
        StudentClass, null=True, on_delete=models.SET_NULL)
    payment_mode = models.CharField(
        max_length=100, choices=MODE_OF_PAYMENT, null=True, default='NILL')
    date = models.DateField(default=datetime.date.today)
    payment_purpose = models.CharField(max_length=200, null=True)
    amount_paid = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='NGN',
        max_digits=11,
    )

    def __str__(self):
        return str(self.student)

    class Meta:
        ordering = ('student_class', 'term',)

