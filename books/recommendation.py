from books.models import Book
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_recommendations(title, num_recommendations=5):
    if not title:  # input validation for title
        raise ValueError("Title cannot be empty or None")

    if num_recommendations <= 0:  # input validation for num_recommendations
        raise ValueError("num_recommendations must be a positive integer")

    books = Book.objects.all()
    titles = [book.title for book in books]
    descriptions = [book.description for book in books]

    if not descriptions:  # handle empty descriptions list
        raise ValueError("Descriptions list cannot be empty")

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(descriptions)

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    try:
        idx = titles.index(title)  # handle ValueError if title not found
    except ValueError:
        return []  # or raise a custom exception

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    if num_recommendations > len(sim_scores) - 1:
        num_recommendations = len(sim_scores) - 1

    sim_scores = sim_scores[1:num_recommendations + 1]

    book_indices = [i[0] for i in sim_scores]
    return [books[i] for i in book_indices]