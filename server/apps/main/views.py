import datetime
import io
import json
import logging
import uuid

import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.forms.models import model_to_dict 
from django.shortcuts import redirect, render
from openhumans.models import OpenHumansMember
from django.db.models import Q
from django.contrib.auth.models import Group


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

def share_experience(request, uuid=False):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated: 
        
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ShareExperienceForm(request.POST)
            # check whether it's valid:

            if form.is_valid():
                
                if uuid: 
                    # we will be here if we are editing a record that already exists               
                    # for OH we need to Delete before reupload.
                    request.user.openhumansmember.delete_single_file(file_basename = f"{uuid}.json")
                
                else:
                    uuid = make_uuid()
                                
                upload(data = form.cleaned_data, uuid = uuid, ohmember = request.user.openhumansmember)                
                
                # for Public Experience we need to check if it's viewable and update accordingly.
                update_public_experience_db(data=form.cleaned_data, uuid=uuid, ohmember=request.user.openhumansmember)                
                
                # redirect to a new URL:
                return redirect('main:confirm_page')

        # if a GET (or any other method) we'll create a blank form
        else:
            
            if uuid:
                # return data from oh.
                data = get_oh_file(ohmember=request.user.openhumansmember, uuid=uuid)
                form = ShareExperienceForm(data["metadata"]["data"])
                
            else:
                form = ShareExperienceForm()
                
            return render(request, 'main/share_experiences.html', {'form': form, 'uuid':uuid})    
    
    else:    
        return redirect('index')

def update_public_experience_db(data, uuid, ohmember):
    """Updates the public experience database for the given uuid.
    
    If data is tagged as viewable, an experience will be updated or inserted.
    If a data is tagged as not public, this function ensures that it is absent from the pe db.

    Args:
        data (dict): an experience
        uuid (str): unique identifier
        ohmember : request.user.openhumansmember
        moderation_status (str, optional): Defaults to 'in review'.
    """
    
    if data['viewable']:
        
        pe = PublicExperience(experience_text=data['experience'],
            difference_text=data['wish_different'],
            title_text=data['title'],
            open_humans_member=ohmember,
            experience_id=uuid,
            abuse=data['abuse'],
            violence=data['violence'],
            drug=data['drug'],
            mentalhealth=data['mentalhealth'],
            negbody=data['negbody'],
            other=data['other'],
            moderation_status=data['moderation_status'],
            research = data['research']
        )
        
        # .save() updates if primary key exists, inserts otherwise. 
        pe.save()        
        
    else:
        delete_PE(uuid,ohmember)
        
            
def delete_PE(uuid, ohmember):
    if PublicExperience.objects.filter(experience_id=uuid, open_humans_member=ohmember).exists():
            PublicExperience.objects.get(experience_id=uuid, open_humans_member=ohmember).delete()
        
    
def make_uuid():
    return str(uuid.uuid1())

def upload(data, uuid, ohmember):
    """Uploads a dictionary representation of an experience to open humans.

    Args:
        data (dict): an experience
        uuid (str): unique identifier
        ohmember : request.user.openhumansmember
    """
    
    output_json = {
            'data': data,
            'timestamp': str(datetime.datetime.now())}
    
    # by saving the output json into metadata we can access the fields easily through request.user.openhumansmember.list_files().
    metadata = {
        'uuid': uuid,   
        'description': data.get('title'),
        'tags': make_tags(data),
        **output_json,
        }
    
    # create stream for oh upload
    output = io.StringIO()
    output.write(json.dumps(output_json))
    output.seek(0)
            

    ohmember.upload(
        stream=output,
        filename=f"{uuid}.json", #filename is Autspaces_timestamp
        metadata=metadata)

def make_tags(data):
    """builds list of tags based on data"""
    
    tag_map = {'viewable': {'True':'public',
                            'False':'not public'},
               'research': {'True':'research',
                            'False':'non-research'},
                'drug':    {'True': 'drugs',
                            'False': ''},
                'abuse':    {'True': 'abuse',
                            'False': ''},
                'negbody':  {'True': 'negative body',
                            'False': ''},
                'violence': {'True': 'violence',
                            'False': ''},
                'mentalhealth': {'True': 'mental health',
                            'False': ''},
                'moderation_status': {'True': '',
                            'False': 'in review'}
                            }
    
    tags = [tag_map[k].get(str(v)) 
            for k,v in data.items() 
            if k in tag_map.keys()]
    if data["other"] != '':
        tags.append("Other triggering label")
    
    return tags
    
