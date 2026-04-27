"""initial tables"""
from alembic import op
import sqlalchemy as sa
revision = "001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("TEACHER", "ADMIN", name="role"), default="TEACHER"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table("lab_rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("building", sa.String(20), nullable=False),
        sa.Column("room_number", sa.String(20), nullable=False),
        sa.Column("pc_count", sa.Integer()),
        sa.Column("capacity", sa.Integer()),
        sa.Column("status", sa.SmallInteger(), default=1),
    )
    op.create_index("ix_lab_rooms_building", "lab_rooms", ["building"])

    op.create_table("lab_booking_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("semester_id", sa.BigInteger(), nullable=False),
        sa.Column("request_no", sa.String(32), nullable=False),
        sa.Column("teacher_id", sa.BigInteger(), sa.ForeignKey("users.id")),
        sa.Column("reason", sa.String(20)),
        sa.Column("course_name", sa.String(100)),
        sa.Column("class_names", sa.String(500)),
        sa.Column("student_count", sa.Integer()),
        sa.Column("content", sa.Text()),
        sa.Column("status", sa.String(20), default="pending"),
        sa.Column("approver_id", sa.BigInteger()),
        sa.Column("approved_at", sa.DateTime()),
    )
    op.create_unique_constraint("uq_request_no", "lab_booking_requests", ["request_no"])

    op.create_table("lab_booking_slots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("lab_id", sa.BigInteger(), nullable=False),
        sa.Column("week_number", sa.SmallInteger(), nullable=False),
        sa.Column("day_of_week", sa.SmallInteger(), nullable=False),
        sa.Column("period_start", sa.SmallInteger(), nullable=False),
        sa.Column("period_end", sa.SmallInteger(), nullable=False),
        sa.Column("request_id", sa.BigInteger(), sa.ForeignKey("lab_booking_requests.id"), nullable=False),
    )
    op.create_index("ix_slots_lab", "lab_booking_slots", ["lab_id"])

def downgrade():
    op.drop_table("lab_booking_slots")
    op.drop_table("lab_booking_requests")
    op.drop_table("lab_rooms")
    op.drop_table("users")
