"""create alchmey post table

Revision ID: 8c8d821f784a
Revises: 
Create Date: 2023-02-22 11:15:32.839786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c8d821f784a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('alchmey_posts',sa.Column('id',sa.INTEGER(), nullable=False,primary_key = True),
                    sa.Column('title',sa.String(),nullable = False))
    pass



def downgrade() -> None:
    op.drop_table('alchmey_posts')
    pass
