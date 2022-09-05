from django.shortcuts import render


def home_view(request):
    return render(request, 'Public/public_home.html')
