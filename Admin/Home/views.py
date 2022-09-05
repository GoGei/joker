from django.shortcuts import render
# from core.Utils.Access.decorators import manager_required


# @manager_required
def admin_home_view(request):
    return render(request, 'Admin/admin_home.html')
