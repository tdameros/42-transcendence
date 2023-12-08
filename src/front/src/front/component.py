from django.shortcuts import render
def generate_component(request, component, default_css=True, default_js=True):
    context = {}
    if default_css:
        context["css"] = f"{component}/{component}.css"
    if default_js:
        context["js"] = f"{component}/{component}.js"
    response = render(request, f"{component}/{component}.html", context=context)
    # TODO: fix it properly
    response["Access-Control-Allow-Origin"] = "http://localhost:8000"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
