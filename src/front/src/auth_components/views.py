from django.shortcuts import render
from front.component import generate_component

def signup(request):
    return generate_component(request, "signup")


def signin(request):
    return generate_component(request, "signin", default_js=False)
