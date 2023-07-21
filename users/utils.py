from django.db.models import Q
from .models import Profiles, Skills
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def searchProfiles(request): 
    search = ''

    if request.GET.get('text'):
        search = request.GET.get('text')

    skills = Skills.objects.filter(name__icontains = search)
        

    profiles = Profiles.objects.distinct().filter(Q(name__icontains = search) | 
                                                  Q(short_intro__icontains = search)|
                                                  Q(skills__in = skills))
    

    return profiles, search



def paginate(request, profiles, results):
    
    page = request.GET.get('page')
    result = 3

    paginator = Paginator(profiles, result)


    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1


    customrange = range(leftIndex, rightIndex)


    return customrange, profiles