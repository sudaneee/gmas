from django.shortcuts import render, redirect
from django.http import HttpResponse
from src.models import Subject, StudentClass, Session, Term, Student, StudentResult, StudentBehaviouralAssessment, signature, sets
from django.db import connection
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.models import User, auth

# cursor to move around the database 

c = connection.cursor()



def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'src/dashboard.html')

        else:
            messages.info(request, 'Incorrect Login-in Details')
            return render(request, 'src/home.html')

    else:
        return render(request, 'src/home.html')


def resultcreate(request):
    global students
    global subject
    global term
    global session
    global classs
    global class_id
    global session_id
    global term_id
    global subject_id

    if request.user.is_authenticated:

        if request.method == 'POST' and "form1" in request.POST:

            session = request.POST['session']
            term = request.POST['term']
            classs = request.POST['class']
            subject = request.POST['subject']

            ses = Session.objects.get(session_name=session)
            session_id = ses.id

            trm = Term.objects.get(term_name=term)
            term_id = trm.id

            clas = StudentClass.objects.get(class_name=classs)
            class_id = clas.id

            subj = Subject.objects.get(subject_name=subject)
            subject_id = subj.id

            students = Student.objects.filter(student_class=class_id).all()
            student_id = []
            for i in students:
                student_id.append(i.id)
            

            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            sessions = Session.objects.all()
            terms = Term.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes,
                'students': students
            }

            return render(request, 'src/resultcreate.html', context)

        if request.method == 'POST' and "form2" in request.POST:
            ses_ids = []
            trm_ids = []
            clas_ids = []
            subj_ids =[]
            total_score = []

            ids = request.POST.getlist('id')
            names = request.POST.getlist('name')
            ca1s = request.POST.getlist('ca1')
            ca1s2 = [int(i) for i in ca1s]
            ca2s = request.POST.getlist('ca2')
            ca2s2 = [int(i) for i in ca2s]
            exams = request.POST.getlist('exams') 
            exams2 = [int(i) for i in exams]
            for i in range(len(ca1s2)):
                total_score.append(ca1s2[i] + ca2s2[i] + exams2[i])


            for i in students:
                ses_ids.append(session_id)
                trm_ids.append(term_id)
                clas_ids.append(class_id)
                subj_ids.append(subject_id)

            clso = int(class_id)
            sess = int(session_id)
            trm = int(term_id)
            sbj = int(subject_id)

            queryset = StudentResult.objects.filter(session=sess, term=trm, student_class=clso, subject=sbj).exists()
            if queryset:
                print("record is already there")
            else:
                c.executemany('INSERT INTO src_studentresult (ca1, ca2, exams, total, student_id, student_class_id, subject_id, session_id, term_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', zip(ca1s, ca2s, exams, total_score, ids, clas_ids, subj_ids, ses_ids, trm_ids))
                connection.commit()

            


            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            sessions = Session.objects.all()
            terms = Term.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes,
                'students': students
            }

            return render(request, 'src/resultcreate.html', context)


        else:
            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes
            }
            return render(request, 'src/resultcreate.html', context)
    else:
        return render(request, 'src/home.html')

def updateresult(request):
    global students
    global subject
    global term
    global session
    global classs
    global class_id
    global session_id
    global term_id
    global subject_id

    if request.user.is_authenticated:

        if request.method == 'POST' and "form1" in request.POST:

            session = request.POST['session']
            term = request.POST['term']
            classs = request.POST['class']
            subject = request.POST['subject']

            ses = Session.objects.get(session_name=session)
            session_id = ses.id

            trm = Term.objects.get(term_name=term)
            term_id = trm.id

            clas = StudentClass.objects.get(class_name=classs)
            class_id = clas.id

            subj = Subject.objects.get(subject_name=subject)
            subject_id = subj.id

            students = Student.objects.filter(student_class=class_id).all()
            student_id = []




            all_results = StudentResult.objects.filter(session=session_id, term=term_id, student_class=class_id,subject=subject_id).all() 
            

            for i in students:
                student_id.append(i.id)

            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            sessions = Session.objects.all()
            terms = Term.objects.all()

            result_students_list = zip(all_results, students)
            context = {
                'subjects': subjects,
                'classes': classes,
                'all_results': all_results,
                'result_students_list': result_students_list
            }

            return render(request, 'src/updateresult.html', context)

        if request.method == 'POST' and "form2" in request.POST:
            ses_ids = []
            trm_ids = []
            clas_ids = []
            subj_ids =[]
            total_score = []

            ids = request.POST.getlist('id')
            names = request.POST.getlist('name')
            ca1s = request.POST.getlist('ca1')
            ca1s2 = [int(i) for i in ca1s]
            ca2s = request.POST.getlist('ca2')
            ca2s2 = [int(i) for i in ca2s]
            exams = request.POST.getlist('exams') 
            exams2 = [int(i) for i in exams]
            for i in range(len(ca1s2)):
                total_score.append(ca1s2[i] + ca2s2[i] + exams2[i])
            print(total_score)


            print(ca1s)

            for i in students:
                ses_ids.append(session_id)
                trm_ids.append(term_id)
                clas_ids.append(class_id)
                subj_ids.append(subject_id)

            
            c.executemany("""UPDATE src_studentresult SET ca1=?, ca2=?, exams=?, total=? WHERE 
                student_id=? AND student_class_id=? AND subject_id=? AND session_id=? AND term_id=?""", 
                zip(ca1s, ca2s, exams, total_score, ids, clas_ids, subj_ids, ses_ids, trm_ids))
            connection.commit()

            
            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            sessions = Session.objects.all()
            terms = Term.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes,
                'students': students
            }

            return render(request, 'src/updateresult.html', context)
        else:
            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes
            }
            return render(request, 'src/updateresult.html', context)
    else:
        return render(request, 'src/home.html')


