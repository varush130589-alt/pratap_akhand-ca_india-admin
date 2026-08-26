from flask import Blueprint, request, jsonify


# =========================================================
# API BLUEPRINT
# =========================================================

api = Blueprint(
    "api",
    __name__
)


# =========================================================
# HEALTH CHECK
# =========================================================

@api.route(
    "/api/health",
    methods=["GET"]
)
def health_check():

    return jsonify({
        "success": True,
        "message": "CA India Admin API is running."
    }), 200


# =========================================================
# CREATE ENQUIRY
# =========================================================

@api.route(
    "/api/enquiries",
    methods=["POST"]
)
def create_enquiry():

    from app import get_db

    from models.enquiries import add_enquiry


    # -----------------------------------------------------
    # READ JSON
    # -----------------------------------------------------

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({
            "success": False,
            "message": "Invalid JSON request."
        }), 400


    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    name = str(
        data.get("name", "")
    ).strip()


    email = str(
        data.get("email", "")
    ).strip()


    phone = str(
        data.get("phone", "")
    ).strip()


    service = str(
        data.get("service", "")
    ).strip()


    message = str(
        data.get("message", "")
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name:

        return jsonify({
            "success": False,
            "message": "Name is required."
        }), 400


    if not email:

        return jsonify({
            "success": False,
            "message": "Email is required."
        }), 400


    if not service:

        return jsonify({
            "success": False,
            "message": "Service is required."
        }), 400


    if not message:

        return jsonify({
            "success": False,
            "message": "Message is required."
        }), 400


    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    try:

        enquiry_id = add_enquiry(
            get_db,
            name,
            email,
            phone,
            service,
            message
        )

    except Exception as error:

        print(
            "ENQUIRY API ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "message":
                "Unable to save enquiry."
        }), 500


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "message":
            "Enquiry received successfully.",

        "enquiry_id":
            enquiry_id

    }), 201