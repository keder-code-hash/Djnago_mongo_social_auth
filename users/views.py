from rest_framework.viewsets import ModelViewSet
from .models.Users import Users 
from .serializers.UsersSerializers import UsersModelSerailizers
from djongo.models.fields import ObjectId
from django.shortcuts import get_object_or_404, render
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.settings import api_settings


from .auth_util_serializers import LoginSerializer,LogoutSerializer,ResetPasswordEmailSentSerializers,ResetPasswordSerializers,RegisterSerializer
from rest_framework import status,generics
from rest_framework_simplejwt.exceptions import InvalidToken
from .JWTConfig.CustiomJwt import CustomRefreshToken


from django.urls import reverse_lazy
from django.template.loader import get_template
from django.core.mail import EmailMessage

from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.viewsets import mixins,GenericViewSet

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import get_authorization_header

# from .CustomJwtAuth import CustomJwtAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

from django.contrib.auth import get_user_model

import json
from django.views.decorators.csrf import csrf_exempt

# python manage.py runserver [::]:8000

#### google social auth custom made ####
 
def google_login_init_page(request):
    return render(request,'google.html',{})
 
class GetGoogleProfDetails(APIView):
    def post(self,request,format=None):
        body_unicode = request.body.decode('utf-8') 	
        body = json.loads(body_unicode)  
        prof_details = body.get('google_prof_details')
        print(prof_details)
        return Response({"msg":"data is recieved"},status=status.HTTP_200_OK)

##########

class UserModelViewSet( mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, 
                        mixins.ListModelMixin,
                        GenericViewSet): 
    queryset = Users.objects.all()
    serializer_class = UsersModelSerailizers
    lookup_field  = "_id"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        try: 

            filter_kwargs = {self.lookup_field: ObjectId(self.kwargs[lookup_url_kwarg])}

            fabrixes_data = get_object_or_404(queryset, **filter_kwargs)
            self.check_object_permissions(self.request, fabrixes_data)
        except:
            message = f"Inavalid request: Author Not Found: {self.kwargs[self.lookup_field]}"
            # log.error(message) 
            raise APIException({"message": ValueError(message)}, 400)
        return fabrixes_data
 

#  https://github.com/CryceTruly/incomeexpensesapi/blob/ecee2fb78645b41187401b42862e71ab45e8e80a/authentication/models.py

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer 

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = Users.objects.get(email=user_data['email'])

        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify')
        # absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        # email_body = 'Hi '+user.username + \
        #     ' Use the link below to verify your email \n' + absurl
        # data = {'email_body': email_body, 'to_email': user.email,
        #         'email_subject': 'Verify your email'}

        # Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LogInView(APIView):
    serializer_class = LoginSerializer

    def post(self,request): 
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode) 
        serializers_data = self.serializer_class(data=body)
        serializers_data.is_valid(raise_exception=True)
 
        return Response(serializers_data.data,status=status.HTTP_200_OK)

class LogOutView(APIView):
    serializer_class = LogoutSerializer
    def post(self,request,format=None):
        serializers_data = self.serializer_class(data=request.data)
        serializers_data.is_valid(raise_exception=True)

         
        try : 
            token = CustomRefreshToken(token = serializers_data.data.get("refresh"))
            token.blacklist()
            msg = "Token Successfully blacklisted and logged out" 
        except :
            msg = 'There is an error with token. Error : '+InvalidToken.default_detail
        return Response(msg,status=status.HTTP_200_OK)

# ########## Password Reset #############

def send_mail(subject_template_name, email_template_name,
                  context, from_email, to_email, message ,html_email_template_name=None):
         
        mail = EmailMessage(
                subject="Reset Password",
                body=message,
                from_email="kedernath.mallick.tint022@gmail.com",
                to=["kedernath.mallick.tint022@gmail.com"],
                reply_to=["kedernath.mallick.tint022@gmail.com"],
            )
        mail.content_subtype = "html"
        mail.send() 
 
class SendResetPassEmail(APIView):
    serializer_class = ResetPasswordEmailSentSerializers
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        if Users.objects.filter(email__iexact=email).exists():
            user = Users.objects.get(email__iexact = email)

            # uidb64 = user id encoded in base 64
            # "reset/<uidb64>/<token>/"

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token  = PasswordResetTokenGenerator().make_token(user=user)
            
            # 127.0.0.1:8000
            curr_site = get_current_site(request=request).domain
            site_name = get_current_site(request=request).name

            url = reverse_lazy("password_reset_confirm",kwargs={
                "uidb64" : uidb64,
                "token" :token
            })

            final_password_reset_link = curr_site+str(url)

            subject_template_name = "email/password_reset_subject.txt"
            email_template_name = None
            from_email = "kedernath.mallick.tint022@gmail.com"
            to_email = email
            html_email_template_name="email/reset_pass.html"


            context = {
                    "resetPass_url" : final_password_reset_link
                }
            message = get_template("email/reset_pass.html").render(context)

            send_mail(subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name , message )


        return Response({"final_link" : final_password_reset_link},status=status.HTTP_200_OK)

class ResetPassTODB(APIView):
    serializer_class = ResetPasswordSerializers

    def get_user(self, uidb64):
        try: 
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Users._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            Users.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
    def post(self,request,*args,**kwargs):

        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        user = self.get_user(uidb64)
        serializer.save(user)
        
        return Response(UsersModelSerailizers(self.get_user(uidb64)).data, status = status.HTTP_200_OK)

##### social authentication using google#######



#################