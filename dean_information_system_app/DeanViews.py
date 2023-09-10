import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import AddStudentForm

from dean_information_system_app.forms import AddStudentForm, EditStudentForm
from dean_information_system_app.models import CustomUser, Staffs, Courses, Modules, Students, SessionYearModel, \
    FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, \
    NotificationStudent, NotificationStaffs

 
def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    module_count=Modules.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    module_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        modules=Modules.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        module_count_list.append(modules)
        student_count_list_in_course.append(students)

    modules_all=Modules.objects.all()
    module_list=[]
    student_count_list_in_module=[]
    for module in modules_all:
        course=Courses.objects.get(id=module.course_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        module_list.append(module.module_name)
        student_count_list_in_module.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        module_ids=Modules.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(module_id__in=module_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)

    return render(request,"dean_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"module_count":module_count,"course_count":course_count,"course_name_list":course_name_list,"module_count_list":module_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_module":student_count_list_in_module,"module_list":module_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})

def add_staff(request):
    return render(request,"dean_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")#then return this error message to user
    else:#else if it is equal to true (POST), it wil process the data of the staff form and save  in to the db
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        telephone=request.POST.get("telephone")
        qualification=request.POST.get("qualification")
       

        # now let's add try except block to handle all errors
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)# here we called the method .create_user() and pass username, psw,email, firstname,lastname,usertype. note staff in the customUser is user type 2
            user.staffs.address=address#here in same custome user object "user"  access the staff object and pass the address also etc
            user.staffs.telephone=telephone
            user.staffs.qualification=qualification
            user.save()#then we save the user
            messages.success(request,"Successfully Added Staff")#here we set success message on data save
            return HttpResponseRedirect(reverse("add_staff"))#here if staff data save it will redirect admin to Add Staff page  again(ie the same page)with success message
        except TypeError as e:
            messages.error(request,"Failed to Add Staff {e}")#here we set message on fail data save
            return HttpResponseRedirect(reverse("add_staff"))#here if staff data is not save, it will redirect admin to Add Staff page again(ie the same page)with error message



