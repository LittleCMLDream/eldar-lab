"""add lab_schedules table"""
from alembic import op
import sqlalchemy as sa
revision = "003"
down_revision = "002"

def upgrade():
    op.create_table("lab_schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("semester_id", sa.BigInteger(), nullable=False),
        sa.Column("course_name", sa.String(100), nullable=False),
        sa.Column("teacher_id", sa.BigInteger()),
        sa.Column("class_names", sa.String(500)),
        sa.Column("week_start", sa.Integer()),
        sa.Column("week_end", sa.Integer()),
        sa.Column("week_type", sa.String(10)),
        sa.Column("day_of_week", sa.SmallInteger()),
        sa.Column("period_start", sa.SmallInteger()),
        sa.Column("period_end", sa.SmallInteger()),
    )
    op.create_index("ix_schedules_semester", "lab_schedules", ["semester_id"])
    op.create_index("ix_schedules_teacher", "lab_schedules", ["teacher_id"])

def downgrade():
    op.drop_table("lab_schedules")
