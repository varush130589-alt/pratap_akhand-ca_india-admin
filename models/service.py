def init_service_table(get_db):

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS services (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'Active',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)

    db.commit()

    db.close()


def get_all_services(
    get_db,
    active_only=False
):

    db = get_db()

    if active_only:

        rows = db.execute("""
            SELECT *
            FROM services
            WHERE status = 'Active'
            ORDER BY id DESC
        """).fetchall()

    else:

        rows = db.execute("""
            SELECT *
            FROM services
            ORDER BY id DESC
        """).fetchall()

    db.close()

    return rows


def get_service(
    get_db,
    service_id
):

    db = get_db()

    row = db.execute(
        """
        SELECT *
        FROM services
        WHERE id = ?
        """,
        (service_id,)
    ).fetchone()

    db.close()

    return row


def add_service(
    get_db,
    title,
    description,
    status
):

    db = get_db()

    db.execute(
        """
        INSERT INTO services
        (
            title,
            description,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            description,
            status
        )
    )

    db.commit()

    db.close()


def update_service(
    get_db,
    service_id,
    title,
    description,
    status
):

    db = get_db()

    db.execute(
        """
        UPDATE services

        SET
            title = ?,
            description = ?,
            status = ?

        WHERE id = ?
        """,
        (
            title,
            description,
            status,
            service_id
        )
    )

    db.commit()

    db.close()


def delete_service(
    get_db,
    service_id
):

    db = get_db()

    db.execute(
        """
        DELETE FROM services
        WHERE id = ?
        """,
        (service_id,)
    )

    db.commit()

    db.close()


def count_services(get_db):

    db = get_db()

    count = db.execute(
        "SELECT COUNT(*) FROM services"
    ).fetchone()[0]

    db.close()

    return count


def count_active_services(get_db):

    db = get_db()

    count = db.execute(
        """
        SELECT COUNT(*)
        FROM services
        WHERE status = 'Active'
        """
    ).fetchone()[0]

    db.close()

    return count