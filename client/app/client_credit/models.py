from app import db
from app.base_class import Base
import datetime
## db inherit from this file

class ClientCredit(Base):
    _tablename_ = "ClientCredit"

    transId = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.String(), nullable=False)
    currentBalance = db.Column(db.Float(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    total_used = db.Column(db.Float(), nullable=False)
    used_per_hour = db.Column(db.Float(), nullable=False)
    create_time = db.Column(db.Integer(), nullable=False)
    end_time = db.Column(db.Integer(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)


    def __init__(self, transId, email, create_time, content, currentBalance, amount, end_time, total_used, is_active, used_per_hour):
        self.transId = transId
        self.email = email
        self.create_time = create_time
        self.end_time = end_time
        self.total_used = total_used
        self.is_active = is_active
        self.used_per_hour = used_per_hour
        self.content = content
        self.amount = amount
        self.currentBalance = currentBalance
    
    def __repr__(self):
        return "<User {}>".format(self.username)
    
    # Test json if ok => return 200 status
    def json(self):
        return {
            "transId": self.transId,
            "email": self.email,
            "create_time": self.create_time,
            "end_time": self.end_time,
            "total_used": self.total_used,
            "is_active": self.is_active,
            "used_per_hour": self.used_per_hour,
            "content": self.content,
            "currentBalance": self.currentBalance,
            "amount": self.amount,
        }, 200
