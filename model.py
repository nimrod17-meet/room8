from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
#secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

# class Inventory(Base):
#     __tablename__ = 'inventory'
#     id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey('product.id'))
#     quantity = Column(Integer)
#     last_filled = Column(DateTime, default=func.now())
#     product = relationship("Product", back_populates="inventory")


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    apartments = relationship("Apartment", back_populates="owner")
    phoneNumber = Column(Integer)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def set_photo(self, photo):
        self.photo = photo

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Tenant(Base):
    __tablename__ = 'tenant'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    sex = Column(String(255))
    work = Column(String(255), unique=True)
    age = Column(Integer)
    intrests = Column(String(200))
    photo = Column(String)





class Apartment(Base):
    __tablename__ = 'apartment'
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    photo = Column(String)
    price = Column(Integer())
    address = Column(String(200))
    phoneNumber = Column(Integer)
    tenantNum = Column(Integer)
    owner = relationship("Customer", back_populates="apartments")
    owner_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    #inventory = relationship("Inventory", uselist=False, back_populates="product")
    


engine = create_engine('sqlite:///room8.db')


Base.metadata.create_all(engine)
