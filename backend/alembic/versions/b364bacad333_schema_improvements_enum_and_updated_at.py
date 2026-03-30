"""schema_improvements_enum_and_updated_at

Revision ID: b364bacad333
Revises: b5e1f320787b
Create Date: 2026-03-30 19:38:30.713970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b364bacad333'
down_revision: Union[str, None] = 'b5e1f320787b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
 
    # ── 1. booking_status ENUM type ───────────────────────────────────────────
    # Create the PostgreSQL enum type first
    booking_status = sa.Enum(
        'pending', 'confirmed', 'cancelled',
        name='booking_status'
    )
    booking_status.create(op.get_bind(), checkfirst=True)
 
    # Migrate existing status column to use the enum
    # Step 1: add a temp column
    op.add_column('bookings', sa.Column('status_new', sa.Enum(
        'pending', 'confirmed', 'cancelled', name='booking_status'
    ), nullable=True))
 
    # Step 2: copy data
    op.execute("UPDATE bookings SET status_new = status::booking_status")
 
    # Step 3: drop old, rename new
    op.drop_column('bookings', 'status')
    op.alter_column('bookings', 'status_new', new_column_name='status',
                    nullable=False, server_default='pending')
 
    # ── 2. bookings.restaurant_id — enforce NOT NULL ──────────────────────────
    # First clean up any orphaned rows (should be 0 if data is consistent)
    op.execute("DELETE FROM bookings WHERE restaurant_id IS NULL")
    op.alter_column('bookings', 'restaurant_id', nullable=False)
 
    # Change ondelete from CASCADE to RESTRICT (don't silently delete bookings)
    op.drop_constraint('bookings_restaurant_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_restaurant_id_fkey',
        'bookings', 'restaurants',
        ['restaurant_id'], ['id'],
        ondelete='RESTRICT'
    )
 
    # ── 3. updated_at on users ────────────────────────────────────────────────
    op.add_column('users', sa.Column(
        'updated_at', sa.DateTime(),
        server_default=sa.text('now()'),
        nullable=True
    ))
 
    # ── 4. updated_at on restaurants ─────────────────────────────────────────
    op.add_column('restaurants', sa.Column(
        'updated_at', sa.DateTime(),
        server_default=sa.text('now()'),
        nullable=True
    ))
 
    # ── 5. Performance indexes ────────────────────────────────────────────────
    # Booking lookups by status (dashboard filter)
    op.create_index('ix_bookings_status', 'bookings', ['status'])
 
    # Booking lookups by date (availability check — most frequent query)
    op.create_index('ix_bookings_date', 'bookings', ['booking_date'])
 
    # Composite: restaurant + date (used in capacity check query)
    op.create_index(
        'ix_bookings_restaurant_date',
        'bookings',
        ['restaurant_id', 'booking_date']
    )
 
    # User bookings ordered by created_at (dashboard list)
    op.create_index(
        'ix_bookings_user_created',
        'bookings',
        ['user_id', 'created_at']
    )
 
    # Restaurant cuisine filter (for AI recommendation phase)
    op.create_index('ix_restaurants_cuisine', 'restaurants', ['cuisine_type'])
 
    # ── 6. users.role — add CHECK constraint ──────────────────────────────────
    op.create_check_constraint(
        'check_user_role',
        'users',
        "role IN ('customer', 'admin')"
    )
 
    # ── 7. restaurants.max_capacity default — ensure column has server default ─
    op.alter_column('restaurants', 'max_capacity',
                    server_default='50',
                    existing_type=sa.Integer(),
                    existing_nullable=True)
 
 
def downgrade() -> None:
    op.drop_constraint('check_user_role', 'users', type_='check')
    op.drop_index('ix_restaurants_cuisine', table_name='restaurants')
    op.drop_index('ix_bookings_user_created', table_name='bookings')
    op.drop_index('ix_bookings_restaurant_date', table_name='bookings')
    op.drop_index('ix_bookings_date', table_name='bookings')
    op.drop_index('ix_bookings_status', table_name='bookings')
    op.drop_column('restaurants', 'updated_at')
    op.drop_column('users', 'updated_at')
 
    # Revert restaurant_id FK to CASCADE + nullable
    op.drop_constraint('bookings_restaurant_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_restaurant_id_fkey',
        'bookings', 'restaurants',
        ['restaurant_id'], ['id'],
        ondelete='CASCADE'
    )
    op.alter_column('bookings', 'restaurant_id', nullable=True)
 
    # Revert status column back to VARCHAR
    op.add_column('bookings', sa.Column('status_old', sa.String(20), nullable=True))
    op.execute("UPDATE bookings SET status_old = status::text")
    op.drop_column('bookings', 'status')
    op.alter_column('bookings', 'status_old', new_column_name='status',
                    nullable=True, server_default='pending')
 
    sa.Enum(name='booking_status').drop(op.get_bind(), checkfirst=True)
