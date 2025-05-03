"""add is_active column with default

Revision ID: 4a99a69b285f
Revises: 0d6dada0e1dd
Create Date: 2025-05-03 17:15:11.061478
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a99a69b285f'
down_revision = '0d6dada0e1dd'
branch_labels = None
depends_on = None


def upgrade():
    # Passo 1: adicionar como nullable (temporariamente)
    with op.batch_alter_table('cupcake') as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # Passo 2: preencher todos os existentes como True
    op.execute("UPDATE cupcake SET is_active = TRUE")

    # Passo 3: tornar NOT NULL
    with op.batch_alter_table('cupcake') as batch_op:
        batch_op.alter_column('is_active', nullable=False)


def downgrade():
    with op.batch_alter_table('cupcake') as batch_op:
        batch_op.drop_column('is_active')
