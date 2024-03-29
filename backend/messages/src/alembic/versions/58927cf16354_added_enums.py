"""added enums

Revision ID: 58927cf16354
Revises: 8dc212a41ff7
Create Date: 2020-10-11 21:59:59.355592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58927cf16354'
down_revision = '8dc212a41ff7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emailtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_emailtype_id'), 'emailtype', ['id'], unique=False)
    op.add_column('email', sa.Column('emailtype_id', sa.Integer(), nullable=True))
    op.alter_column('email', 'category',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('general', 'newaccount', 'paswordreset', name='email_type'),
               existing_nullable=True)
    op.create_foreign_key(None, 'email', 'emailtype', ['emailtype_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'email', type_='foreignkey')
    op.alter_column('email', 'category',
               existing_type=sa.Enum('general', 'newaccount', 'paswordreset', name='email_type'),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_column('email', 'emailtype_id')
    op.drop_index(op.f('ix_emailtype_id'), table_name='emailtype')
    op.drop_table('emailtype')
    # ### end Alembic commands ###
