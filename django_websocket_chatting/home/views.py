from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


def front_view(request):
    return render(request, 'front/hello.html')

@login_required
def index(request):
    return render(request, 'main/index.html')

