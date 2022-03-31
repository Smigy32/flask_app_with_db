from flask import jsonify, request, Blueprint

from app.models import AuthorModel

author_bp = Blueprint('authors', __name__)


@author_bp.route("/authors", methods=["GET"])  # get all authors
def get_authors():
    last_name = request.args.get("last_name")
    offset = request.args.get("offset", 0)
    limit = request.args.get("limit", 10)
    authors = AuthorModel.return_all(offset, limit)

    # a simple filter by last_name QUERY param
    if last_name:
        last_name = last_name.capitalize()
        author = AuthorModel.find_by_last_name(last_name)
        return jsonify(author)

    return jsonify(authors)


@author_bp.route("/authors/<int:author_id>", methods=["GET"])  # get an author by his id
def get_author(author_id):
    author = AuthorModel.find_by_id(author_id)
    if not author:
        return jsonify({"message": "Author not found."}), 404

    return jsonify(author)


@author_bp.route("/authors", methods=["POST"])  # create a new author
def create_author():
    if not request.json:  # a post request mustn't be empty
        return jsonify({"message": "Please fill in all information about the author!"}), 400
    first_name, last_name = request.json.get("first_name"), request.json.get("last_name")
    if not first_name or not last_name:  # to add an author you need to set all values
        return jsonify({"message": "Please fill in all information about the author!"}), 400
    author = AuthorModel(first_name=first_name, last_name=last_name)
    author.save_to_db()
    return jsonify({"message": f"The author with id {author.id} was created!"})


@author_bp.route("/authors/<int:author_id>", methods=["PATCH"])
def update_author(author_id):
    author = AuthorModel.find_by_id(author_id, to_dict=False)
    if not author:
        return jsonify({"message": "Author not found."}), 404
    if not request.json:  # a patch request mustn't be empty
        return jsonify({"message": "Please fill in all information about the author!"}), 400
    first_name, last_name = request.json.get("first_name"), request.json.get("last_name")

    if first_name:
        author.first_name = first_name
    if last_name:
        author.last_name = last_name
    author.save_to_db()
    return jsonify({"message": "The author was updated"})


@author_bp.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    response_code = AuthorModel.delete_by_id(author_id)
    if response_code == 404:
        return jsonify({"message": "Author not found."}), 404

    return jsonify({"message": "The author was deleted!"})


