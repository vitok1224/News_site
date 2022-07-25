from django.shortcuts import render
from .models import Rubric


def index(request):
    return render(request, "Menu/rubric.html", {'rubrics': Rubric.objects.all()})

def get_rubrics():
    pass