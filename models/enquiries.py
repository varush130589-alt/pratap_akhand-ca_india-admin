def init_enquiry_table(get_db):

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT NOT NULL,

            phone TEXT,

            message TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'Unread',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)

    db.commit()

    db.close()


def add_enquiry(
    get_db,
    name,
    email,
    phone,
    message
):

    db = get_db()

    db.execute(
        """
        INSERT INTO enquiries
        (
            name,
            email,
            phone,
            message,
            status
        )
        VALUES (?, ?, ?, ?, 'Unread')
        """,
        (
            name,
            email,
            phone,
            message
        )
    )

    db.commit()

    db.close()


def get_all_enquiries(get_db):

    db = get_db()

    rows = db.execute("""
        SELECT *
        FROM enquiries
        ORDER BY created_at DESC
    """).fetchall()

    db.close()

    return rows


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


def count_enquiries(get_db):

    db = get_db()

    count = db.execute(
        "SELECT COUNT(*) FROM enquiries"
    ).fetchone()[0]

    db.close()

    return count


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