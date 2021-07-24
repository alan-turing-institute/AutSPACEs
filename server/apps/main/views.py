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
    return render(request, 'main/landing.html', context=context)


def overview(request):
    if request.user.is_authenticated:
        oh_member = request.user.openhumansmember
        context = {'oh_id': oh_member.oh_id,
                   'oh_member': oh_member,
                   'oh_proj_page': settings.OH_PROJ_PAGE}
        return render(request, 'main/landing.html', context=context)
    return redirect('index')


def logout_user(request):
    """
    Logout user
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')


def upload(request):
    if request.method == 'POST':
        print(request.POST)
        experience_text = request.POST.get('experience')
        wish_different_text = request.POST.get('wish_different')
        viewable = request.POST.get('viewable')
        if not viewable:
            viewable = 'not public'
        research = request.POST.get('research')
        if not research:
            research = 'non-research'

        if experience_text:
            experience_id = str(uuid.uuid1())
            output_json = {
                'text': experience_text,
                'wish_different': wish_different_text,
                'timestamp': str(datetime.datetime.now())}
            output = io.StringIO()
            output.write(json.dumps(output_json))
            output.seek(0)
            metadata = {'tags': [viewable, research],
                        'uuid': experience_id,
                        'description': 'this is a test file'}
            request.user.openhumansmember.upload(
                stream=output,
                filename='testfile.json',
                metadata=metadata)
            if viewable == 'viewable':
                PublicExperience.objects.create(
                    experience_text=experience_text,
                    difference_text=wish_different_text,
                    open_humans_member=request.user.openhumansmember,
                    experience_id=experience_id)
        return redirect('main:confirm_page')
    else:
        if request.user.is_authenticated:
            return render(request, 'main/share_experiences.html')
    return redirect('index')


def list_files(request):
    if request.user.is_authenticated:
        context = {'files': request.user.openhumansmember.list_files()}
        return render(request, 'main/list.html',
                      context=context)
    return redirect('index')


def list_public_experiences(request):
    experiences = PublicExperience.objects.filter(approved='approved')
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

def signup(request):
    return render(request, "main/signup.html")

def signup_frame4_test(request):
    return render(request, "main/signup1.html")

def my_stories(request):
    context = {}

    if request.user.is_authenticated:
        return render(request, "main/my_stories.html", context)
    else:
        return redirect("main:overview")


def confirmation_page(request):
    """
    Confirmation Page For App
    """
    return render(request, "main/confirmation_page.html")
