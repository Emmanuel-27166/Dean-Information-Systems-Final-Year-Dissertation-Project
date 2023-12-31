import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from dean_information_system_app.models import Modules, SessionYearModel, Students, Attendance, AttendanceReport, \
    LeaveReportStaff, Staffs, FeedBackStaffs, CustomUser, Courses, NotificationStaffs, StudentGrade

# ===========================FUNCTION FOR STAFF HOME==============
def staff_home(request):
    #For Fetch All Student Under Staff
    modules=Modules.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for module in modules:
        course=Courses.objects.get(id=module.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(module_id__in=modules).count()

    #Fetch All Approve Leave
    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    module_count=modules.count()

    #Fetch Attendance Data by Subject
    module_list=[]
    attendance_list=[]
    for module in modules:
        attendance_count1=Attendance.objects.filter(module_id=module.id).count()
        module_list.append(module.module_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"module_count":module_count,"module_list":module_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    modules=Modules.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html",{"modules":modules,"session_years":session_years})

@csrf_exempt
def get_students(request):
    module_id=request.POST.get("module")
    session_year=request.POST.get("session_year")

    module=Modules.objects.get(id=module_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=module.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    module_id=request.POST.get("module_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    module_model=Modules.objects.get(id=module_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(module_id=module_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    modules=Modules.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"staff_template/staff_update_attendance.html",{"modules":modules,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
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
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

# here we create a function for staff to apply for leave
def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})

def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
       
        leave_date=request.POST.get("leave_date") # here we create variable leave_date and access the leave data coming from Post ie from staff apply_leave html template ( name="leave_date")
        leave_msg=request.POST.get("leave_msg")# here we create variable leave_msg and access the Leave Reason coming from Post ie from staff apply_leave html template ( name="leave_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id) #access staff object from current user login Id
        try:

            # Now, create leave_report object  by calling LeaveReportStaff function from our Model.py 
            leave_report=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Staffs.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_all_notification(request):
    staff=Staffs.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})

def staff_add_grade(request):
    modules=Modules.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_add_grade.html",{"modules":modules,"session_years":session_years})

def save_student_grade(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_grade')
    student_admin_id=request.POST.get('student_list')
    # assignment_marks=request.POST.get('assignment_marks')
    # exam_marks=request.POST.get('exam_marks')
    grade_marks=request.POST.get('grade_marks')#this is for the modulegrade mark
    module_id=request.POST.get('module')


    student_obj=Students.objects.get(admin=student_admin_id)
    module_obj=Modules.objects.get(id=module_id)

    try:
        check_exist=StudentGrade.objects.filter(module_id=module_obj,student_id=student_obj).exists()
        if check_exist:
            grade=StudentGrade.objects.get(module_id=module_obj,student_id=student_obj)
            # grade.module_assignment_marks=assignment_marks
            # grade.module_exam_marks=exam_marks
            grade.module_grade_marks=grade_marks
            grade.save()
            messages.success(request, "Successfully Updated Grade")
            return HttpResponseRedirect(reverse("staff_add_grade"))
        else:
            grade=StudentGrade(student_id=student_obj,module_id=module_obj,module_grade_marks=grade_marks)
            # grade=StudentGrade(student_id=student_obj,module_id=module_obj,module_exam_marks=exam_marks,module_assignment_marks=assignment_marks,module_grade_marks=grade_marks)
            grade.save()
            messages.success(request, "Successfully Added Grade")
            return HttpResponseRedirect(reverse("staff_add_grade"))
    except TypeError as e:
        messages.error(request, "Failed to Add Grade {e}")
        return HttpResponseRedirect(reverse("staff_add_grade"))


@csrf_exempt
def fetch_grade_student(request):
    module_id=request.POST.get('module_id')
    student_id=request.POST.get('student_id')
  
    student_obj=Students.objects.get(admin=student_id)
    grade=StudentGrade.objects.filter(student_id=student_obj.id,module_id=module_id).exists()
    if grade:
        grade=StudentGrade.objects.get(student_id=student_obj.id,module_id=module_id)
        grade_data={ "grade_marks":grade.module_grade_marks}
        return HttpResponse(json.dumps(grade_data))
    else:
        return HttpResponse("False")


def returnHtmlWidget(request):
    return render(request,"widget.html")