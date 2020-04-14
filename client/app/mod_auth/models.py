from app import db
from app.base_class import Base

# other database will inherit form this class

class User(Base):
    __tablename__ = "Users"

    #  create new user
    name = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password, role, status):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.status = status

    def __repr__(self):
        return "<User %r>" % (self.name)
