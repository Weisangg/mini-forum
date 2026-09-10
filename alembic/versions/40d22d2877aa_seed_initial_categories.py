"""seed initial categories

Revision ID: 40d22d2877aa
Revises: 3f39a93fbac1
Create Date: 2026-09-09 23:12:29.749659

"""
from datetime import datetime, timezone
from typing import Sequence, Union
from sqlalchemy import column, table

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40d22d2877aa'
down_revision: Union[str, Sequence[str], None] = '3f39a93fbac1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

categories_table = table(
    "categories",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
    sa.column("descrition", sa.String),
    sa.column("created_at", sa.DateTime(timezone=True))
)

def upgrade() -> None:
    op.bulk_insert
    ("""
        INSERT INTO categories (name, description, created_at) VALUES
        ('Python', 'Обсуждение языка Python, библиотек и экосистемы.', NOW()),
        ('FastAPI', 'Вопросы по асинхронной веб-разработке и FastAPI.', NOW()),
        ('Linux', 'Администрирование, Arch Linux, bash и системный софт.', NOW()),
        ('Frontend', 'HTML, CSS, JavaScript, интерфейсы и клиенты.', NOW()),
        ('Other', 'Темы и вопросы, не вошедшие в другие категории.', NOW());
    """)


def downgrade() -> None:
    op.execute("DELETE FROM categories")
