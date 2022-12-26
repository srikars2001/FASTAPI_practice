"""add last few columns to post table

Revision ID: 767ee6d8172c
Revises: c9614ef413f9
Create Date: 2022-12-27 01:20:01.100587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '767ee6d8172c'
down_revision = 'c9614ef413f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                    sa.Column("published",sa.Boolean,nullable=False,server_default="TRUE")
                    )

    op.add_column("posts",sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")
    ))
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
