"""add user table

Revision ID: 2395705bb4d9
Revises: 63fbebc68b8b
Create Date: 2023-02-23 14:23:44.505773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2395705bb4d9'
down_revision = '63fbebc68b8b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer(),Nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    pass


def downgrade():
    op.drop_table('users')
    pass
