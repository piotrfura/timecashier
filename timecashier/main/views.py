from django.shortcuts import render
#from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def test(request):
    task_list = ['Pranie', 'Sprzątanie', 'Praca', 'Jedzenie']
    tekst = 'Jakiś tekst testowy tutaj dam...'
    languages = {
        'python': 'advanced',
        'sql': 'intermediate',
        'js': 'beginner'
    }
    context = {'tasks': task_list, 'text': tekst, 'languages':languages}
    return render(request, 'main/test.html', context)