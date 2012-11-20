from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from heliosauth.security import get_user
from helios.view_utils import render_template

from helios.models import Election


def home(request):
  user = get_user(request)
  return render_template(request, "zeus/home", {'menu_active': 'home',
                                                        'user': user})

def faqs_trustee(request):
  user = get_user(request)
  return render_template(request, "zeus/faqs_admin", {'menu_active': 'faqs',
                                                      'submenu': 'admin', 'user': user})
def faqs_voter(request):
  user = get_user(request)
  return render_template(request, "zeus/faqs_voter", {'menu_active': 'faqs',
                                                      'submenu': 'voter',
                                                        'user': user})
def resources(request):
  user = get_user(request)
  return render_template(request, "zeus/resources", {'menu_active': 'resources',
                                                     'user': user})

def stats(request):
    user = get_user(request)
    uuid = request.GET.get('uuid', None)
    election = None

    if uuid:
        election = Election.objects.filter(uuid=uuid)
        if not user or not user.superadmin_p:
          election = election.filter(is_completed=True)

        election = election.defer('encrypted_tally', 'result')[0]

    if user.superadmin_p:
      elections = Election.objects.filter(is_completed=True)
    else:
      elections = Election.objects.filter(is_completed=True)

    elections = elections.order_by('-created_at').defer('encrypted_tally',
                                                        'result')

    return render_template(request, 'zeus/stats', {'menu_active': 'stats',
                                                   'election': election,
                                                   'uuid': uuid,
                                                   'user': user,
                                                   'elections': elections})
