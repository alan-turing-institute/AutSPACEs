from openhumans.models import OpenHumansMember

def create_auth_url(request):
    auth_url = OpenHumansMember.get_auth_url()
    return {'auth_url': auth_url}
