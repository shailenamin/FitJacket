from django.shortcuts import render

# Create your views here.

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'events/events.html', {'template_data': template_data})