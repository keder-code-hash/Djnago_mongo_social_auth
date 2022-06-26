from django.urls import include, path
from rest_framework import routers 
from .views import ResetPassTODB,LogInView,LogOutView,SendResetPassEmail,RegisterView,GetGoogleProfDetails
from rest_framework.authtoken import views

from rest_framework_simplejwt.views import ( 
    TokenRefreshView,
)
from django.urls.conf import include
from django.contrib.auth import views
 

from .views import  UserModelViewSet 

router = routers.DefaultRouter()
router.register(r'authors',UserModelViewSet) 


urlpatterns = [ 
    path('',include(router.urls)),# api for users activity
    path('register/',
        RegisterView.as_view(),
        name = "register"
    ),
    path('login/',
        LogInView.as_view(),
        name = "login"
    ),
    path('logout/',
        LogOutView.as_view(),
        name="logout"
    ),
    path('',include(router.urls)),

    path('token/refresh/',
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),

    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),

    # password reset
    path("password_reset/", 
        SendResetPassEmail.as_view(), 
        name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        ResetPassTODB.as_view(),
        name="password_reset_confirm",
    ),


    ####social auth####
    path("get_google_details/",GetGoogleProfDetails.as_view())

    ####################




    # path('fabrix/datasource/<int:fabrix_id>/',DataSourceTypeView.as_view(),name ="dtat_source_type") ,
    # path('test/',FabrixView.as_view(),name = "test")
]
