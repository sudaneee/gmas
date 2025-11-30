from src.models import Subject, StudentClass, Session, Term, Student, StudentResult, StudentBehaviouralAssessment, signature, sets

def site_settings(request):
    classes = StudentClass.objects.all()
    sessions = Session.objects.all()
    terms = Term.objects.all()

    return {
        'classes': classes,
        'terms': terms,
        'sessions': sessions,
    }