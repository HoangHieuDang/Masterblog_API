from flask import Flask, jsonify, request
import logging
from flask_cors import CORS

# Configure logging to save logs to 'myapp.log'
logging.basicConfig(filename='myapp.log', level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample in-memory database (list of posts)
POSTS = [
    {"id": 1, "title": "C First post", "content": "This is the first post A."},
    {"id": 2, "title": "B Second post", "content": "This is the second post B."},
    {"id": 3, "title": "A Third post", "content": "This is the third post C."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Fetch all posts.
    Optional: sort the list according to
    sort and direction params in query string
    and return the sorted list"""

    sort_direction = False  # Default mode for sorting is Ascending
    sort_param = request.args.get("sort")
    direction_param = request.args.get("direction")
    # check direction param if it exists and set a value for boolean sort_direction
    if direction_param:
        if direction_param.lower() == "asc":
            sort_direction = False
        elif direction_param.lower() == "desc":
            sort_direction = True
        else:
            return jsonify({"Message": "invalid value for 'direction' parameter"}), 400
    # check sort param if it exists and execute sorting with given sort_direction
    if sort_param:
        if sort_param.lower() == "title":
            return jsonify(sorted(POSTS, key=lambda d: d['title'], reverse=sort_direction)), 200
        elif sort_param.lower() == "content":
            return jsonify(sorted(POSTS, key=lambda d: d['content'], reverse=sort_direction)), 200
        else:
            return jsonify({"Message": "invalid value for 'sort' parameter"}), 400

    return jsonify(POSTS)


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Search a post with a search term"""
    found_post = []
    for param, search_term in request.args.items():
        # search for search criteria "title"
        if param == "title":
            for post in POSTS:
                if str(search_term).lower() in post["title"].lower():
                    if post not in found_post:
                        found_post.append(post)
        # search for search criteria "content"
        elif param == "content":
            for post in POSTS:
                if str(search_term).lower() in post["content"].lower():
                    if post not in found_post:
                        found_post.append(post)
    return jsonify(found_post)


@app.route('/api/posts', methods=['POST'])
def add_new_post():
    """Add a new post.
    Expects JSON payload with 'title' and 'content'.
    """
    # Get JSON data from request
    data = request.get_json()
    new_title = ""
    new_content = ""

    # Check if data is not empty and extract 'title' and 'content'
    if data:
        for key, value in data.items():
            if key.lower() == 'title':
                new_title = value
            elif key.lower() == 'content':
                new_content = value

    # Validate title and content
    if new_title and new_content:
        new_id = max([post['id'] for post in POSTS]) + 1
        new_post = {"id": new_id, "title": new_title, "content": new_content}
        POSTS.append(new_post)
        found_new_post = False

        # Verify that the post was added successfully
        for post in POSTS:
            if post["id"] == new_id:
                return jsonify(post), 201

        if not found_new_post:
            return jsonify({"error": "Server error when adding new content"}), 500
    else:
        return jsonify({"error": "content and title should not be empty"}), 400


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """Update an existing post by ID.
    Expects JSON payload with 'title' and/or 'content'.
    """
    # Get JSON data from request
    data = request.get_json()
    new_title = ""
    new_content = ""

    # Extract 'title' and 'content' from request data
    if data:
        for key, value in data.items():
            if key.lower() == 'title':
                new_title = value
            elif key.lower() == 'content':
                new_content = value

    found_post = False
    for post in POSTS:
        if post['id'] == id:
            found_post = True
            if new_title:
                post['title'] = new_title
            if new_content:
                post['content'] = new_content
            return jsonify(post), 200

    if not found_post:
        return jsonify({"Message": "Post not found"}), 404


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Delete a post by ID."""
    found_post = False
    for post in POSTS:
        if post['id'] == id:
            POSTS.remove(post)
            msg_content = f"Post with id {id} has been deleted successfully."
            return jsonify({"message": msg_content}), 200

    if found_post == False:
        return jsonify({"message": "Post not found!"}), 404


if __name__ == '__main__':
    # Start the Flask server
    app.run(host="0.0.0.0", port=5002, debug=True)
