from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('rubrics/', get_rubrics, name='rubric')
]