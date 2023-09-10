from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from dean_information_system_app.models import CustomUser
from .models import* 

admin.register(CallToAction,About_Courses_Section,About_Courses_Descriptions,PostSection,PostDescription)(admin.ModelAdmin)
# here we create a blank usermodel class and regiister into admin.py ....if we dont create balnk usermodel then password will not be ecrypted 


class UserModel(UserAdmin):
    pass

# here we register the model and customeUser model which we created in models.py 


admin.site.register(CustomUser,UserModel)




# =========================TEST==================================
class ModelAdmin(admin.ModelAdmin):
    # Define your customizations here

    def add_view(self, request, form_url='', extra_context=None):
        # Your custom logic for the "Add" view goes here
        return super().add_view(request, form_url, extra_context)

# =========================TEST=============







