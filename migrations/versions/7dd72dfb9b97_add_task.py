"""add task

Revision ID: 7dd72dfb9b97
Revises: d2f739927b3f
Create Date: 2019-03-20 13:35:05.181683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dd72dfb9b97'
down_revision = 'd2f739927b3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_name'), 'task', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_name'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
