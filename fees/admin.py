from django.contrib import admin
from fees.models import FeesRecord


    

class FeesRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'payment_purpose', 'session','term','student_class','amount_paid')
    search_fields = ('student', 'payment_purpose', 'session','term','student_class',)


admin.site.register(FeesRecord,FeesRecordAdmin)

