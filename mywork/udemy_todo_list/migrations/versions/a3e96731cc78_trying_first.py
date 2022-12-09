"""trying first

Revision ID: a3e96731cc78
Revises: 
Create Date: 2022-08-08 17:18:45.029553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3e96731cc78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TODOLIST',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.Text(), nullable=True),
    sa.Column('task_status', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TODOLIST')
    # ### end Alembic commands ###