def add_course(request):
    return render(request,"dean_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":#if the method is not equal to post, then it will show error message
        return HttpResponse("Method Not Allowed")#then return this error message to user
    else: #it will process the form data
        course=request.POST.get("course")#storing the course data into course variable
        # now let's add try except block to handle all errors
        try:
            course_model=Courses(course_name=course) #here we create a course model object from our courses table of the model.py and call the course_name and pass the course variable 
            course_model.save()#then save our course in into db
            messages.success(request,"Successfully Added Course")#here we set success message on data save
            return HttpResponseRedirect(reverse("add_course"))#here if course data save it will redirect admin to Add Course page again(ie the same page) with success message
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Course")#here we set message on fail data save
            return HttpResponseRedirect(reverse("add_course"))#here if staff data is not save, it will redirect admin to Add Course again(ie the same page) page with error message
  # we surround the whole code into try except

def add_student(request):
    form=AddStudentForm()
    return render(request,"dean_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else: #else if it is equal to true (POST), it wil process the data of the staff form and save  in to the db
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            date_of_birth=form.cleaned_data["date_of_birth"]
            address=form.cleaned_data["address"]
            telephone=form.cleaned_data["telephone"]
            registration_no=form.cleaned_data["registration_no"]
            next_of_kin=form.cleaned_data["next_of_kin"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            current_year=form.cleaned_data["current_year"]
            sex=form.cleaned_data["sex"]
            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
# now let's add try except block to handle all errors
            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.date_of_birth=date_of_birth
                user.students.current_year=current_year
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                session_year=SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id=session_year
                user.students.gender=sex
                user.students.profile_pic=profile_pic_url
                user.students.telephone=telephone
                user.students.registration_no=registration_no
                user.students.next_of_kin=next_of_kin
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except TypeError as e:
                messages.error(request,"Failed to Add Student {e}")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "dean_template/add_student_template.html", {"form": form})


def add_module(request):
    courses=Courses.objects.all()#here we read all courses data by calling methof courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)#here we access all staff data. our staff data is customuser with user type of 2
    return render(request,"dean_template/add_module_template.html",{"staffs":staffs,"courses":courses})#now pass the template name and pass the data in template page as a dictionary and pass staff in staffs object and course in course object

def add_module_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        module_name=request.POST.get("module_name")
        module_code=request.POST.get("module_code")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
# now let's add try except block to handle all errors
        try:
            module=Modules(module_name=module_name,module_code=module_code,course_id=course,staff_id=staff)
            module.save()
            messages.success(request,"Successfully Added Module")
            return HttpResponseRedirect(reverse("add_module"))
        
        except TypeError as e:
            messages.error(request,"Failed to Add Module {e}")
            return HttpResponseRedirect(reverse("add_module"))


def manage_staff(request):
    # ====condition is for the searchbar=====
    if 'searchbar' in request.GET:
        searchbar = request.GET['searchbar']
        # staffs = Staffs.objects.filter(name__icontains=searchbar)
        staffs = Staffs.objects.filter(telephone__icontains=searchbar)
    # ====condition is for the searchbar=====
    
    else:
        staffs=Staffs.objects.all()#here we read all staff data by calling method staffs.objects.all()
    return render(request,"dean_template/manage_staff_template.html",{"staffs":staffs})#then pass the staff in the template and pass the staff object


# modal class view courses begins
def view_staff_modal(request, id):
    staff = Staffs.objects.get(pk=id)

    return HttpResponseRedirect(reverse('manage_staff'))

# student search
def manage_student(request):
        # ====condition is for the searchbar=====
    if 'searchbar' in request.GET:
        searchbar = request.GET['searchbar']
        students = Students.objects.filter(registration_no__icontains=searchbar)
    # ====condition is for the searchbar=====

    else:
        students=Students.objects.all()
    return render(request,"dean_template/manage_student_template.html",{"students":students})



# modal class view students begins
def view_student(request, id):
    student = Students.objects.get(pk=id)

    return HttpResponseRedirect(reverse('manage_student'))

# course searcher bar
def manage_course(request):
            # ====condition is for the searchbar=====
    if 'searchbar' in request.GET:
        searchbar = request.GET['searchbar']
        courses = Courses.objects.filter(course_name__icontains=searchbar)
    # ====condition is for the searchbar=====
    else:
        courses=Courses.objects.all()
    return render(request,"dean_template/manage_course_template.html",{"courses":courses})


# modal class view courses begins
def view_course_modal(request, id):
    course = Courses.objects.get(pk=id)

    return HttpResponseRedirect(reverse('manage_course'))


# search modules

def manage_module(request):
    if 'searchbar' in request.GET:
        searchbar = request.GET['searchbar']
        modules = Modules.objects.filter(module_code__icontains=searchbar)
      
    else:
        modules=Modules.objects.all()
    return render(request,"dean_template/manage_module_template.html",{"modules":modules})


# modal class view courses begins
def view_module_modal(request, id):
    module = Modules.objects.get(pk=id)

    return HttpResponseRedirect(reverse('manage_course'))

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"dean_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        telephone=request.POST.get("telephone")
        qualification=request.POST.get("qualification")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.telephone=telephone
            staff_model.qualification=qualification
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['telephone'].initial=student.telephone
    form.fields['next_of_kin'].initial=student.next_of_kin
    form.fields['registration_no'].initial=student.registration_no
    form.fields['date_of_birth'].initial=student.date_of_birth
    form.fields['course'].initial=student.course_id.id
    form.fields['current_year'].initial=student.current_year
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    return render(request,"dean_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            address = form.cleaned_data["address"]
            telephone = form.cleaned_data['telephone']
            next_of_kin = form.cleaned_data['next_of_kin']
            registration_no = form.cleaned_data['registration_no']
            session_year_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            current_year = form.cleaned_data["current_year"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None
            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.date_of_birth=date_of_birth
                student.address=address
                student.telephone=telephone
                student.next_of_kin=next_of_kin
                student.registration_no=registration_no
                student.date_of_birth=date_of_birth
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                student.current_year = current_year
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"dean_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_module(request,module_id):
    module=Modules.objects.get(id=module_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"dean_template/edit_module_template.html",{"module":module,"staffs":staffs,"courses":courses,"id":module_id})

def edit_module_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        module_id=request.POST.get("module_id")
        module_name=request.POST.get("module_name")
        module_code=request.POST.get("module_code")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")

        try:
            module=Modules.objects.get(id=module_id)
            module.module_name=module_name
            module.module_code=module_code
            staff=CustomUser.objects.get(id=staff_id)
            module.staff_id=staff
            course=Courses.objects.get(id=course_id)
            module.course_id=course
            module.save()

            messages.success(request,"Successfully Edited Module")
            return HttpResponseRedirect(reverse("edit_module",kwargs={"module_id":module_id}))
        except TypeError as e:
            messages.error(request,"Failed to Edit Module {e}")
            return HttpResponseRedirect(reverse("edit_module",kwargs={"module_id":module_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"dean_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            print(Courses.course_name)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


def manage_session(request):
    return render(request,"dean_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

# ==========================VALIDATIONS====================
# this is to check if the email exist in db
@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# this is to check if the username exist in db
@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

# this is to check if the username exist in db
@csrf_exempt
def check_registration_no_exist(request):
    registration_no=request.POST.get("registration_no")
    user_obj=Students.objects.filter(registration_no=registration_no).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    # =============CHECK STUDENT TELEPHONE NUMBER EXISTENCE======
@csrf_exempt
def check_telephone_exist(request):
    telephone=request.POST.get("telephone")
    user_obj=Students.objects.filter(telephone=telephone).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
# def check_staff_telephone_exist(request):
# def check_staff_telephone_exist(request):
    telephone=request.POST.get("telephone")
    user_obj=Staffs.objects.filter(telephone=telephone).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

# ================check for course existence===
@csrf_exempt
def check_course_name_exist(request):
    course_name=request.POST.get("course_name")
    user_obj=Courses.objects.filter(course_name=course_name).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


 

# =======to be uncomment if i want to use validation on module=======

# check module code exitst
# @csrf_exempt
# def check_module_code_exist(request):
#     module_code=request.POST.get("module_code")
#     user_obj=Modules.objects.filter(module_code=module_code).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)

# check module code exitst
# @csrf_exempt
# def check_module_name_exist(request):
#     module_name=request.POST.get("module_name")
#     user_obj=Modules.objects.filter(module_name=module_name).exists()
#     if user_obj:
#         return HttpResponse(True)
#     else:
#         return HttpResponse(False)


def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"dean_template/staff_feedback_template.html",{"feedbacks":feedbacks})

def student_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"dean_template/student_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"dean_template/staff_leave_view.html",{"leaves":leaves})

def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"dean_template/student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    modules=Modules.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request,"dean_template/admin_view_attendance.html",{"modules":modules,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    module=request.POST.get("module")
    session_year_id=request.POST.get("session_year_id")
    module_obj=Modules.objects.get(id=module)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(module_id=module_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"dean_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def admin_send_notification_student(request):
    if 'searchbar' in request.GET:
        searchbar = request.GET['searchbar']
        students = Students.objects.filter(registration_no__icontains=searchbar)
    else:
        students=Students.objects.all()
    return render(request,"dean_template/student_notification.html",{"students":students})

def admin_send_notification_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"dean_template/staff_notification.html",{"staffs":staffs})

@csrf_exempt
def send_student_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    student=Students.objects.get(admin=id)
    token=student.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Dean Information System",
            "body":message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStudent(student_id=student,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

@csrf_exempt
def send_staff_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    staff=Staffs.objects.get(admin=id)
    token=staff.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Dean Information System",
            "body":message,
            "click_action":"https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStaffs(staff_id=staff,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

