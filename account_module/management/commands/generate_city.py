import os
import csv

from django.core.management.base import BaseCommand

import data
from account_module.models import (
    Province, City
)


class Command(BaseCommand):
    help = 'Generate all data'

    def add_arguments(self, parser):
        """initialize arguments"""
        pass

    def read_csv(self, path):
        with open(path, encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                print(row)
            return csv_reader

    def generate_province(self, path):
        with open(path, encoding='utf-8') as f:
            data = csv.DictReader(f)
            province_objs = [
                Province(
                    # id=int(row.get('id')),
                    name=row.get('name'),
                ) for row in data
            ]
            Province.objects.bulk_create(province_objs)
            print('Province Objects Created Successfully')


    def generate_city(self, path):
        with open(path, encoding='utf-8') as f:
            data = csv.DictReader(f)
            city_objs = []
            for row in data:
                province_name = row.get('Province')
                try:
                    province = Province.objects.get(name=province_name)
                except Province.DoesNotExist:
                    print(f"Skipping city '{row.get('City')}', province '{province_name}' not found.")
                    continue
                city_objs.append(City(name=row.get('City'), province=province))
            City.objects.bulk_create(city_objs)
            print('City Objects Created Successfully')


    def handle(self, *args, **options):
        province_data_path = os.path.abspath(data.__file__).replace('__init__.py', 'province.csv')
        city_data_path = os.path.abspath(data.__file__).replace('__init__.py', 'city.csv')

        self.generate_province(province_data_path)
        self.generate_city(city_data_path)

        self.stdout.write(
            self.style.SUCCESS('Data generated successfully.')
        )
