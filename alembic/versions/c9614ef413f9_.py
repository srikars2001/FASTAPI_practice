"""add foreign key to posts table

Revision ID: c9614ef413f9
Revises: c968337c9a24
Create Date: 2022-12-27 01:02:24.597306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9614ef413f9'
down_revision = 'c968337c9a24'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",
                            local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column(table_name="posts",column_name="owner_id")
