from django.shortcuts import render, redirect
from django.http import HttpResponse
from src.models import Subject, StudentClass, Session, Term, Student, StudentResult, StudentBehaviouralAssessment, signature, sets
from .models import FeesRecord
from django.db import connection
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User, auth
import openpyxl
from openpyxl import Workbook
import datetime
# from openpyxl.writer.excel import save_virtual_workbook
# from eval.models import General_Info, General_Questions
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from collections import Counter
from djmoney.money import Money
def fees_index(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.username == 'sudaniy':
            if "next" in request.POST:
                auth.login(request, user)
                return redirect(request.POST.get("next"))
            else:
                return redirect('/fees-record/fees_activation')

        else:
            if user is None:
                messages.error(request, "Incorrect Login-in Details")
            else:
                messages.error(
                    request, 'You are not authorized to Visit this page')

            return render(request, 'fees/index.html')

    else:
        return render(request, "fees/index.html")


@login_required(login_url='/fees-record')
def fees_activation(request):
    if request.method == 'POST':
        registration_number = request.POST['reg_no']
        session = request.POST['session']
        term = request.POST['term']
        payment_purpose = request.POST['purpose']
        amount_paid = request.POST['amount_paid']
        payment_mode = request.POST['payment_mode']


        # getting Student Information
        student_id = int(registration_number)
        student = Student.objects.get(id=student_id)
        
        
        FeesRecord.objects.create(
            student = student,
            student_class = StudentClass.objects.get(id=student.student_class.id),
            session = Session.objects.get(session_name=session),
            term = Term.objects.get(term_name=term),
            payment_purpose = payment_purpose,
            amount_paid = Money(amount_paid, 'NGN'),
            payment_mode = payment_mode

        )

        messages.success(request, "Fees Has Been Recorded Successfully")
        return redirect('/fees-record/fees_activation')

    else:
        term = Term.objects.all()
        session = Session.objects.all()
        student_class = StudentClass.objects.all()

        context = {
            'term': term,
            'session': session,
            'class': student_class,
        }

        return render(request, "fees/fees_activation.html", context)


@login_required(login_url='/fees-record')
def fees_record(request):

    # ================Getting Session===========
    if request.method == 'POST':
        session = request.POST['session']
        fees_record = FeesRecord.objects.filter(session=Session.objects.get(session_name=session)).all()

        context = {
            'fees_record': fees_record,
            
        }
        
        
        return render(request, "fees/fees_record.html", context)
    else:
        session = Session.objects.all()
        context = {
            'session': session,
        }

        return render(request, "fees/fees_record1.html", context)

    # results =  Fees_Breakdown_Record.objects.all()
    # desc0 = []
    # amount1 =[]
    # count1 = []

    
    

    # for result in results:
    #     amount = 0
    #     count = 0
        
    #     for desc in results:
    #         if desc.description == result.description:
    #             if desc.description not in desc0:
    #                 desc0.append(desc.description)
    #             amount += desc.amount
    #             count += 1
                
    #     amount1.append(amount)
    #     count1.append(count)

    


    # final_testing = zip(desc0, amount1, count1)
    # bulk = {
    #     'ddd': final_testing,
        
    # }



   
















"""desc0 = []
    amount1 =[]
    count1 = []

    for result in results:
        amount = 0
        count = 0
        
        for desc in results:
            if desc.description == result.description:
                if desc.description not in desc0:
                    desc0.append(desc.description)
                amount += desc.amount
                count += 1
                
        amount1.append(amount)
        count1.append(count)

    total = sum(amount1)


    final_testing = zip(desc0, amount1, count1)
    bulk = {
        'ddd': final_testing,
        'total': total
    }

    print(desc0)
    print(amount1)
    print(count1)
"""





'''
        bulk = {}

        for result in results:
            ca1_total = 0
            ca2_total = 0
            exams_total = 0
            total = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    subjects.append(subject)
                    ca1_total += subject.ca1
                    ca2_total += subject.ca2
                    exams_total += subject.exams
                    total += subject.total
                    subject_pos = subject.subject_position
                    grade = subject.grade
                    terms = subject.term
                    sesss = subject.session
                    classs = subject.student_class
                    avr = total/len(subjects)



                bulk[result.student] = {
                "student": result.student,
                "subjects": subjects,
                "ca1_total": ca1_total,
                "ca2_total": ca1_total,
                "exams_total": exams_total,
                "total": total,
                "grade": grade,
                "subject_pos": subject_pos,
                "terms": terms,
                "sesss": sesss,
                "classs": classs,
                "overal_total": total,
                "average": round(avr, 2)



                }
'''