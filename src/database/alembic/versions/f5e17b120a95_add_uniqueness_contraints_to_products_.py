"""add uniqueness contraints to products category, variety and packaging 

Revision ID: f5e17b120a95
Revises: da7701d1b980
Create Date: 2023-06-19 17:56:44.898097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5e17b120a95'
down_revision = 'da7701d1b980'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'products', ['Category', 'Variety', 'Packaging'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    # ### end Alembic commands ###