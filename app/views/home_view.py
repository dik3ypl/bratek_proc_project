from django.shortcuts import render


def home_view(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'app/home.html', locals())
