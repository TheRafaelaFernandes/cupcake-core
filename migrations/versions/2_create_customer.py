"""create_customer

Revision ID: 2
Revises: 
Create Date: 2024-11-27 01:17:25.458373

"""
from alembic import op
from sqlalchemy import Integer, String, column, table, Boolean

revision = '2'
down_revision = '1'
branch_labels = None
depends_on = None


def upgrade():
    customer_table = table(
        'customer',
        column('id', Integer),
        column('username', String),
        column('name', String),
        column('password', String),
        column('email', String),
        column('superuser', Boolean)
    )

    op.bulk_insert(customer_table, [
        {
            'id': 1,
            'username': 'admin',
            'name': 'Administrator',
            'password': '123456',
            'email': 'admin@example.com',
            'superuser': True
        }
    ])

def downgrade():
    pass
