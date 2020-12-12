from django.db import models


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return(self.subject_name)

class StudentClass(models.Model):
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return(self.class_name)

class Session(models.Model):
    session_name = models.CharField(max_length=100)

    def __str__(self):
        return(self.session_name)

class Term(models.Model):
    term_name = models.CharField(max_length=100)

    def __str__(self):
        return(self.term_name)


class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_class = models.ForeignKey(StudentClass, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return(self.student_name)
    

class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    ca1 = models.IntegerField(default=0)
    ca2 = models.IntegerField(default=0)
    exams = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    subject_position = models.IntegerField(default=0)


    class Meta:
        ordering = ['session']

    def __str__(self):
        return f'{self.session} {self.term} {self.subject} {self.student}'
       
    def grade(self):
        if (self.ca1 + self.ca2 + self.exams) >=70:
            return "A"
        elif (self.ca1 + self.ca2 + self.exams) >= 60:
            return "B"
        elif (self.ca1 + self.ca2 + self.exams) >= 50:
            return "C"
        elif (self.ca1 + self.ca2 + self.exams) >= 45:
            return "D"
        elif (self.ca1 + self.ca2 + self.exams) >= 40:
            return "E"
        else:
            return "F"

class StudentBehaviouralAssessment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    conduct = models.IntegerField(default=0)
    punctuality = models.IntegerField(default=0)
    dedication = models.IntegerField(default=0)
    participation = models.IntegerField(default=0)
    hospitality = models.IntegerField(default=0)
    neatness = models.IntegerField(default=0)
    creativity = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.session} {self.term} {self.student_class} {self.student}'

class signature(models.Model):
    classs = models.CharField(max_length=100)
    t_image = models.ImageField(upload_to='signs')
    p_image = models.ImageField(upload_to='signs')
        

    def __str__(self):
        return self.classs

class sets(models.Model):
    h_image = models.ImageField(upload_to='setting_images')
    g_image = models.ImageField(upload_to='setting_images')