# =========================================================
# INITIALIZE ENQUIRY TABLE
# =========================================================

def init_enquiry_table(get_db):

    db = get_db()

    # -----------------------------------------------------
    # CREATE TABLE IF IT DOES NOT EXIST
    # -----------------------------------------------------

    db.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL,

            phone TEXT,

            service TEXT,

            message TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'Unread',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # -----------------------------------------------------
    # DATABASE MIGRATION
    # -----------------------------------------------------
    # Older database versions did not have the service
    # column.
    #
    # Check whether the column already exists.
    # -----------------------------------------------------

    columns = db.execute(
        "PRAGMA table_info(enquiries)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    if "service" not in column_names:

        db.execute("""
            ALTER TABLE enquiries
            ADD COLUMN service TEXT
        """)

    db.commit()

    db.close()


# =========================================================
# ADD ENQUIRY
# =========================================================

def add_enquiry(
    get_db,
    name,
    email,
    phone,
    service,
    message
):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO enquiries
        (
            name,
            email,
            phone,
            service,
            message,
            status
        )
        VALUES (?, ?, ?, ?, ?, 'Unread')
        """,
        (
            name,
            email,
            phone,
            service,
            message
        )
    )

    enquiry_id = cursor.lastrowid

    db.commit()

    db.close()

    return enquiry_id


# =========================================================
# GET ALL ENQUIRIES
# =========================================================

def get_all_enquiries(get_db):

    db = get_db()

    rows = db.execute("""
        SELECT *
        FROM enquiries
        ORDER BY created_at DESC
    """).fetchall()

    db.close()

    return rows


# =========================================================
# MARK ENQUIRY AS READ
# =========================================================

def mark_enquiry_read(
    get_db,
    enquiry_id
):

    db = get_db()

    db.execute(
        """
        UPDATE enquiries

        SET status = 'Read'

        WHERE id = ?
        """,
        (enquiry_id,)
    )

    db.commit()

    db.close()


# =========================================================
# DELETE ENQUIRY
# =========================================================

def delete_enquiry(
    get_db,
    enquiry_id
):

    db = get_db()

    db.execute(
        """
        DELETE FROM enquiries

        WHERE id = ?
        """,
        (enquiry_id,)
    )

    db.commit()

    db.close()


# =========================================================
# COUNT ENQUIRIES
# =========================================================

def count_enquiries(get_db):

    db = get_db()

    count = db.execute(
        "SELECT COUNT(*) FROM enquiries"
    ).fetchone()[0]

    db.close()

    return count


# =========================================================
# COUNT UNREAD ENQUIRIES
# =========================================================

def count_unread_enquiries(get_db):

    db = get_db()

    count = db.execute(
        """
        SELECT COUNT(*)
        FROM enquiries
        WHERE status = 'Unread'
        """
    ).fetchone()[0]

    db.close()

    return count