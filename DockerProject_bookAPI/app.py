from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample book data (from the given gist)
BOOKS = [
    {
        'id': 1,
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'publication_year': 1960,
        'genre': 'Southern Gothic'
    },
    {
        'id': 2,
        'title': '1984',
        'author': 'George Orwell',
        'publication_year': 1949,
        'genre': 'Dystopian Fiction'
    },
    {
        'id': 3,
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'publication_year': 1813,
        'genre': 'Romantic Novel'
    },
    {
        'id': 4,
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'publication_year': 1925,
        'genre': 'American Literature'
    },
    {
        'id': 5,
        'title': 'The Hunger Games',
        'author': 'Suzanne Collins',
        'publication_year': 2008,
        'genre': 'Young Adult Dystopian'
    }
]

# @app.route("/books", methods=["GET"])
# def get_books():
#     return jsonify(books)  # Convert the list of dictionaries to JSON and return it

@app.route('/books', methods=['GET'])
def get_books():
    genre = request.args.get('genre', '').strip().lower()
    book_id = request.args.get('id', '').strip()
    title = request.args.get('title', '').strip().lower()
    author = request.args.get('author', '').strip().lower()
    year = request.args.get('publication_year', '').strip()

    filtered_books = BOOKS

    if genre:
        filtered_books = [book for book in filtered_books if genre in book['genre'].lower()]

    if book_id:
        filtered_books = [book for book in filtered_books if str(book['id']) == book_id]

    if title:
        filtered_books = [book for book in filtered_books if title in book['title'].lower()]

    if author:
        filtered_books = [book for book in filtered_books if author in book['author'].lower()]

    if year:
        try:
            year = int(year)
            filtered_books = [book for book in filtered_books if book['publication_year'] == year]
        except ValueError:
            return jsonify({"error": "Invalid year format. Must be an integer."}), 400

    return jsonify(filtered_books)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
