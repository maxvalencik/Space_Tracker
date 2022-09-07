from csv import DictReader
from app import db
from models import User, Role

db.drop_all()
db.create_all()

r1 = Role(
    roleType='Spaceport',
    definition='Launch site for vertical or horizontal launches'
)

r2 = Role(
    roleType='Launcher',
    definition='Entity launching payload and/or crews into Space',
)

r3 = Role(
    roleType='Enthusiast',
    definition='Whoever is interested in the things of Space',
)

db.session.add_all([r1, r2, r3])
db.session.commit()

# with open('generators/roles.csv') as roles:
#     db.session.bulk_insert_mappings(Role, DictReader(roles))

# with open('generators/users.csv') as users:
#     db.session.bulk_insert_mappings(User, DictReader(users))
