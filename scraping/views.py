from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy

def home_view(request):
    # print(request.GET)
    form = FindForm()

    return render(request, 'scraping/home.html', {
        'form': form
    })

def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    # qs = []
    # page_obj = []
    context = {
        'city': city,
        'language': language,
        'form': form,
    }
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city  # т.к. это ForeignKey к модели City - полю slug
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 5) # Show 5 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj

    return render(request, 'scraping/list.html', context)

