from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user

        # HERE WE CHECK IF USER IS LOGIN AND  USER TYPE IS ONE DO NOTHING (PASS)
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "dean_information_system_app.DeanViews":
                    pass
                elif modulename == "dean_information_system_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "dean_information_system_app.StaffViews" or modulename == "dean_information_system_app.EditGradeVIewClass":
                    pass
                elif modulename == "dean_information_system_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if modulename == "dean_information_system_app.StudentViews" or modulename == "django.views.static":
                    pass
                elif modulename == "dean_information_system_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("/"))
                # return HttpResponseRedirect(reverse("index"))
                # return HttpResponseRedirect(reverse("show_login"))
# HERE IF USER IS NOT LOGIN WE WILL DIRECT THE USER TO THE LOGIN PAGE
        else:
            if request.path == reverse("index") or request.path == reverse("do_login") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="dean_information_system_app.views":
            # if request.path == reverse("show_login") or request.path == reverse("do_login") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="dean_information_system_app.views":
                pass
            else:
                return HttpResponseRedirect(reverse("index"))
                # return HttpResponseRedirect(reverse("show_login"))