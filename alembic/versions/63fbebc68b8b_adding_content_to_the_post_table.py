""" adding content to the post table

Revision ID: 63fbebc68b8b
Revises: 8c8d821f784a
Create Date: 2023-02-22 12:07:27.946046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63fbebc68b8b'
down_revision = '8c8d821f784a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('alchmey_posts',sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('alchmey_posts','content')
    pass
