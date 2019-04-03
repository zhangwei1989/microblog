"""add role and permission

Revision ID: 8656f79d7a02
Revises: a56900e65050
Create Date: 2019-04-03 11:25:06.493172

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8656f79d7a02'
down_revision = 'a56900e65050'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles_permissions',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], )
    )
    op.alter_column('comment', 'from_post_author',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('comment', 'is_hidden',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('post', 'can_comment',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('task', 'complete',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.add_column('user', sa.Column('role_id', sa.Integer(), nullable=True))
    op.alter_column('user', 'confirmed',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'])
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.alter_column('user', 'confirmed',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_column('user', 'role_id')
    op.alter_column('task', 'complete',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('post', 'can_comment',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('comment', 'is_hidden',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('comment', 'from_post_author',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_table('roles_permissions')
    op.drop_table('role')
    op.drop_table('permission')
    # ### end Alembic commands ###