def delete_experience(request, uuid, title):
    # TODO: we currently are passing title via url because it is nice to display it in the confirmation. We could improve the deletion process by having a javascript layover.
    
    if request.user.is_authenticated:
    
        if request.method == 'POST':
        
            delete_single_file(uuid = uuid,
                               ohmember = request.user.openhumansmember)
            
                
            return render(request, 'main/deletion_success.html', {"title":title})
        
        else:
            return render(request, 'main/deletion_confirmation.html', {"title": title,
                                                                       "uuid": uuid})
    else:    
        return redirect('index')
        
    
def delete_single_file(uuid, ohmember):
    """Deletes a given file id and uuid from openhumans and ensures absence from local PublicExperiences database.

    Args:
        
        uuid (str): unique identifier, used for PublicExperience primary key and for OpenHumans filename.
        ohmember : request.user.openhumansmember
    """

    ohmember.delete_single_file(file_basename=f"{uuid}.json")
    delete_PE(uuid,ohmember)
    
def get_oh_file(ohmember, uuid):
    """Returns a single file from OpenHumans, filtered by uuid.

    Args:
        ohmember : request.user.openhumansmember
        uuid (str): unique identifier

    Raises:
        Exception: If uuid belongs to more than one file.

    Returns:
        file (dict): dictionary representation of OpenHumans file. Returns None if uuid is not matched.
    """
    files = ohmember.list_files()
    file = [f for f in files if f["metadata"]["uuid"]==uuid]
    
    if len(file)==0:
        file=None
    elif len(file)>1:
        raise Exception("duplicate uuids in open humans")
    
    return file[0]
    


def list_files(request):
    if request.user.is_authenticated:
        context = {'files': request.user.openhumansmember.list_files()}
        return render(request, 'main/list.html',
                      context=context)
    return redirect('index')


def list_public_experiences(request):
    experiences = PublicExperience.objects.all()

    return render(
        request,
        'main/experiences_page.html',
        context={'experiences': experiences})


def moderate_public_experiences(request):
    if request.user.is_authenticated and is_moderator(request.user):
        unreviewed_experiences = PublicExperience.objects.filter(moderation_status='not reviewed')
        previously_reviewed_experiences = PublicExperience.objects.filter(~Q(moderation_status='not reviewed'))
        return render(
            request,
            'main/moderate_public_experiences.html',
            context={"unreviewed_experiences": unreviewed_experiences,
            "previously_reviewed_experiences": previously_reviewed_experiences})
    else:
        return redirect("main:overview")



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

def get_review_status(files):
    """Given a list of files, count the number of each moderation status of the publicly viewable files

    Args:
        files (dict): list of files, which are dictionaries. See `upload()`.

    Returns:
        statuses (dict): counts of moderation statuses
    """
        
        
    status_list = [f['metadata']['data']['moderation_status'].replace(' ','_') for f in files if f['metadata']['data']['viewable']]
        
    statuses = {f"n_{s}":status_list.count(s) for s in set(status_list)}
    
    statuses["n_viewable"] = len(status_list)
    statuses["n_moderated"] = statuses.pop("n_approved", False) + statuses.pop("n_rejected", False)
        

    return statuses

    
def my_stories(request):
    if request.user.is_authenticated:
        context = {'files': request.user.openhumansmember.list_files()}
        statuses = get_review_status(context['files'])
        context = {**context, **statuses}
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

def moderate_experience(request, uuid):
    if request.user.is_authenticated and is_moderator(request.user):
        model = PublicExperience.objects.get(experience_id = uuid)
        form = model_to_form(model, moderate=True)
        return render(request, 'main/share_experiences.html', {'form': form, 'uuid':uuid, 'moderate':True})  
    else:
        redirect('index')

def model_to_form(model, moderate = False):
    model_dict = model_to_dict(model)

    form = ShareExperienceForm({
        "experience": model_dict["experience_text"],
        "wish_different": model_dict["difference_text"],
        "title":model_dict["title_text"],
        "abuse":model_dict["abuse"],
        "violence":model_dict["violence"],
        "drug":model_dict["drug"],
        "mentalhealth":model_dict["mentalhealth"],
        "negbody":model_dict["negbody"],
        "other":model_dict["other"],
        "viewable":True, #we only moderate public experiences
        "research":model_dict["research"],
        "moderation_status":model_dict["moderation_status"]
    }, moderate=moderate)

    return form


def is_moderator(user):
  """return membership of moderator group"""
  
  try:
    group = Group.objects.get(user=user)
    return (group.name == "Moderators")
  
  except Group.DoesNotExist:
    return False

    