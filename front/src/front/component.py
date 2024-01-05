from django.shortcuts import render
def generate_component(request, component, default_css=True, default_js=True):
    context = {}
    if default_css:
        context['css'] = f"{component}/{component}.css"
    if default_js:
        context["js"] = f"{component}/{component}.js"
    response = render(request, f"{component}/{component}.html", context=context)
    return response
