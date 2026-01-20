"""fix doctor id autoincrement

Revision ID: 55119c701c86
Revises: 201d96814116
Create Date: 2026-01-20 14:40:06.539315
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = '55119c701c86'
down_revision: Union[str, Sequence[str], None] = '201d96814116'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("doctors", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=sa.Integer(),
            autoincrement=True,
            nullable=False
        )
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), nullable=True)
        )
        # ✅ constraint бо ном
        batch_op.create_foreign_key(
            "fk_doctors_user_id",  # номи constraint
            "users",               # таблицаи parent
            ["user_id"],           # майдон дар doctors
            ["id"]                 # майдон дар users
        )


def downgrade():
    with op.batch_alter_table("doctors", schema=None) as batch_op:
        batch_op.drop_constraint("fk_doctors_user_id", type_="foreignkey")
        batch_op.drop_column("user_id")
        batch_op.alter_column(
            "id",
            existing_type=sa.Integer(),
            autoincrement=False,
            nullable=False
        )
