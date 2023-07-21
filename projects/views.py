from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm, AddTag, Reviewform
from django.contrib import messages
from django.db.models import Q
from .utils import searchProjects, paginate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.utils import IntegrityError

def projects(request):

    project, search = searchProjects(request)

    customrange, project = paginate(request, project, 3)


    return render(request, 'projects/projects.html', {'pro':project, 'search':search, 'customrange':customrange})


def project(request, pk):
    project = Project.objects.get(id=pk)
    if request.user.is_authenticated:
        profile = request.user.profiles
    form = Reviewform()
    owners = project.reviewers

    if request.method == 'POST':
        form = Reviewform(request.POST)
        try:
            if form.is_valid():
                review = form.save(commit=False)
                review.owner = profile
                review.project = project
                review.save()
                project.getVoteCount
                messages.success(request, 'Your review was successfully submitted')
                return redirect('project', pk=project.id)
            

        except IntegrityError:
            messages.error(request, "You've already reviewed this project!!")
            return redirect('project', pk=project.id)



    return render(request, 'projects/single-project.html', {'pr':project, 'form':form, 'owners':owners }) 




@login_required(login_url='login')
def create_project(request):
    profile = request.user.profiles
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        tagss = request.POST.get('newtags').replace(',',' ').split(' ')

        tags = []

        for i in tagss:
            i = i.capitalize()
            tags.append(i)

        tags = list(filter(None,tags))


        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile

            project.save()

            for tag in tags:
                tag, created = Tag.objects.get_or_create(name = tag)
                project.tags.add(tag)


            return redirect('account')

    return render(request, 'projects/project_form.html', {'form':form})




@login_required(login_url='login')
def update_project(request, pk):


    profile = request.user.profiles

    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        tagss = request.POST.get('newtags').replace(',',' ').split(' ')
        
        tags = []

        for i in tagss:
            i = i.capitalize()
            tags.append(i)


        tags = list(filter(None,tags))

        print(tags)


        
        form = ProjectForm(request.POST, request.FILES, instance=project )
        if form.is_valid():
            project = form.save()

            for tag in tags:
                tag, created = Tag.objects.get_or_create(name = tag)
                project.tags.add(tag)


            return redirect('account')

    return render(request, 'projects/project_form.html', {'form':form, 'project':project})



@login_required(login_url='login')
def delete_project(request, pk):

    profile = request.user.profiles

    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')
    return render(request, 'projects/delete_template.html', {'object':project.title})


@login_required(login_url='login')
def add_tag(request, pk):

    profile = request.user.profiles
    project = profile.project_set.get(id=pk)
    form = AddTag(instance=project)

    if request.method == 'POST':
        form = AddTag(request.POST, instance=project )
        if form.is_valid():
            form.save()

    return render(request, 'projects/tagadd.html', {'form':form})