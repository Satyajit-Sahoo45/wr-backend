"""Initial migration

Revision ID: 0916072b3ece
Revises: 
Create Date: 2024-07-27 14:17:07.132275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0916072b3ece'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('retreat',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('condition', sa.String(length=255), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.Text(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('booking',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(length=255), nullable=True),
    sa.Column('user_email', sa.String(length=255), nullable=True),
    sa.Column('user_phone', sa.String(length=255), nullable=True),
    sa.Column('retreat_id', sa.String(), nullable=True),
    sa.Column('retreat_title', sa.String(length=255), nullable=True),
    sa.Column('retreat_location', sa.String(length=255), nullable=True),
    sa.Column('retreat_price', sa.Numeric(), nullable=True),
    sa.Column('retreat_duration', sa.String(length=255), nullable=True),
    sa.Column('payment_details', sa.Text(), nullable=True),
    sa.Column('booking_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['retreat_id'], ['retreat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_table('user')
    op.drop_table('retreat')
    # ### end Alembic commands ###
