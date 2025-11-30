from django.contrib import admin
from src.models import Subject, StudentClass, Session, Term, Student, StudentResult, StudentBehaviouralAssessment, signature, sets

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student_name',
        'student_class',
        'status',
        'gender',
    )
    search_fields = ['id','student_name', 'student_class__class_name']


# Register your models here.
admin.site.register(Subject)
admin.site.register(StudentClass)
admin.site.register(Session)
admin.site.register(Term)
admin.site.register(StudentResult)
admin.site.register(StudentBehaviouralAssessment)
admin.site.register(signature)
admin.site.register(sets)

