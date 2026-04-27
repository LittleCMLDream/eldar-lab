"""add EXCLUDE constraint for conflict detection"""
from alembic import op
revision = "002"
down_revision = "001"

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute("""
        ALTER TABLE lab_booking_slots
        ADD CONSTRAINT no_overlapping_lab_slots
        EXCLUDE USING gist (
            lab_id WITH =,
            week_number WITH =,
            day_of_week WITH =,
            int4range(period_start, period_end, '[]') WITH &&
        )
    """)

def downgrade():
    op.execute("ALTER TABLE lab_booking_slots DROP CONSTRAINT IF EXISTS no_overlapping_lab_slots")
    op.execute("DROP EXTENSION IF EXISTS btree_gist")
