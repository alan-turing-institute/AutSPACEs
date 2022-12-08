import datetime
import io
import json
import logging
import uuid

import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from openhumans.models import OpenHumansMember

from .models import PublicExperience

from .forms import ShareExperienceForm

logger = logging.getLogger(__name__)


def index(request):
    """
    Starting page for app.
    """
    auth_url = OpenHumansMember.get_auth_url()
    context = {'auth_url': auth_url,
               'oh_proj_page': settings.OH_PROJ_PAGE}
    if request.user.is_authenticated:
        return redirect('main:overview')
    return render(request, 'main/home.html', context=context)


def overview(request):
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member,
                   'oh_proj_page': settings.OH_PROJ_PAGE}
        return render(request, 'main/home.html', context=context)
    return redirect('index')


def logout_user(request):
    """
    Logout user
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def share_experience(request, edit=False):
    # if this is a POST request we need to process the form data
    
    if request.method == 'POST':
        
        # create a form instance and populate it with data from the request:
        form = ShareExperienceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if not edit:
                if form.cleaned_data.pop("file_id", False):  
                    request.user.openhumansmember.delete_single_file(file_id=request.POST.get("file_id"))

                upload(form.cleaned_data, request.user.openhumansmember)                
                # redirect to a new URL:
                return redirect('main:confirm_page')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ShareExperienceForm()

    if request.user.is_authenticated:
        return render(request, 'main/share_experiences.html', {'form': form})
    else:    
        return redirect('index')

def upload(data, ohmember):
    """Uploads a dictionary representation of an experience to open humans.
    
    If the experience is tagged as viewable, it is saved to the PublicExperiences database

    Args:
        data (dict): an experience
        ohmember : request.user.openhumansmember
    """
    
    output_json = {
            'data': data,
            'timestamp': str(datetime.datetime.now())}
    
    # by saving the output json into metadata we can access the fields easily through request.user.openhumansmember.list_files().
    metadata = {
        'uuid': str(uuid.uuid1()),   
        'description':'placeholder',
        'tags': make_tags(data),
        **output_json,
        }
    
    # create stream for oh upload
    output = io.StringIO()
    output.write(json.dumps(output_json))
    output.seek(0)
            
    ohmember.upload(
        stream=output,
        filename='testfile.json',
        metadata=metadata)
        
    if data['viewable']:
        PublicExperience.objects.create(
            experience_text=data['experience'],
            difference_text=data['wish_different'],
            title_text=data['title'],
            open_humans_member=ohmember,
            experience_id=metadata['uuid'])

def make_tags(data):
    """builds list of tags based on data"""
    
    tag_map = {'viewable': {'True':'public',
                            'False':'not public'},
               'research': {'True':'research',
                            'False':'non-research'}}
    
    # TODO: do we want to add tags for the triggering checkboxes herte?
    
    tags = [tag_map[k].get(str(v)) 
            for k,v in data.items() 
            if k in tag_map.keys()]
    
    return tags
    
    

def list_files(request):
    if request.user.is_authenticated:
        context = {'files': request.user.openhumansmember.list_files()}
        return render(request, 'main/list.html',
                      context=context)
    return redirect('index')


def list_public_experiences(request):
    # experiences = PublicExperience.objects.filter(approved='approved')
    experiences = PublicExperience.objects.all()
    return render(
        request,
        'main/experiences_page.html',
        context={'experiences': experiences})


def moderate_public_experiences(request):
    experiences = PublicExperience.objects.filter(approved='not reviewed')
    return render(
        request,
        'main/moderate_public_experiences.html',
        context={'experiences': experiences})


def review_experience(request, experience_id):
    experience = PublicExperience.objects.get(experience_id=experience_id)
    print(experience)
    experience.approved = 'approved'
    experience.save()
    print(experience.approved)
    return redirect('moderate_public_experiences')


def make_non_viewable(request, oh_file_id, file_uuid):
    pe = PublicExperience.objects.get(experience_id=file_uuid)
    pe.delete()
    oh_files = request.user.openhumansmember.list_files()
    for f in oh_files:
        if str(f['id']) == str(oh_file_id):
            experience = requests.get(f['download_url']).json()
            new_metadata = f['metadata']
            new_metadata['tags'] = ['not public'] + f['metadata']['tags'][1:]
            output = io.StringIO()
            output.write(json.dumps(experience))
            output.seek(0)
            request.user.openhumansmember.upload(
                stream=output,
                filename='testfile.json',
                metadata=new_metadata)
            request.user.openhumansmember.delete_single_file(file_id=oh_file_id)
    return redirect('main:list')


def make_viewable(request, oh_file_id, file_uuid):
    oh_files = request.user.openhumansmember.list_files()
    for f in oh_files:
        if str(f['id']) == str(oh_file_id):
            experience = requests.get(f['download_url']).json()
            new_metadata = f['metadata']
            new_metadata['tags'] = ['viewable'] + f['metadata']['tags'][1:]
            output = io.StringIO()
            output.write(json.dumps(experience))
            output.seek(0)
            request.user.openhumansmember.upload(
                stream=output,
                filename='testfile.json',
                metadata=new_metadata)
            request.user.openhumansmember.delete_single_file(
                file_id=oh_file_id)
            PublicExperience.objects.create(
                experience_text=experience['text'],
                difference_text=experience['wish_different'],
                open_humans_member=request.user.openhumansmember,
                experience_id=file_uuid)
    return redirect('list')


def make_non_research(request, oh_file_id, file_uuid):
    oh_files = request.user.openhumansmember.list_files()
    for f in oh_files:
        if str(f['id']) == str(oh_file_id):
            experience = requests.get(f['download_url']).json()
            new_metadata = f['metadata']
            new_metadata['tags'] = f['metadata']['tags'][:-1] + ['non-research']
            output = io.StringIO()
            output.write(json.dumps(experience))
            output.seek(0)
            request.user.openhumansmember.upload(
                stream=output,
                filename='testfile.json',
                metadata=new_metadata)
            request.user.openhumansmember.delete_single_file(
                file_id=oh_file_id)
    return redirect('list')


def make_research(request, oh_file_id, file_uuid):
    oh_files = request.user.openhumansmember.list_files()
    for f in oh_files:
        if str(f['id']) == str(oh_file_id):
            experience = requests.get(f['download_url']).json()
            new_metadata = f['metadata']
            new_metadata['tags'] = f['metadata']['tags'][:-1] + ['research']
            output = io.StringIO()
            output.write(json.dumps(experience))
            output.seek(0)
            request.user.openhumansmember.upload(
                stream=output,
                filename='testfile.json',
                metadata=new_metadata)
            request.user.openhumansmember.delete_single_file(
                file_id=oh_file_id)
    return redirect('list')

def edit_experience(request):
    
    print(request.POST)
    return render(request, 'main/share_experiences.html')

    # context = {}
    # if request.method == 'POST':
    #     print(request.POST)
    #     return render(request, 'main/share_experiences.html', context)
    # else:
    #     if request.user.is_authenticated:
    #         return render(request, 'main/share_experiences.html', context)
    # redirect('main:my_stories')

def signup(request):
    return render(request, "main/signup.html")

def registration(request):
    registration_status = True
    print(registration_status)
    return render(request, "main/registration.html", {'page_status': 'registration'})

def signup_frame4_test(request):
    return render(request, "main/signup1.html")

def my_stories(request):
    if request.user.is_authenticated:
        context = {'files': request.user.openhumansmember.list_files()}
        print(context)
        return render(request, "main/my_stories.html", context)
    else:
        return redirect("main:overview")


def confirmation_page(request):
    """
    Confirmation Page For App
    """
    return render(request, "main/confirmation_page.html")


def about_us(request):
    return render(request, "main/about_us.html")

# def what_autism_is(request):
#     auth_url = OpenHumansMember.get_auth_url()
#     context = {'auth_url': auth_url,
#                'oh_proj_page': settings.OH_PROJ_PAGE}
#     if request.user.is_authenticated:
#         return redirect('main:what_autism_is')
#     return render(request, 'main/what_autism_is.html', context=context)
def navigation(request):
    return render(request, "main/navigation.html")

# def about_us(request):
#     return render(request, "main/about_us.html")

def what_autism_is(request):
    return render(request, "main/what_autism_is.html")

def footer(request):
    return render(request, "main/footer.html")

