from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def searchProjects(request):
    search = ''

    if request.GET.get('text'):
        search = request.GET.get('text')

    tags = Tag.objects.filter(name__icontains = search)

    
    project = Project.objects.distinct().filter( Q(title__icontains = search) |
                                                Q(tags__in = tags) |
                                                Q(owner__name__icontains = search)

    )

    return project, search



def paginate(request, project, results):
    
    page = request.GET.get('page')
    result = 3

    paginator = Paginator(project, result)


    try:
        project = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        project = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        project = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1


    customrange = range(leftIndex, rightIndex)


    return customrange, project