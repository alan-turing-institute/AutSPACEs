from .models import PublicExperience
from django.contrib.syndication.views import Feed
from django.urls import reverse
from server.apps.main.helpers import extract_triggers_to_show, expand_filter
from django.utils.feedgenerator import Atom1Feed

class PublicExperienceFeed(Feed):
	description_template = "main/feed.html"

	def get_object(self, request):
		# check if 'all triggers' is in keys
		all_triggers = request.GET.get("all_triggers", False)
		# set all trigger labels if set
		if all_triggers:
			allowed_triggers = {
	            "abuse",
	            "violence",
	            "drug",
	            "mentalhealth",
	            "negbody",
	            "other",
        	}
		else:
        	# Check the allowed triggers
			allowed_triggers = set(request.GET.keys())
		triggers_to_show = extract_triggers_to_show(allowed_triggers)
		return triggers_to_show

	def title(self, obj):
		return "AutSPACEs public experiences"

	def link(self, obj):
		return reverse("main:public_experiences")

	def description(self, obj):
		joined_triggers = ", ".join(obj)
		if joined_triggers:
			return "This feed includes potentially triggering stories related to %s" % joined_triggers
		else:
			return "No triggering content is included in this feed"

	def item_link(self, item):
		return reverse('main:single_story', args=[item.experience_id])
	
	def item_title(self, item):
		return item.title_text

	def item_pubdate(self, item):
		return item.created_at

	def items(self, obj):
		experiences = PublicExperience.objects.filter(moderation_status="approved")
		experiences = expand_filter(experiences, obj)
		experiences = experiences.order_by("-created_at")[:10]
		return experiences

class PublicExperienceAtomFeed(PublicExperienceFeed):
	feed_type = Atom1Feed
	subtitle = PublicExperienceFeed.description