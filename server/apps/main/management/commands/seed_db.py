from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember
from server.apps.main.models import PublicExperience
import csv

class Command(BaseCommand):
    help = 'Process so far unprocessed data sets'

    def add_arguments(self, parser):
        parser.add_argument(
            "-f, --file",
            dest="file",
            required=True,
            help="the CSV file with experiences to import",
            )

    def handle(self, *args, **options):
        file_name = options["file"]
        
        # create OH member for public experience import
        data = {"access_token": 'foo',
                "refresh_token": 'bar',
                "expires_in": 36000}
        oh_member = OpenHumansMember.create(oh_id='999999999',
                                                 data=data)
        oh_member.save()


        # iterate over CSV file, 
        # expects first row to be header and then 4 columns
        # 1. title, 2. experience text, 3. difference text
        # 4. (optional entry): which trigger label applies

        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i,row in enumerate(reader):
                if i > 0:
                    pe_data = {
                        "title_text": row[0],
                        "experience_text": row[1],
                        "difference_text": row[2],
                        "moderation_status": "approved",
                        "first_hand_authorship": "True",
                    }
                    if row[3]:
                        pe_data[row[3]] = True                    
                    PublicExperience.objects.create(
                        open_humans_member=oh_member, experience_id=str(i), **pe_data)
