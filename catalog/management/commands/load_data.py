from django.core.management.base import BaseCommand
import pandas as pd
from catalog.models import NetflixTitle
from datetime import datetime

class Command(BaseCommand):
    help = 'Load Netflix data from CSV'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('netflix_titles.csv')
        
        for _, row in df.iterrows():
            try:
                date_added = pd.to_datetime(row['date_added']).date() if pd.notna(row['date_added']) else None
                
                NetflixTitle.objects.create(
                    show_id=row['show_id'],
                    title_type=row['type'],
                    title=row['title'],
                    director=row['director'] if pd.notna(row['director']) else '',
                    cast=row['cast'] if pd.notna(row['cast']) else '',
                    country=row['country'] if pd.notna(row['country']) else '',
                    date_added=date_added,
                    release_year=int(row['release_year']),
                    rating=row['rating'] if pd.notna(row['rating']) else '',
                    duration=row['duration'],
                    genres=row['listed_in'],
                    description=row['description']
                )
            except Exception as e:
                print(f"Error loading {row['title']}: {e}")
        
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))