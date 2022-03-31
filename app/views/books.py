from flask import jsonify, request, Blueprint

from app.models import BookModel

book_bp = Blueprint('books', __name__)


@book_bp.route("/books", methods=["GET"])  # get all books
def get_books():
    author_id = request.args.get("author_id")
    offset = request.args.get("offset", 0)
    limit = request.args.get("limit", 10)

    # a simple filter by last_name QUERY param
    if author_id:
        books = BookModel.find_by_author_id(author_id, offset, limit)
    else:
        books = BookModel.return_all(offset, limit)
    return jsonify(books)


@book_bp.route("/books/<int:book_id>", methods=["GET"])  # get a book by its id
def get_book(book_id):
    book = BookModel.find_by_id(book_id)
    if not book:
        return jsonify({"message": "Book not found."}), 404

    return jsonify(book)


@book_bp.route("/books", methods=["POST"])  # create a new book
def create_book():
    if not request.json:  # a post request mustn't be empty
        return jsonify({"message": "Please fill in all information about the book!"}), 400
    title, genre, author_id = request.json.get("title"), request.json.get("genre"), request.json.get("author_id")
    if not title or not genre or not author_id:  # to add a book you need to set all values
        return jsonify({"message": "Please fill in all information about the book!"}), 400
    book = BookModel(title=title, genre=genre, author_id=author_id)
    book.save_to_db()
    return jsonify({"message": f"The book with id {book.id} was created!"})


@book_bp.route("/books/<int:book_id>", methods=["PATCH"])
def update_book(book_id):
    book = BookModel.find_by_id(book_id, to_dict=False)
    if not book:
        return jsonify({"message": "Book not found."}), 404
    if not request.json:  # a patch request mustn't be empty
        return jsonify({"message": "Please fill in all information about the book!"}), 400
    title, genre, author_id = request.json.get("title"), request.json.get("genre"), request.json.get("author_id")

    if title:
        book.title = title
    if genre:
        book.genre = genre
    if author_id:
        book.author_id = author_id
    book.save_to_db()
    return jsonify({"message": "The book was updated"})


@book_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    response_code = BookModel.delete_by_id(book_id)
    if response_code == 404:
        return jsonify({"message": "Book not found."}), 404

    return jsonify({"message": "The book was deleted!"})


