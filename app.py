from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from api import api

import os
import sqlite3


# =========================================================
# APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# SECRET KEY
# =========================================================

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)


# =========================================================
# REGISTER API
# =========================================================

app.register_blueprint(api)


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE = os.path.join(
    DATABASE_DIR,
    "admin.db"
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    db = sqlite3.connect(
        DATABASE
    )

    db.row_factory = sqlite3.Row

    return db


# =========================================================
# ADMIN TABLE
# =========================================================

def init_admin_table():

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS admins (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    db.commit()


    # -----------------------------------------------------
    # CREATE DEFAULT ADMIN IF NONE EXISTS
    # -----------------------------------------------------

    admin = db.execute(
        """
        SELECT id
        FROM admins
        WHERE username = ?
        """,
        ("admin",)
    ).fetchone()


    if not admin:

        password = os.environ.get(
            "ADMIN_PASSWORD",
            "11111111"
        )

        password_hash = generate_password_hash(
            password
        )

        db.execute(
            """
            INSERT INTO admins
            (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (
                "admin",
                password_hash
            )
        )

        db.commit()


    db.close()


# =========================================================
# INITIALIZE MODELS
# =========================================================

from models.news import (
    init_news_table,
    get_all_news,
    add_news,
    update_news,
    delete_news,
    count_news
)

from models.service import (
    init_service_table,
    get_all_services,
    add_service,
    update_service,
    delete_service,
    count_services,
    count_active_services
)

from models.enquiries import (
    init_enquiry_table,
    get_all_enquiries,
    mark_enquiry_read,
    delete_enquiry,
    count_enquiries,
    count_unread_enquiries
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    init_admin_table()

    init_news_table(
        get_db
    )

    init_service_table(
        get_db
    )

    init_enquiry_table(
        get_db
    )


initialize_database()


# =========================================================
# LOGIN CHECK
# =========================================================

def login_required():

    return "admin_id" in session


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def login():

    if login_required():

        return redirect(
            url_for("dashboard")
        )


    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        db = get_db()

        admin = db.execute(
            """
            SELECT *
            FROM admins
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        db.close()


        if admin and check_password_hash(
            admin["password"],
            password
        ):

            session.clear()

            session["admin_id"] = admin["id"]

            session["username"] = admin["username"]

            return redirect(
                url_for("dashboard")
            )


        flash(
            "Invalid username or password.",
            "error"
        )


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not login_required():

        return redirect(
            url_for("login")
        )


    statistics = {

        "news":
            count_news(get_db),

        "services":
            count_services(get_db),

        "active_services":
            count_active_services(get_db),

        "enquiries":
            count_enquiries(get_db),

        "unread_enquiries":
            count_unread_enquiries(get_db)

    }


    return render_template(
        "dashboard.html",
        statistics=statistics
    )


# =========================================================
# NEWS
# =========================================================

@app.route("/news")
def news():

    if not login_required():

        return redirect(
            url_for("login")
        )


    news_items = get_all_news(
        get_db
    )


    return render_template(
        "news.html",
        news=news_items
    )


# =========================================================
# ADD NEWS
# =========================================================

@app.route(
    "/news/add",
    methods=["POST"]
)
def add_news_route():

    if not login_required():

        return redirect(
            url_for("login")
        )


    title = request.form.get(
        "title",
        ""
    ).strip()


    content = request.form.get(
        "content",
        ""
    ).strip()


    status = request.form.get(
        "status",
        "Published"
    ).strip()


    if not title or not content:

        flash(
            "Title and content are required.",
            "error"
        )

        return redirect(
            url_for("news")
        )


    add_news(
        get_db,
        title,
        content,
        status
    )


    flash(
        "News article added successfully.",
        "success"
    )


    return redirect(
        url_for("news")
    )


# =========================================================
# EDIT NEWS
# =========================================================

@app.route(
    "/news/edit/<int:news_id>",
    methods=["POST"]
)
def edit_news_route(news_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    title = request.form.get(
        "title",
        ""
    ).strip()


    content = request.form.get(
        "content",
        ""
    ).strip()


    status = request.form.get(
        "status",
        "Published"
    ).strip()


    if not title or not content:

        flash(
            "Title and content are required.",
            "error"
        )

        return redirect(
            url_for("news")
        )


    update_news(
        get_db,
        news_id,
        title,
        content,
        status
    )


    flash(
        "News article updated.",
        "success"
    )


    return redirect(
        url_for("news")
    )


# =========================================================
# DELETE NEWS
# =========================================================

@app.route(
    "/news/delete/<int:news_id>",
    methods=["POST"]
)
def delete_news_route(news_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    delete_news(
        get_db,
        news_id
    )


    flash(
        "News article deleted.",
        "success"
    )


    return redirect(
        url_for("news")
    )


# =========================================================
# SERVICES
# =========================================================

@app.route("/services")
def services():

    if not login_required():

        return redirect(
            url_for("login")
        )


    services_list = get_all_services(
        get_db
    )


    return render_template(
        "services.html",
        services=services_list
    )


# =========================================================
# ADD SERVICE
# =========================================================

@app.route(
    "/services/add",
    methods=["POST"]
)
def add_service_route():

    if not login_required():

        return redirect(
            url_for("login")
        )


    title = request.form.get(
        "title",
        ""
    ).strip()


    description = request.form.get(
        "description",
        ""
    ).strip()


    status = request.form.get(
        "status",
        "Active"
    ).strip()


    if not title or not description:

        flash(
            "Service name and description are required.",
            "error"
        )

        return redirect(
            url_for("services")
        )


    add_service(
        get_db,
        title,
        description,
        status
    )


    flash(
        "Service added successfully.",
        "success"
    )


    return redirect(
        url_for("services")
    )


# =========================================================
# EDIT SERVICE
# =========================================================

@app.route(
    "/services/edit/<int:service_id>",
    methods=["POST"]
)
def edit_service_route(service_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    title = request.form.get(
        "title",
        ""
    ).strip()


    description = request.form.get(
        "description",
        ""
    ).strip()


    status = request.form.get(
        "status",
        "Active"
    ).strip()


    if not title or not description:

        flash(
            "Service name and description are required.",
            "error"
        )

        return redirect(
            url_for("services")
        )


    update_service(
        get_db,
        service_id,
        title,
        description,
        status
    )


    flash(
        "Service updated successfully.",
        "success"
    )


    return redirect(
        url_for("services")
    )


# =========================================================
# DELETE SERVICE
# =========================================================

@app.route(
    "/services/delete/<int:service_id>",
    methods=["POST"]
)
def delete_service_route(service_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    delete_service(
        get_db,
        service_id
    )


    flash(
        "Service deleted.",
        "success"
    )


    return redirect(
        url_for("services")
    )


# =========================================================
# ENQUIRIES
# =========================================================

@app.route("/enquiries")
def enquiries():

    if not login_required():

        return redirect(
            url_for("login")
        )


    enquiries_list = get_all_enquiries(
        get_db
    )


    return render_template(
        "enquiries.html",
        enquiries=enquiries_list
    )


# =========================================================
# MARK ENQUIRY AS READ
# =========================================================

@app.route(
    "/enquiries/read/<int:enquiry_id>",
    methods=["POST"]
)
def read_enquiry(enquiry_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    mark_enquiry_read(
        get_db,
        enquiry_id
    )


    flash(
        "Enquiry marked as read.",
        "success"
    )


    return redirect(
        url_for("enquiries")
    )


# =========================================================
# DELETE ENQUIRY
# =========================================================

@app.route(
    "/enquiries/delete/<int:enquiry_id>",
    methods=["POST"]
)
def delete_enquiry_route(enquiry_id):

    if not login_required():

        return redirect(
            url_for("login")
        )


    delete_enquiry(
        get_db,
        enquiry_id
    )


    flash(
        "Enquiry deleted.",
        "success"
    )


    return redirect(
        url_for("enquiries")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5001
        )
    )


    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )