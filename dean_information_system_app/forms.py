from django import forms
from django.forms import ChoiceField

from dean_information_system_app.models import Courses, SessionYearModel, Modules, Students

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email ",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    
    # date_of_birth=forms.DateField(label="Date of Birth", widget=forms.DateInput(format=('YYYY-MM-DD'),attrs={'class': ' form-control', 'placeholder': 'Select a date', 'type': 'date'}))
    date_of_birth=forms.CharField(label="Date of Birth", widget=forms.TextInput(attrs={"class":"form-control"}))
    # date_of_birth=forms.DateField(label="Date of Birth", widget=forms.DateInput(format=('%m/%m/%Y'),attrs={'class': 'datepicker form-control', 'placeholder': 'Select a date', 'type': 'date'}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    telephone=forms.CharField(label="Telephone",max_length=12,widget=forms.TextInput(attrs={"class":"form-control"}))
    registration_no=forms.CharField(label="Registration No",max_length=5,widget=forms.TextInput(attrs={"class":"form-control"}))
    next_of_kin=forms.CharField(label="Next of Kin",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    current_year=forms.CharField(label="Current Year",max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))



    course_list=[]
    try:
        courses=Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]
    #course_list=[]

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list=[]

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,  widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    date_of_birth=forms.CharField(label="Date of Birth", widget=forms.TextInput(attrs={"class":"form-control, "}))
    # date_of_birth =  forms.DateField(label="Date of Birth", widget=forms.DateInput(format=('%YYYY-%mm-%dd'),attrs={'class': 'datepicker form-control', 'placeholder': 'Select a date', 'type': 'date'}))
    # date_of_birth =  forms.DateField(label="Date of Birth", widget=forms.DateInput(format=('YYYY-MM-DD'),attrs={'class': ' form-control', 'placeholder': 'Select a date', 'type': 'date'}))
    # date_of_birth =  forms.DateField(label="Date of Birth", widget=forms.DateInput(format=('%d/%m/%Y'),attrs={'class': 'datepicker form-control', 'placeholder': 'Select a date', 'type': 'date'}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    telephone=forms.CharField(label="Telephone",max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))
    registration_no=forms.CharField(label="Registration No",max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))
    next_of_kin=forms.CharField(label="Next of Kin",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    current_year=forms.CharField(label="Current Year",max_length=15,widget=forms.TextInput(attrs={"class":"form-control"}))
    

    course_list=[]
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        pass
        #session_list = []

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)


# this is a form to edit Resut form
class EditGradeForm(forms.Form):
    def __init__(self, *args, **kwargs): #here we create a constructor  __init__for the form
        self.staff_id=kwargs.pop("staff_id") #so we take  StaffId input which will call the form
        super(EditGradeForm,self).__init__(*args,**kwargs)

        #here we declear an empty module list and we surround it with try and except block 
        module_list=[] 
       
        try:
            modules=Modules.objects.filter(staff_id=self.staff_id) #here we access all the module data of staff
            for module in modules:
                module_single=(module.id,module.module_name)# here we access all the module data and store into subject_list as tuple with id and subject name so it will show in form with value and text subject name
                module_list.append(module_single)#so here we append this module_single into module_list
        except:
            module_list=[]
        self.fields['module_id'].choices=module_list # here we set the module_id choice data Inside __ini__method


    session_list=[]
    # here we add try block 
    try:
        sessions=SessionYearModel.object.all()#acess all the sessionYear Data
        # here we create a for loop that will access a;; the session year data and storing into session_list as a tuple with ID and Session Start and Session End Year
        for session in sessions:
            session_single=(session.id,str(session.session_start_year)+" TO "+str(session.session_end_year))
            session_list.append(session_single) #now we append the tuple into session_list
    except: #so here we add the empty session_list
        session_list=[] 
# here are our field for the edit students 
    module_id=forms.ChoiceField(label="Module:",widget=forms.Select(attrs={"class":"form-control"}))#here we add module_id field which show all module in drop down choice
    session_ids=forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    student_ids=ChoiceNoValidation(label="Student",widget=forms.Select(attrs={"class":"form-control"}))
    # assignment_marks=forms.CharField(label="Assignment Marks",widget=forms.TextInput(attrs={"class":"form-control"}))
    grade_marks=forms.CharField(label="Grade Mark",widget=forms.TextInput(attrs={"class":"form-control"}))

