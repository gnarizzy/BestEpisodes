from django.shortcuts import render


# Shows two unique, randomly selected episodes with screenshot, title, and description
def home(request):
    return render(request, 'home.html')
