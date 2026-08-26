def init_news_table(get_db):

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS news (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            content TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'Published',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)

    db.commit()

    db.close()


def get_all_news(
    get_db,
    published_only=False
):

    db = get_db()

    if published_only:

        rows = db.execute("""
            SELECT *
            FROM news
            WHERE status = 'Published'
            ORDER BY created_at DESC
        """).fetchall()

    else:

        rows = db.execute("""
            SELECT *
            FROM news
            ORDER BY created_at DESC
        """).fetchall()

    db.close()

    return rows


def get_news(
    get_db,
    news_id
):

    db = get_db()

    row = db.execute(
        """
        SELECT *
        FROM news
        WHERE id = ?
        """,
        (news_id,)
    ).fetchone()

    db.close()

    return row


def add_news(
    get_db,
    title,
    content,
    status
):

    db = get_db()

    db.execute(
        """
        INSERT INTO news
        (
            title,
            content,
            status
        )
        VALUES (?, ?, ?)
        """,
        (
            title,
            content,
            status
        )
    )

    db.commit()

    db.close()


def update_news(
    get_db,
    news_id,
    title,
    content,
    status
):

    db = get_db()

    db.execute(
        """
        UPDATE news

        SET
            title = ?,
            content = ?,
            status = ?

        WHERE id = ?
        """,
        (
            title,
            content,
            status,
            news_id
        )
    )

    db.commit()

    db.close()


def delete_news(
    get_db,
    news_id
):

    db = get_db()

    db.execute(
        """
        DELETE FROM news
        WHERE id = ?
        """,
        (news_id,)
    )

    db.commit()

    db.close()


def count_news(get_db):

    db = get_db()

    count = db.execute(
        "SELECT COUNT(*) FROM news"
    ).fetchone()[0]

    db.close()

    return count