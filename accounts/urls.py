from django.contrib.auth.decorators import login_required
from django.urls import path

from accounts.views import SignUp, SignIn, SignOut

urlpatterns = (

    path('register/', SignUp.as_view(), name='register'),
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', login_required(SignOut.as_view()), name='logout'),
)

