from django.core.management.base import BaseCommand
from books.models import Book
import requests

class Command(BaseCommand):
    help = 'Load book data from Open Library API using Work IDs'

    def handle(self, *args, **kwargs):
        subject = 'Computer Science'
        language = 'eng'
        limit = 100
        page = 1
        base_search_url = 'https://openlibrary.org/search.json'
        max_books = 2000
        book_count = 0

        while True:
            search_url = f'{base_search_url}?subject={subject}&language={language}&limit={limit}&page={page}'
            search_response = requests.get(search_url)
            search_results = search_response.json().get('docs', [])

            print(f"Fetching page {page}: {search_url}")
            print(f"Number of results: {len(search_results)}")

            if not search_results:
                break

            base_work_url = 'https://openlibrary.org/works/'

            for item in search_results:
                work_id = item.get('key', '').split('/')[-1]
                work_url = f'{base_work_url}{work_id}.json'
                work_response = requests.get(work_url)
                work_data = work_response.json()

                title = work_data.get('title', '')
                authors = ', '.join(author.get('name', '') for author in work_data.get('authors', []))
                subjects = ', '.join(work_data.get('subjects', []))

                description_data = work_data.get('description', 'No description available')
                if isinstance(description_data, dict):
                    description = description_data.get('value', 'No description available')
                else:
                    description = description_data

                pub_year = work_data.get('created', {}).get('value', '')[:4]

                if description.lower() in authors.lower() or description.lower() in title.lower():
                    description = 'No description available'

                Book.objects.get_or_create(
                    book_id=work_id,
                    defaults={
                        'title': title,
                        'author': authors,
                        'genre': subjects,
                        'description': description,
                        'pub_year': pub_year,
                    }
                )
                book_count += 1

                if book_count >= max_books:
                    break

            if book_count >= max_books:
                break

            page += 1

        self.stdout.write(self.style.SUCCESS('Successfully loaded book data'))