"""add user table

Revision ID: c968337c9a24
Revises: 9b8af143fd33
Create Date: 2022-12-27 00:55:26.785146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c968337c9a24'
down_revision = '9b8af143fd33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("email",sa.String(),nullable=False),
                    sa.Column("password",sa.String(),nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
