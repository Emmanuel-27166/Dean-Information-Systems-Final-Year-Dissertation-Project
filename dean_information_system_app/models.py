from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
# =========================================HOME PAGE TABLES BEGINS=========================================
class CallToAction(models.Model):
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100)
    SubTitle = models.CharField(max_length=100)
    # Button = models.CharField(max_length=20)
    # SliderImage = models.ImageField(upload_to="Home Pics")

class About_Courses_Section(models.Model):
    id = models.AutoField(primary_key=True)
    Section = models.CharField(max_length=150)
    Paragraph = models.TextField()

class About_Courses_Descriptions(models.Model):
    id = models.AutoField(primary_key=True)
    CourseName = models.CharField(max_length=100)
    Description = models.TextField()
    Image = models.ImageField(upload_to="Home Pics")


class PostSection(models.Model):
    id = models.AutoField(primary_key=True)
    Section = models.CharField(max_length=150)
    Paragraph = models.TextField()

class PostDescription(models.Model):
    id = models.AutoField(primary_key=True)
    Topic = models.CharField(max_length=35)
    Title = models.CharField(max_length=35)
    Description = models.TextField()
    Date = models.DateField()
    Image = models.ImageField(upload_to="Home Pics")


# =========================================HOME PAGE TABLES ENDS=====================================



# HERE WE CREATE A NEW MODEL WHICH IS SESSION yEAR WHIHC HAD 3 FIELDS (SESSION ID, SESSION_START_YEAR AND SESSION_YEAR _END)
class SessionYearModel(models.Model):
    id=models.AutoField(primary_key=True)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    object=models.Manager()

# here we override the default django auth user and adding one more field in this model which is user type: 1 admin, 2: staff, 3:student
class CustomUser(AbstractUser):
    user_type_data=((1,"Dean"),(2,"Staff"),(3,"Student")) #now create a tuple set of Admin, Staff, Student
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)
    

  
# from the above we create class CustomUser and passing parent  AbstractUser so we can Extend the Default Auth User



 
# # ======================1. Admin table======================
class Dean(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE) #we connect a relationship with our CustomUser (ie one to one Field)
    # name=models.CharField(max_length=225)   #========NOte name, email and password already storing into django default user which is customUser   so we removed them to normalising the student, staff, hod model
    # email = models.CharField(max_length=225)
    # password = models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    # =======================2 Staff Table========================
class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)#we connect a relationship with our CustomUser (ie one to one Field)
       # name=models.CharField(max_length=225)   #========NOte name, email and password already storing into django default user which is customUser   so we removed them to normalising the student, staff, hod model
    # email = models.CharField(max_length=225)
    # password = models.CharField(max_length=225)
    address=models.TextField()
    telephone = models.CharField(max_length=13)
    qualification = models.CharField(max_length=225)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects=models.Manager()


    # def __str__(self):
    #     return self.first_name

    # ======================5. students Course table=================
class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    # ======================4. Module Table======================
class Modules(models.Model):
    id=models.AutoField(primary_key=True)
    module_name=models.CharField(max_length=255)
    module_code=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)#Relation with course and module
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)#Relationship with staff and module
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()



    # ===============6. MODULECOURSE========= for both module and course===
class ModuleCourses(models.Model):
    id = models.AutoField(primary_key=True)
    # course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    # module_id = models.ForeignKey(Modules, on_delete=models.CASCADE)
    objects = models.Manager()
    # ======================3. student table=================
class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)#we connect a relationship with our CustomUser (ie one to one Field)
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField()
    registration_no = models.CharField(max_length=5)
    address=models.TextField()
    telephone = models.CharField(max_length=13)
    date_of_birth=models.CharField(max_length=25)
    next_of_kin = models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)# a relation with student and course
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE) #A foreign key from SessionYearModel
    current_year = models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    fcm_token=models.TextField(default="")
    objects = models.Manager() 
 
    # ======================6 Attendance table=================
class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    module_id=models.ForeignKey(Modules,on_delete=models.DO_NOTHING)
    attendance_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    session_year_id=models.ForeignKey(SessionYearModel,on_delete=models.CASCADE)#A foreign key from SessionYearModel
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    # ======================7 Attendance Report table=================
class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.DO_NOTHING)#Relationship with student
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)#Relationship with Attendance
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    # ======================8 Leave Report Student table=================
class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)#Relationship with Student
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


    # ======================9 Leave Report Staff table=================
class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)#Relationship with staff
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


    # ======================10 FeedBack Student table=================
class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)#Relationship with Student
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


    # ======================11 FeedBack Staff table=================
class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)#Relationship with Staff
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


    # ======================12 Notification Student table=================
class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)#Relatioonship with Student
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    # ======================13 Notification Staff table=================
class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)#Relatioonship with Staff
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


    # ======================14 Student Result table=================
class StudentGrade(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)#Relatioonship with Student
    module_id=models.ForeignKey(Modules,on_delete=models.CASCADE)#Relatioonship with Module
    module_grade_marks=models.FloatField(default=0)
    # module_assignment_marks=models.FloatField(default=0)
    # module_grade_marks=models.FloatField(default=0) #this is for the actual grade
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)
    objects=models.Manager()



# ==================================================================
  #  here we create  signal in django so that when a new user create it will add new row in HOD,
    # staff,student with it's ID in admin_id column, so we create @receiver(post_save, send=CustomUser)
    # so this method will run only when data is added

@receiver(post_save,sender=CustomUser)
# ================students create method======================================
# =================added========
#here we create a function that will add data into HOD, staff and student table
# take parameter sender, instance,created here sender is class which call this method, instance is current inserted data model, created is true/false, it is true when data is inserted
def create_user_profile(sender,instance,created,**kwargs):
    if created: #if created is true means daata inserted
        if instance.user_type==1:#if user type is 1  then it it will add row in hod table with admin id
            Dean.objects.create(admin=instance)#then call Dean objects.create()and pass admin instance. here the instance is CustomUser
        if instance.user_type==2:#if user type is 2
            Staffs.objects.create(admin=instance,address="",telephone="",qualification="")#then call staff objects.create()and pass admin instance. here the instance is CustomUser
        if instance.user_type==3:#if user type is 3
            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_year_id=SessionYearModel.object.get(id=1),date_of_birth="",current_year="", address="",telephone="",next_of_kin="",registration_no="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs): #this method wil be called after create_user() execution
    if instance.user_type==1:#if user type is 1
        instance.dean.save()#then call instance.dean.save() method to  save Admin Model
    if instance.user_type==2:#if user type is 2
        instance.staffs.save()#then call instance.staffs.save() method to save Staff Model
    if instance.user_type==3:#if user type is 3
        instance.students.save()#then call instance.students.save() method to save Students Model
# All this Receiver work when we add new data in CustomUser Table after inserting data it will insert the current ID of CustomUser (1,2,3) into other table such as Dean, Staff Students 