def single_result_update(request):
    global students
    global subject
    global term
    global session
    global classs
    global class_id
    global session_id
    global term_id
    global subject_id
    global student_qr_id
    global student_id

    if request.user.is_authenticated:

        if request.method == 'POST' and "form1" in request.POST:
            session = request.POST['session']
            term = request.POST['term']
            classs = request.POST['class']
            subject = request.POST['subject']
            student_id = request.POST['student_id']

            ses = Session.objects.get(session_name=session)
            session_id = ses.id

            trm = Term.objects.get(term_name=term)
            term_id = trm.id

            clas = StudentClass.objects.get(class_name=classs)
            class_id = clas.id

            subj = Subject.objects.get(subject_name=subject)
            subject_id = subj.id

            student = []
            student.append(student_id)

            get_student = StudentResult.objects.get(student=student_id, session=session_id, term=term_id, student_class=class_id, subject=subject_id)
            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes,
                'get_student': get_student,
                'student_id': student_id
                }
            return render(request, 'src/single_result_update.html', context)




        if request.method == 'POST' and "form2" in request.POST:

            ids = request.POST['id']
            ca1 = request.POST['ca1']
            ca2 = request.POST['ca2']
            exams = request.POST['exams']

            total_score = int(ca1) + int(ca2) + int(exams)



            queryy = StudentResult.objects.get(student=ids, session=session_id, term=term_id, student_class=class_id, subject=subject_id)
            
            queryy.ca1 = ca1
            queryy.save() 
            queryy.ca2 = ca2
            queryy.save() 
            queryy.exams = exams 
            queryy.save() 
            queryy.total = total_score
            queryy.save() 


            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes
                }
            return render(request, 'src/single_result_update.html', context)


        else:
            subjects = Subject.objects.all()
            classes = StudentClass.objects.all()
            context = {
                'subjects': subjects,
                'classes': classes
                }
            return render(request, 'src/single_result_update.html', context)
    else:
        return render(request, 'src/home.html')
        

def result_view(request):
    global class_id
    global session_id
    global term_id

    if request.user.is_authenticated:

        if request.method == 'POST' and "form1" in request.POST:
            classes = StudentClass.objects.all()

            context = {
                'classes': classes
                }

            session = request.POST['session']
            term = request.POST['term']
            classs = request.POST['class']

            ses = Session.objects.get(session_name=session)
            session_id = ses.id

            trm = Term.objects.get(term_name=term)
            term_id = trm.id

            clas = StudentClass.objects.get(class_name=classs)
            class_id = clas.id

            results = StudentResult.objects.filter(session=session_id, term=term_id, student_class=class_id)
            bulk = {}

            print(results)

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
            print(result.student)
            classes = StudentClass.objects.all()
            bhv = StudentBehaviouralAssessment.objects.filter(session=session_id, term=term_id, student_class=class_id)
            signs = signature.objects.filter(classs=classs).first()
            some_images = sets.objects.first()

            context = {
                'classes': classes,
                'results': bulk,
                'bhv': bhv,
                'signs': signs,
                'some_images':some_images
            }



            return render(request, 'src/single_result_view.html', context)

        else:
            classes = StudentClass.objects.all()

            context = {
                'classes': classes
                }

            return render(request, 'src/result_view.html', context)

    else:
        return render(request, 'src/home.html')

