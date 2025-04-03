from django.shortcuts import render

# Create your views here.

def index(request):
    template_data = {}
    template_data['title'] = 'Fit Jacket'
    is_admin = request.user.groups.filter(name="admin").exists()
    template_data['is_admin'] = is_admin
    return render(request, 'home/index.html', {'template_data': template_data})

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})