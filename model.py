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


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    apartment = relationship("Apartment", back_populates="owner")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def set_photo(self, photo):
        self.photo = photo

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)






class Apartment(Base):
    __tablename__ = 'apartment'
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String(200))
    photo = Column(String(200))
    price = Column(Integer)
    phoneNumber = Column(Integer)
    owner = relationship("Member", back_populates="apartment")
    #inventory = relationship("Inventory", uselist=False, back_populates="product")
    


engine = create_engine('sqlite:///room8.db')


Base.metadata.create_all(engine)
