from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

BOOK_API_URL = os.getenv("BOOK_API_URL", "sse-lab10-book.etd2czg2ayavd8eq.uksouth.azurecontainer.io")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Search</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            display: inline-block;
            margin-top: 20px;
        }
        label {
            font-weight: bold;
            margin-right: 10px;
        }
        input {
            padding: 8px;
            margin: 10px 0;
            width: 80%;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 15px;
            margin-top: 10px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .results {
            margin-top: 20px;
            text-align: left;
            display: inline-block;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>Book Search</h1>
    <form action="/search" method="get">
        <label for="title">Title:</label>
        <input type="text" name="title" id="title"><br>

        <label for="author">Author:</label>
        <input type="text" name="author" id="author"><br>

        <label for="genre">Genre:</label>
        <input type="text" name="genre" id="genre"><br>

        <label for="year">Publication Year:</label>
        <input type="text" name="year" id="year"><br>

        <button type="submit">Search</button>
    </form>

    {% if books is not none %}
    <div class="results">
        <h2>Search Results</h2>
        {% if books|length == 0 %}
            <p>No results found</p>
        {% else %}
            <ul>
                {% for book in books %}
                    <li><strong>{{ book['title'] }}</strong> - {{ book['author'] }} ({{ book['publication_year'] }}) - {{ book['genre'] }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, books=None)

@app.route('/search', methods=['GET'])
def search_books():
    params = {
        'title': request.args.get('title', '').strip(),
        'author': request.args.get('author', '').strip(),
        'genre': request.args.get('genre', '').strip(),
        'year': request.args.get('year', '').strip()
    }

    filtered_params = {key: value for key, value in params.items() if value}

    if not filtered_params:
        return render_template_string(HTML_TEMPLATE, books=[])

    response = requests.get(BOOK_API_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch books from API"}), 500

    books = response.json()

    return render_template_string(HTML_TEMPLATE, books=books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
