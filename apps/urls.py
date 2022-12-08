from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from apps.views import MainFormView, ShortView, SigninView, SignupView

urlpatterns = [
    path('', MainFormView.as_view(), name='form_view'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('form_view')), name='logout_view'),
    path('sign-in', SigninView.as_view(), name='signin_view'),
    path('sign-up', SignupView.as_view(), name='signup_view'),
    path('<str:name>', ShortView.as_view(), name='short_view'),
]
