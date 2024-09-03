from django.db import models
import requests

class Book(models.Model):
    book_id = models.CharField(max_length=255, unique=True)
    title = models.TextField()
    author = models.TextField(blank=True)
    genre = models.TextField(blank=True)
    description = models.TextField(blank=True)
    pub_year = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return self.title

    @property
    def img_link(self):
        cover_id = self.get_cover_id()
        return f'http://covers.openlibrary.org/b/id/{cover_id}-L.jpg' if cover_id else ''

    def get_cover_id(self):
        work_url = f'https://openlibrary.org/works/{self.book_id}.json'
        response = requests.get(work_url)
        work_data = response.json()
        cover_id = work_data.get('covers', [None])[0]
        return cover_id