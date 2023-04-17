from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from rest_api_db import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)

    restaurant = relationship("Restaurants", back_populates="owner")

    # address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    # address = relationship("Address", back_populates="user_address")
    
class Restaurants(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)
    sub_category = Column(String)
    phone_number = Column(String)
    # complete = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("Users", back_populates="restaurant")

    address_id = Column(Integer, ForeignKey("address.id"), nullable=True)
    address = relationship("Address", back_populates="rest_address")

    booking_id = relationship("Booking", back_populates="restaurant")

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)

    rest_address = relationship("Restaurants", back_populates="address")

class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    email_id = Column(String)
    phone_number = Column(String)
    complete = Column(Boolean, default=False)
    booking_date = Column(String)
    booking_time = Column(String)

    restr_id = Column(Integer, ForeignKey("restaurants.id"), nullable=True)
    restaurant = relationship("Restaurants", back_populates="booking_id")

### sql query 
## to get all the entries from the datase where owner id is 1
# select * from todos where owner=1;


### connecting to sqlite db
### Create a db in instance python configuration first
# sqlite3 todos.db
#sqlite> .schema

'''
### How to alter table manually
ALTER TABLE users
	ADD phone_number varchar(12) DEFAULT NULL,
	ADD address_id integer DEFAULT NULL,
	ADD FOREIGN KEY (address_id) REFERENCES address(id);

### Creating a new table with FK relationship
DROP TABLE IF EXISTS sdf;

CREATE TABLE asd (
    id SERIAL,
    email varchar(200) DEFAULT NULL,
	username varchar(45) DEFAULT NULL,
	first_name varchar(45) DEFAULT NULL,
	last_name varchar(45) DEFAULT NULL,
	hashed_password varchar(200) DEFAULT NULL,
	is_active boolean DEFAULT NULL,
	PRIMARY KEY (id)
);

DROP TABLE IF EXISTS sdf;

CREATE TABLE tod (
	id SERIAL,
	title varchar(200) DEFAULT NULL,
	description varchar(200) DEFAULT NULL,
	priority integer DEFAULT NULL,
	complete boolean DEFAULT NULL,
	owner_id integer DEFAULT NULL,
	PRIMARY KEY (id)
	FOREIGN KEY (owner_id) REFERENCES users(id)
);
)
'''