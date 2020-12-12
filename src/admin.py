from django.contrib import admin
from src.models import Subject, StudentClass, Session, Term, Student, StudentResult, StudentBehaviouralAssessment, signature, sets

# Register your models here.
admin.site.register(Subject)
admin.site.register(StudentClass)
admin.site.register(Session)
admin.site.register(Term)
admin.site.register(Student)
admin.site.register(StudentResult)
admin.site.register(StudentBehaviouralAssessment)
admin.site.register(signature)
admin.site.register(sets)