from django.urls import path
from .views import *
urlpatterns=[
    path('register/',register_view),
    path('login/',login_view),
    path('list_users/',user_details_view),
    path('user_details/',CurrentUserDetailsView.as_view()),
    path('my_referrals/',my_referrals_view),
]