from django.test import TestCase
from django.contrib import auth
from django.test import Client
from django.db import models
from server.apps.main.models import PublicExperience
from django.contrib.auth.models import User
import vcr
import urllib
from server.apps.main.forms import ShareExperienceForm


from openhumans.models import OpenHumansMember


class Views(TestCase):
    """
    Tests the views function
    """

    def setUp(self):
        """
        Set-up for test with two users
        """
        # Placeholder data
        data = {"access_token": "123456", "refresh_token": "bar", "expires_in": 36000}

        # Create user A
        self.oh_a = OpenHumansMember.create(oh_id=12345678, data=data)
        self.oh_a.save()
        self.user_a = self.oh_a.user
        self.user_a.openhumansmember = self.oh_a
        self.user_a.set_password("password_a")
        self.user_a.save()
        # Create user B
        self.oh_b = OpenHumansMember.create(oh_id=87654321, data=data)
        self.oh_b.save()
        self.user_b = self.oh_b.user
        self.user_b.openhumansmember = self.oh_b
        self.user_b.set_password("password_a")
        self.user_b.save()

        # Each with a public experience
        pe_data = {
            "experience_text": "Here is some experience text",
            "difference_text": "Here is some difference text",
            "title_text": "Here is the title",
        }
        approved = {
            "experience_text": "This is an approved story",
            "difference_text": "This is some approved difference text",
            "title_text": "An approved title",
            "moderation_status": "approved",
        }
        approved_with_trigger = {
            "experience_text": "This is an approved story with caramel",
            "difference_text": "This is some approved difference text",
            "title_text": "An approved title",
            "moderation_status": "approved",
            "abuse": True,
        }
        rejected_with_trigger = {
            "experience_text": "This is a rejected story with sundaes",
            "difference_text": "This is some rejected difference text",
            "title_text": "A rejected title",
            "moderation_status": "rejected",
            "mentalhealth": True,
        }
        self.pe_a = PublicExperience.objects.create(
            open_humans_member=self.oh_a, experience_id="1234_1", **pe_data
        )
        self.pe_a = PublicExperience.objects.create(
            open_humans_member=self.oh_a, experience_id="1234_2", **pe_data
        )
        self.pe_b = PublicExperience.objects.create(
            open_humans_member=self.oh_b, experience_id="8765_1", **approved
        )
        self.pe_b = PublicExperience.objects.create(
            open_humans_member=self.oh_b,
            experience_id="8765_2",
            **approved_with_trigger
        )
        self.pe_b = PublicExperience.objects.create(
            open_humans_member=self.oh_b,
            experience_id="8765_3",
            **rejected_with_trigger
        )

    def test_confirm_page(self):
        c = Client()
        unauthorised_response = c.get("/main/confirm_page/")
        # Redirect when logged out
        assert unauthorised_response.status_code == 302
        c.force_login(self.user_a)
        response = c.get("/main/confirm_page/")
        assert response.status_code == 200

    def test_about_us(self):
        c = Client()
        response = c.get("/main/about_us/")
        assert response.status_code == 200

    def test_what_autism_is(self):
        c = Client()
        response = c.get("/main/what_autism_is/")
        assert response.status_code == 200

    def test_help(self):
        c = Client()
        response = c.get("/main/help/")
        assert response.status_code == 200

    def test_code_of_conduct(self):
        c = Client()
        response = c.get("/main/code_of_conduct/")
        assert response.status_code == 200

    def test_registration(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.get("/main/registration/")
        assert response.status_code == 200

    def test_logout_user(self):
        """
        Test that a user can log themselves out
        """
        c = Client()

        # Pre-login. Get redirected to home
        pre_login = c.get("/main/share_exp/", follow=True)
        self.assertTemplateUsed(pre_login, "main/home.html")

        # Logged in go to the share experiences page
        c.force_login(self.user_a)
        logged_in_response = c.get("/main/share_exp/", follow=True)
        self.assertTemplateUsed(logged_in_response, "main/share_experiences.html")

        # Log out the user using AutSPACEs. Get redirected to home
        c.post("/main/logout/")
        logged_out_response = c.get("/main/share_exp/", follow=True)
        self.assertTemplateUsed(logged_out_response, "main/home.html")

    @vcr.use_cassette(
        "server/apps/main/tests/fixtures/view_exp.yaml",
        record_mode="none",
        filter_query_parameters=["access_token"],
        match_on=["path"],
    )
    def test_view_exp_logged_in(self):
        """
        Test that a user can view their experience when logged in and gets redirected to overview when not
        """
        c = Client()
        unauthorised_response = c.get(
            "/main/view/33b30e22-f950-11ed-8488-0242ac140003/"
        )
        assert unauthorised_response.status_code == 302
        unauthorised_response_f = c.get(
            "/main/view/33b30e22-f950-11ed-8488-0242ac140003/", follow=True
        )
        self.assertTemplateUsed(unauthorised_response_f, "main/home.html")
        c.force_login(self.user_a)
        response = c.get(
            "/main/view/33b30e22-f950-11ed-8488-0242ac140003/", follow=True
        )
        self.assertContains(
            response, "This is a simple short story for testing", status_code=200
        )

    def test_share_exp(self):
        """
        Check that non-authorised users are redirected (to index, then home) - get
        logic:
            request.user.is_authenticated == False
        """
        c = Client()
        response = c.get("/main/share_exp/")
        assert response.status_code == 302

    def test_share_exp_logged_in(self):
        """
        Test that logged in members are taken to the correct page
        logic:
            request.user.is_authenticated == True
        """
        c = Client()
        c.force_login(self.user_a)
        response = c.get("/main/share_exp/")
        assert response.status_code == 200

    @vcr.use_cassette(
        "server/apps/main/tests/fixtures/share_experience.yaml",
        record_mode="none",
        filter_query_parameters=["access_token"],
        match_on=["path"],
    )
    def test_share_exp_submit_new_experience(self):
        """
        Test that user can submit a new experience of their own
        logic:
            request.user.is_authenticated == True
            request.method == "POST"
            form.is_valid() == True
            uuid == False

        """
        # Cannot confirm creation of a new UUID
        # Need to confirm upload of the (cleaned) data to that user's OH account [X]
        # Need to confirm update of the PE database [X]
        # Need to confirm redirection to confirm page

        c = Client()
        c.force_login(self.user_a)

        user_a_stories_before = len(
            PublicExperience.objects.filter(open_humans_member=self.oh_a)
        )

        response = c.post(
            "/main/share_exp/",
            {
                "experience_text": "Here is some experience text",
                "difference_text": "Here is some difference text",
                "title_text": "A new story added",
                "viewable": "True",
                "open_humans_member": self.oh_a,
            },
            follow=True,
        )

        user_a_stories_after = len(
            PublicExperience.objects.filter(open_humans_member=self.oh_a)
        )

        pe_db_after = PublicExperience.objects.filter(title_text="A new story added")

        # Check that a story with the title now exists in the database
        assert len(pe_db_after) == 1

        # Check that there is one new story for user A
        assert user_a_stories_after == user_a_stories_before + 1

        # Check that there is a redirect after
        assert response.status_code == 200

    @vcr.use_cassette(
        "server/apps/main/tests/fixtures/share_experience.yaml",
        record_mode="none",
        filter_query_parameters=["access_token"],
        match_on=["path"],
    )
    def test_share_exp_missing_data(self):
        """
        Test that user cannot submit a new experience if required data is missing
        """
        # Check that redirects back to form with alerts displayed
        # Check that no experience is created

        c = Client()
        c.force_login(self.user_a)

        user_a_stories_before = len(
            PublicExperience.objects.filter(open_humans_member=self.oh_a)
        )

        response = c.post(
            "/main/share_exp/",
            {
                "experience_text": "",
                "difference_text": "",
                "title_text": "",
                "viewable": "True",
                "open_humans_member": self.oh_a,
            },
            follow=True,
        )

        user_a_stories_after = len(
            PublicExperience.objects.filter(open_humans_member=self.oh_a)
        )

        pe_db_after = PublicExperience.objects.filter(title_text="A new story added")

        # Check that story has not been added to the database
        assert len(pe_db_after) == 0

        # Check that is no new story for user A
        assert user_a_stories_after == user_a_stories_before 

        # Check that there is a redirect after
        assert response.status_code == 200

        self.assertIn("Choose a title for your story: This field is required.",str(response.content))
        self.assertIn("What could have made your experience better?: This field is required.",str(response.content))
        self.assertIn("Please share your experience: This field is required.",str(response.content))

    @vcr.use_cassette(
        "server/apps/main/tests/fixtures/load_to_edit.yaml",
        record_mode="none",
        filter_query_parameters=["access_token"],
        match_on=["path"],
    )
    def test_share_exp_load_to_edit(self):
        """
        Test that the share experience form is populated with the appropriate fields
        from that user's specific PublicExperience.
        logic:
            request.user.is_authenticated == True
            request.method == "GET"
            uuid == True
        """

        c = Client()
        c.force_login(self.user_a)
        response = c.get(
            "/main/edit/33b30e22-f950-11ed-8488-0242ac140003/", follow=True
        )
        self.assertContains(
            response, "This is a simple short story for testing", status_code=200
        )
        self.assertNotContains(response, "It is certainly an unpleasant thing,")


    def test_edit_exp_missing_data(self):
        """
        Test that editing an existing experience also fails gracefully 
        if there's missing data
        """

        c = Client()
        c.force_login(self.user_a)
        response = c.post(
            "/main/edit/1234_1/", 
                   {
                "experience_text": "",
                "difference_text": "",
                "title_text": "",
                "viewable": "True",
                "open_humans_member": self.oh_a,
            },
            follow=True
        )
        self.assertIn("This field is required",str(response.content))

    @vcr.use_cassette(
        "server/apps/main/tests/fixtures/delete_exp.yaml",
        record_mode="none",
        filter_query_parameters=["access_token"],
        match_on=["path"],
    )
    def test_delete_experience(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.post(
            "/main/delete/3653328c-f956-11ed-9803-0242ac140003/Placeholder%20text/"
        )
        assert response.status_code == 200

    def test_list_public_exp(self):
        c = Client()
        c.force_login(self.user_a)
        response = c.post("/main/public_experiences/")

        # Check that there is only one story visible - the one with no triggering labels
        for item in response.context[0]:
            if item.keys().__contains__("experiences"):
                assert len(item['experiences']) == 1

        # If you allow the abuse tag there should be 2 stories one with no tags one with the abuse tag
        search_response_abuse = c.get("/main/public_experiences/", {"searched": "", "abuse": True})
        for item in search_response_abuse.context[0]:
            if item.keys().__contains__("experiences"):
                assert len(item['experiences']) == 2

        # Results for story containing caramel is none as there is no triggering warning tag used
        search_response_c = c.get("/main/public_experiences/", {"searched": "caramel"})
        for item in search_response_c.context[0]:
            if item.keys().__contains__("experiences"):
               assert len(item['experiences'])==  0

        # Results for story containing caramel when the wrong trigger label is used is 0
        search_response_c_nb = c.get("/main/public_experiences/", {"searched": "caramel", "negbody": True})
        for item in search_response_c_nb.context[0]:
            if item.keys().__contains__("experiences"):
               assert len(item['experiences']) ==  0

        # Results for story containing caramel is 1 when there is no triggering warning tag used
        search_response_c = c.get("/main/public_experiences/", {"searched": "caramel", "all_triggers": True})
        for item in search_response_c.context[0]:
            if item.keys().__contains__("experiences"):
               assert len(item['experiences']) ==  1

        # Results for story containing sausages is no stories
        search_response = c.get("/main/public_experiences/", {"searched": "sausages"})
        for item in search_response.context[0]:
            if item.keys().__contains__("experiences"):
                assert len(item['experiences']) ==  0

        # One triggering story visible
        search_response_t = c.get(
            "/main/public_experiences/", {"searched": "", "triggering_stories": "True"}
        )
        for item in search_response_t.context[0]:
            if item.keys().__contains__("experiences"):
                assert len(item['experiences']) == 1

    def test_single_story(self):
        c = Client()
        c.force_login(self.user_a)

        # Check approved story is shown
        r_approved_story = c.get("/main/single_story/8765_1/")
        assert r_approved_story.status_code == 200
        for item in r_approved_story.context[0]:
            if "experiences" in item:
                assert item["experiences"].count() == 1
                for experience in item["experiences"]:
                    assert experience.title_text == "An approved title"

        # Check redirect if invalid UUID given
        r_bad_uuid = c.get("/main/single_story/this-is-an-invalid-uuid/", follow=True)
        self.assertRedirects(r_bad_uuid, "/main/overview")

        # Check that rejected story isn't shown
        r_rejected_story = c.get("/main/single_story/8765_3/")
        self.assertRedirects(r_rejected_story, "/main/overview")
     
    def test_list_public_exp_pagination(self):
        c = Client()
        c.force_login(self.user_a)

        # Creating 15 more experiences to have a total of 16 public, non-triggering experiences. 
        # Assuming items_per_page = 10, we should have 2 pages.
        pe_data = {
        "experience_text": "This is my experience",
        "difference_text": "Here what could have made a difference",
        "title_text": "Here is the title",
        "moderation_status": "approved",
        }
        for i in range(15):
            PublicExperience.objects.create(
                open_humans_member=self.oh_a,
                experience_id=f"1234_{i+3}",  # increment the id to make it unique
                **pe_data
            )

        # Accessing the first page
        response = c.get("/main/public_experiences/?page=1")

        # The first page should have 10 experiences
        assert len(response.context["experiences"]) == 10

        # The first item on the first page should be the 1st item overall
        assert response.context["experiences"][0].number == 1

        # Accessing the second page
        response = c.get("/main/public_experiences/?page=2")

        # The second page should have 6 experiences
        print(f'length of experiences: {len(response.context["experiences"])}')
        assert len(response.context["experiences"]) == 6

        # The first item on the second page should be the 11th item overall
        assert response.context["experiences"][0].number == 11
