"""create posts table

Revision ID: 6a532b48b3c4
Revises: 
Create Date: 2022-12-27 00:32:40.560193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a532b48b3c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                            sa.Column("title",sa.String(),nullable=False))
    



def downgrade() -> None:
    op.drop_table("posts")
