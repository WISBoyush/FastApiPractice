"""update author table

Revision ID: 5ef436b8a76b
Revises: f54edeb81a68
Create Date: 2022-11-17 11:36:50.422893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ef436b8a76b'
down_revision = 'f54edeb81a68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authors', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('authors', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('authors', sa.Column('bio', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('authors', 'bio')
    op.drop_column('authors', 'last_name')
    op.drop_column('authors', 'first_name')
    # ### end Alembic commands ###
