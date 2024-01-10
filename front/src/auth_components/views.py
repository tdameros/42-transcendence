from django.shortcuts import render
from front.component import generate_component

def signup(request):
    return generate_component(request, "signup")


def signin(request):
    return generate_component(request, "signin")

def reset_password_email(request):
    return generate_component(request, "reset_password_email")
