from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from dean_information_system_app.forms import EditGradeForm
from dean_information_system_app.models import Students, Modules, StudentGrade

# here we create an editGRadeViewclass 
class EditGradeViewClass(View):
    def get(self,request,*args,**kwargs): #here we create get method, which will be call when user make any get request
        staff_id=request.user.id
        # here we create object for edit grade form class
        edit_grade_form=EditGradeForm(staff_id=staff_id)
        return render(request,"staff_template/edit_student_grade.html",{"form":edit_grade_form})#ai. now here we return the edit_student_result template file | then we pass the form into template
        # aii. in our form.py create a class EditGradeForm to edit Grade
# now create method for post. this method will call when user making post request
    def post(self,request,*args,**kwargs): 
        form=EditGradeForm(staff_id=request.user.id,data=request.POST)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            assignment_marks = form.cleaned_data['assignment_marks']
            exam_marks = form.cleaned_data['exam_marks']
            module_id = form.cleaned_data['module_id']

            student_obj = Students.objects.get(admin=student_admin_id)
            module_obj = Modules.objects.get(id=module_id)
            grade=StudentGrade.objects.get(module_id=module_obj,student_id=student_obj)
            grade.module_assignment_marks=assignment_marks
            grade.module_exam_marks=exam_marks
            grade.save()
            messages.success(request, "Successfully Updated Grade")
            return HttpResponseRedirect(reverse("edit_student_grade"))
        else:
            messages.error(request, "Failed to Update Grade")
            form=EditGradeForm(request.POST,staff_id=request.user.id)
            return render(request,"staff_template/edit_student_grade.html",{"form":form})


