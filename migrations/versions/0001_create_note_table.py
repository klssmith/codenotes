"""empty message

Revision ID: 0001_create_note_table
Revises:
Create Date: 2018-02-23 16:34:29.819578

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_note_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('note',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_note_title'), 'note', ['title'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_note_title'), table_name='note')
    op.drop_table('note')
