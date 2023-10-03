"""Initial migrate

Revision ID: a984c1bb6e9e
Revises: 
Create Date: 2023-10-03 00:21:24.289784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a984c1bb6e9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('web_identifier', sa.CHAR(length=36), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('onboarding', sa.Enum('ONBOARDING_STEP_ONE', 'ONBOARDING_STEP_TWO', name='typeonboarding'), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('web_identifier')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_web_identifier'), ['web_identifier'], unique=True)

    op.create_table('users_historical_stock_price',
    sa.Column('uuid', sa.CHAR(length=36), nullable=False),
    sa.Column('web_identifier_uuid', sa.CHAR(length=36), nullable=False),
    sa.Column('symbol_stock', sa.String(length=20), nullable=False),
    sa.Column('open_price', sa.Float(precision=4, asdecimal=3), nullable=True),
    sa.Column('high_price', sa.Float(precision=4, asdecimal=3), nullable=True),
    sa.Column('low_price', sa.Float(precision=4, asdecimal=3), nullable=True),
    sa.Column('close_price', sa.Float(precision=4, asdecimal=3), nullable=True),
    sa.Column('date_stock', sa.Date(), nullable=False),
    sa.Column('time_stock', sa.Time(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['web_identifier_uuid'], ['users.web_identifier'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    with op.batch_alter_table('users_historical_stock_price', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_historical_stock_price_symbol_stock'), ['symbol_stock'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_historical_stock_price_uuid'), ['uuid'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_historical_stock_price_web_identifier_uuid'), ['web_identifier_uuid'], unique=False)
        batch_op.create_index('ix_web_identifier_symbol', ['web_identifier_uuid', 'symbol_stock'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_historical_stock_price', schema=None) as batch_op:
        batch_op.drop_index('ix_web_identifier_symbol')
        batch_op.drop_index(batch_op.f('ix_users_historical_stock_price_web_identifier_uuid'))
        batch_op.drop_index(batch_op.f('ix_users_historical_stock_price_uuid'))
        batch_op.drop_index(batch_op.f('ix_users_historical_stock_price_symbol_stock'))

    op.drop_table('users_historical_stock_price')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_web_identifier'))

    op.drop_table('users')
    # ### end Alembic commands ###