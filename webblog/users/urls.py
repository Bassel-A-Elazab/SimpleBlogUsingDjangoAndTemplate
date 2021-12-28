from django.urls import path

from.views import SignUp, activate


app_name = 'users'


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('my-account/activate/<str:uid>/<str:token>', activate, name='activate'),
]
