"""Makes an organization's slug into a column.

Revision ID: c0bc938b058e
Revises: 0ab4f8f54bfa
Create Date: 2021-07-22 09:14:12.411910

"""
from alembic import op
from slugify import slugify
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = "c0bc938b058e"
down_revision = "0ab4f8f54bfa"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("organization", Column("slug", String()), schema="dispatch_core")
    op.create_unique_constraint(None, "organization", ["name"], schema="dispatch_core")

    # generate existing slugs
    conn = op.get_bind()
    res = conn.execute("select id, name from dispatch_core.organization")
    results = res.fetchall()

    for r in results:
        slug = slugify(r[1], separator="_")
        conn.execute(f"update dispatch_core.organization set slug = '{slug}' where id = {r[0]}")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("organization", "slug", schema="dispatch_core")
    op.drop_constraint(None, "organization", schema="dispatch_core", type_="unique")
    # ### end Alembic commands ###
