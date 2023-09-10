import datetime
import json
import os,sys

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from dean_information_system_app.EmailBackEnd import EmailBackEnd
from dean_information_system_app.models import CustomUser, Courses, SessionYearModel
from dean_information_system import settings

from .models import*



#   ===========HOME PAGE===========
def index(request):
    # here we create object for all the home tables
    call_to_action = CallToAction.objects.all()
    aboutCoursesSection = About_Courses_Section.objects.all()
    aboutCoursesDescription = About_Courses_Descriptions.objects.all()
    postSection = PostSection.objects.all()
    postDescription = PostDescription.objects.all()
    return render(request, "home/pages/index.html", {'call_to_actions':call_to_action,'aboutCoursesSections':aboutCoursesSection,'aboutCoursesDescriptions':aboutCoursesDescription, 'postSections':postSection,'postDescriptions':postDescription})


#   ===========DEAN PAGE===========
def deanLogin(request):
    return render(request, "home/pages/deanLogin.html")


#   ===========STAFF PAGE===========
def staffLogin(request):
    return render(request, "home/pages/staffLogin.html")


#   ===========STUDENT PAGE===========
def studentLogin(request):
    return render(request, "home/pages/studentLogin.html")



def showDemoPage(request):
    return render(request,"demo.html")


# here we create a function for showing login page
def ShowLoginPage(request):
    return render(request,"login_page.html") # then we return the render html page



# This is the login page
def doLogin(request):
      # we pass a condition for the login details
    if request.method!="POST":#here if method is not equal  to post
        return HttpResponse("<h2>Method Not Allowed</h2>")#then return this  httpResponse message () this will return error message
    else:
        captcha_token=request.POST.get("g-recaptcha-response") ,#here we store our captcha token in a variable call captcha_token 
        cap_url="https://www.google.com/recaptcha/api/siteverify" #here we create url variable where we can send our token, so we call the Google API which return Captcha if it is valid or invalid
        cap_secret="6LfWaCUjAAAAAGWs-VjOwhrsTb5WX313a5b9m51X" #here we create captcha_secret variable copy and paste the server key which we got from google captcha Panel
    # cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT" #here we create captcha_secret variable copy and paste the server key which we got from google captcha Panel
        cap_data={"secret":cap_secret,"response":captcha_token} #here we create dictionary object and add value server Key and captcha token
        cap_server_response=requests.post(url=cap_url,data=cap_data)#here we make a request to Google Captcha Server and passing the server key and captcha Response and store into object cap_server_response 
        cap_json=json.loads(cap_server_response.text)#Now lets parse the JSON data into Dictionary by using json.loads() method and pass the response text here

        if cap_json['success']==False:  #here we check condition if success is false then it will redirect still to the same Login page with the error message below
            messages.error(request,"D.I.S. says | Invalid Captcha Try Again")
            return HttpResponse('<b><h4 style="color:red;">Try again, Please Make sure that You Check the CAPTCHA Box to verify your login</b></h4> ')
            # return HttpResponseRedirect("index")

        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))#now create user object by calling method EmailBackEnd.aauthenticate() and passing Email and Password
        if user!=None:#if user is not none then we call the login() and pass user object
            login(request,user)#call the log object 
            # here we process login for the users(dean, Students, St  aff)
            if user.user_type=="1":#here if user type is 1
                return HttpResponseRedirect('/admin_home')#then if login is success it will take us to the Dean HomePage
            elif user.user_type=="2":#if the user type is 2
                return HttpResponseRedirect(reverse("staff_home"))#  return HttpResponseRedirect(reverse("staff_home")) #this will take us to the staff page
            else:
                return HttpResponseRedirect(reverse("student_home"))  #  return HttpResponseRedirect(reverse("student_home")) #or else if th user login as sstudent  it will take us to the student page
        else:         # now here we store the error message and success message in messages after login is completed (if login fail we store data into message.error())
            messages.error(request,"Invalid Login Details")#in the login page.html we add a block of condition to pass this error
            # return HttpResponseRedirect("/index")#this will show invalid login message to user and also redirect user to login page again
            return HttpResponseRedirect("/")#this will show invalid login message to user and also redirect user to login page again

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type)) #this will print the current login user email and user type
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
    # return HttpResponseRedirect("index")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    return render(request,"signup_admin_page.html")

def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})

def signup_staff(request):
    return render(request,"signup_staff_page.html")

def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("deanLogin"))
    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("signup_admin"))



# staff signup //////
def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")
    telephone=request.POST.get("telephone")
    qualification=request.POST.get("qualification")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.staffs.telephone=telephone
        user.staffs.qualification=qualification
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    telephone = request.POST.get("telephone")
    next_of_kin = request.POST.get("next_of_kin")
    registration_no = request.POST.get("registration_no")
    # date_of_birth = request.POST.get("date_of_birth")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    profile_pic = request.FILES['profile_pic']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)

    #try:
    user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                          first_name=first_name, user_type=3)
    user.students.address = address
    user.students.telephone = telephone
    user.students.next_of_kin = next_of_kin
    user.students.registration_no = registration_no
    # user.students.date_of_birth = date_of_birth
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.object.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
    #except:
     #   messages.error(request, "Failed to Add Student")
      #  return HttpResponseRedirect(reverse("show_login"))



