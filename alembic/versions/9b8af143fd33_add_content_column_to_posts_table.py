"""add content column to posts table

Revision ID: 9b8af143fd33
Revises: 6a532b48b3c4
Create Date: 2022-12-27 00:48:10.564569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b8af143fd33'
down_revision = '6a532b48b3c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