def settings(request):

    if request.user.is_authenticated:

        c.execute("""UPDATE src_studentresult SET subject_position=( SELECT count(*) FROM src_studentresult AS i WHERE i.total > src_studentresult.total AND i.student_class_id = src_studentresult.student_class_id AND i.subject_id = src_studentresult.subject_id AND i.session_id = src_studentresult.session_id AND i.term_id = src_studentresult.term_id) + 1;""")
        connection.commit()

        global students
        global subject
        global term
        global session
        global classs
        global class_id
        global session_id
        global term_id
        global subject_id
        global student_id

        if request.method == 'POST' and "form1" in request.POST:

            session = request.POST['session']
            term = request.POST['term']
            classs = request.POST['class']


            ses = Session.objects.get(session_name=session)
            session_id = ses.id

            trm = Term.objects.get(term_name=term)
            term_id = trm.id

            clas = StudentClass.objects.get(class_name=classs)
            class_id = clas.id

            students = Student.objects.filter(student_class=class_id).all()
            student_id = []

            for i in students:
                student_id.append(i.id)
            print(student_id)

            classes = StudentClass.objects.all()

            context = {
                'classes': classes,
                'students': students
                }

            return render(request, 'src/settings.html', context)

        if request.method == 'POST' and "form2" in request.POST:

            ses_ids = []
            trm_ids = []
            clas_ids = []

            ids = request.POST.getlist('id')
            conduct = request.POST.getlist('conduct')
            punc = request.POST.getlist('punctuality')
            ded = request.POST.getlist('dedication')
            part = request.POST.getlist('participation')
            hosp = request.POST.getlist('hospitality')
            creat= request.POST.getlist('creativity')
            phy = request.POST.getlist('physical')
            neat = request.POST.getlist('neatness')

            for i in ids:
                ses_ids.append(session_id)
                trm_ids.append(term_id)
                clas_ids.append(class_id)


            queryset = StudentBehaviouralAssessment.objects.filter(session=session_id, term=term_id, student_class=class_id).exists()
            if queryset:
                print("record is already there")
            else:
                c.executemany("""INSERT INTO src_studentbehaviouralassessment (conduct, punctuality, dedication, participation, hospitality, 
                	neatness, creativity, physical, session_id, student_id, student_class_id, term_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                	zip(conduct, punc, ded, part, hosp, neat, creat, phy, ses_ids, ids, clas_ids, trm_ids))
                connection.commit()
            
            classes = StudentClass.objects.all()

            context = {
                'classes': classes
                }

            return render(request, 'src/settings.html', context)


        else:
            classes = StudentClass.objects.all()

            context = {
                'classes': classes
                }

            return render(request, 'src/settings.html', context)
    else:
        return render(request, 'src/home.html')        

    
def single_result_view(request):
    global subject
    global term
    global session
    global classs
    global class_id
    global session_id
    global term_id
    global subject_id
    global student_qr_id
    global students

    if request.method == 'POST' and "form1" in request.POST:
        session = request.POST['session']
        term = request.POST['term']
        student_id = request.POST['student_id']

        ses = Session.objects.get(session_name=session)
        session_id = ses.id

        trm = Term.objects.get(term_name=term)
        term_id = trm.id


        results = StudentResult.objects.filter(session=session_id, term=term_id, student=student_id)
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
        bhv = StudentBehaviouralAssessment.objects.filter(session=session_id, term=term_id, student=student_id)
        signs = signature.objects.filter(classs=classs).first()
        some_images = sets.objects.first()
        print(some_images)
        

        context = {
            'results': bulk,
            'bhv': bhv,
            'signs': signs,
            'some_images':some_images
        }

        return render(request, 'src/single_result_view.html', context)

    else:

        return render(request, 'src/single_result_view1.html')
   
'''
    if request.method == 'POST' and "form0" in request.POST:
        
        global student_qr_id
        student = request.POST['students']

        student_qry = Student.objects.get(student_name=student, student_class=)
        student_qr_id = student_qry.id

        trm = Term.objects.get(term_name=term)
        term_id = trm.id

        clas = StudentClass.objects.get(class_name=classs)
        class_id = clas.id



        results = StudentResult.objects.filter(session=session_id, term=term_id, student_class=class_id)
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
                "average": avr



                }
        classes = StudentClass.objects.all()
        bhv = StudentBehaviouralAssessment.objects.filter(session=session_id, term=term_id, student_class=class_id)

        context = {
            'classes': classes,
            'results': bulk,
            'bhv': bhv
        }



        return render(request, 'src/result_view.html', context)

    else:
        classes = StudentClass.objects.all()

        context = {
            'classes': classes
            }

        return render(request, 'src/result_view.html', context)
'''