# # The code snippet you provided is a Python script that defines a Django management command for
# loading data from a CSV file into a Django model called `EVChargingLocation`. Here's a breakdown
# of the code:
# import csv
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from core.models import EVChargingLocation


# class Command(BaseCommand):
#     help = 'Load data from EV Station file'

#     def handle(self, *args, **kwargs):
#         data_file = settings.BASE_DIR / 'core' / 'dataset' / 'yahoo_news_points_5days.csv'
        # keys = ('city', 'point')  # the CSV columns we will gather data from.
        
        # records = []
        # with open(data_file, 'r') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         records.append({k: row[k] for k in keys})

        # extract the latitude and longitude from the Point object
        # for record in records:
        #     longitude, latitude = record['point'].split("(")[-1].split(")")[0].split()
        #     record['longitude'] = float(longitude)
        #     record['latitude'] = float(latitude)

        #     # add the data to the database
        #     EVChargingLocation.objects.get_or_create(
        #         station_name=record['title'],
        #         latitude=record['latitude'],
        #         longitude=record['longitude']
        #     )
            
        #chatGPT
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import EVChargingLocation

class Command(BaseCommand):
    help = 'Load EV station data from CSV'

    def handle(self, *args, **kwargs):
        data_file = settings.BASE_DIR / 'core' / 'dataset' / 'yahoo_news_points_5days.csv'

        with open(data_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                try:
                    station_name = row['title']
                    latitude = float(row['latitude'])
                    longitude = float(row['longitude'])

                    EVChargingLocation.objects.get_or_create(
                        station_name=station_name,
                        latitude=latitude,
                        longitude=longitude
                    )
                except (KeyError, ValueError) as e:
                    self.stdout.write(self.style.WARNING(f'略過資料列: {e}'))
        
        self.stdout.write(self.style.SUCCESS('資料載入完成！'))
