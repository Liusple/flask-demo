"""Todo add timestamp

Revision ID: 10a4b744e42a
Revises: 6766fe08f185
Create Date: 2017-06-20 21:36:15.298506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10a4b744e42a'
down_revision = '6766fe08f185'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_todos_timestamp'), 'todos', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_todos_timestamp'), table_name='todos')
    op.drop_column('todos', 'timestamp')
    # ### end Alembic commands ###
