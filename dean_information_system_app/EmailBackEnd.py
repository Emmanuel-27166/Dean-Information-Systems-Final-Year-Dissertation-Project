from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend



# here we create a class whose parent class in modelBackend (ie we inherent from the ModelBackend class)
class EmailBackEnd(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):# here we create an authenticate function in the class
        UserModel=get_user_model()
        # pass a try and catch
        try: #in try we will fetch the user from database
            user=UserModel.objects.get(email=username) #so pass the username
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None