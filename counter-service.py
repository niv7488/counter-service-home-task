from flask import Flask, request, jsonify, Response
from flask_rbac import RBAC

# Initialize Flask app and RBAC
app = Flask(__name__)
rbac = RBAC()
rbac.init_app(app)

# Roles and permissions
roles = {
    'admin': ['increment', 'read'],
    'user': ['read']
}

# User data (replace with a user management system)
users = {
    'username1': {'id': 1, 'roles': ['admin']},
    'username2': {'id': 2, 'roles': ['user']},
}

# Global counter variable
counter = 0


@app.before_request
def before_request():
    """Assigns user roles to Flask-RBAC based on authentication."""
    user = auth.current_user()  # Assuming you have authentication implemented
    if user:
        user_roles = [role for user in users if user['id'] == user['id'] for role in user['roles']]
        rbac.init_identity(user_roles)  # Assign roles to RBAC identity


@rbac.can
def has_role(role):
    """Checks if the current user has the specified role.

    Args:
        role: The role to check for.

    Returns:
        True if the user has the role, False otherwise.
    """
    return any(role in user_roles for user_roles in rbac.current_user)


@app.route("/", methods=["GET", "POST"])
@rbac.require('read')  # Require 'read' permission for all requests
def handle_requests():
    """Handles authenticated GET and POST requests to the counter service.

    - Increments the counter on authorized POST requests (handles potential data issues).
    - Returns the current counter value in JSON format on authorized GET requests.

    Returns:
        JSON response containing the current counter value or error message.
    """

    if request.method == "POST":
        if has_role('increment'):
            try:
                # Attempt to convert request data (if any) to an integer
                data = request.get_json()
                if data:
                    counter += int(data.get("increment", 1))  # Allow optional increment value
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid increment value (must be an integer)."}), 400
            else:
                return jsonify({"message": "Counter incremented successfully."}), 201
        else:
            return jsonify({"error": "Unauthorized to increment counter."}), 403
    else:
        return jsonify({"counter": counter}), 200


@app.errorhandler(Exception)
def handle_exceptions(error):
    """Handles unexpected exceptions during request processing.

    Returns:
        JSON response with generic error message.
    """
    return jsonify({"error": "An internal error occurred."}), 500


# Run the Flask app on port 80
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
