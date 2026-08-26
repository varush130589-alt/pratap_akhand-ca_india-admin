from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import requests


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)

# Used for Flask flash messages
app.secret_key = "ca-india-website-secret-key"


# ============================================================
# ADMIN API
# ============================================================

ADMIN_API_URL = (
    "https://pratap-akhand-ca-india-admin.onrender.com"
    "/api/enquiries"
)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ============================================================
# SERVICES
# ============================================================

@app.route("/services")
def services():

    return render_template(
        "services.html"
    )


# ============================================================
# INDIVIDUAL SERVICE PAGES
# ============================================================

@app.route("/services/income-tax")
def income_tax():

    return render_template(
        "income_tax.html"
    )


@app.route("/services/gst")
def gst():

    return render_template(
        "gst.html"
    )


@app.route("/services/accounting")
def accounting():

    return render_template(
        "accounting.html"
    )


@app.route("/services/audit")
def audit():

    return render_template(
        "audit.html"
    )


@app.route("/services/financial-advisory")
def financial_advisory():

    return render_template(
        "financial_advisory.html"
    )


# ============================================================
# CONTACT
# ============================================================

@app.route("/contact")
def contact():

    return render_template(
        "contact.html"
    )


# ============================================================
# ENQUIRY FORM
# ============================================================

@app.route(
    "/submit-enquiry",
    methods=["POST"]
)
def submit_enquiry():

    # --------------------------------------------------------
    # GET FORM DATA
    # --------------------------------------------------------

    name = request.form.get(
        "name",
        ""
    ).strip()


    email = request.form.get(
        "email",
        ""
    ).strip()


    phone = request.form.get(
        "phone",
        ""
    ).strip()


    service = request.form.get(
        "service",
        ""
    ).strip()


    message = request.form.get(
        "message",
        ""
    ).strip()


    # --------------------------------------------------------
    # VALIDATE FORM
    # --------------------------------------------------------

    if (
        not name
        or not email
        or not service
        or not message
    ):

        flash(
            "Please complete all required fields before submitting.",
            "error"
        )

        return redirect(
            request.referrer
            or url_for("home")
        )


    # --------------------------------------------------------
    # PREPARE DATA FOR ADMIN API
    # --------------------------------------------------------

    enquiry_data = {

        "name": name,

        "email": email,

        "phone": phone,

        "service": service,

        "message": message

    }


    # --------------------------------------------------------
    # SEND ENQUIRY TO ADMIN DASHBOARD
    # --------------------------------------------------------

    try:

        response = requests.post(

            ADMIN_API_URL,

            json=enquiry_data,

            timeout=15

        )


    except requests.exceptions.RequestException as error:

        print(
            "ADMIN API CONNECTION ERROR:",
            error
        )

        flash(
            "We could not submit your enquiry right now. "
            "Please try again later.",
            "error"
        )

        return redirect(
            request.referrer
            or url_for("contact")
        )


    # --------------------------------------------------------
    # CHECK ADMIN API RESPONSE
    # --------------------------------------------------------

    if response.status_code == 201:

        try:

            result = response.json()

        except ValueError:

            result = {}


        if result.get("success"):

            flash(
                "Thank you. Your enquiry has been received.",
                "success"
            )

            return redirect(
                request.referrer
                or url_for("contact")
            )


    # --------------------------------------------------------
    # API ERROR
    # --------------------------------------------------------

    print(
        "ADMIN API ERROR:",
        response.status_code,
        response.text
    )

    flash(
        "We could not submit your enquiry right now. "
        "Please try again later.",
        "error"
    )

    return redirect(
        request.referrer
        or url_for("contact")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )