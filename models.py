import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json

database_path = os.environ['HEROKU_POSTGRESQL_GRAY_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''



def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # adds initial data for testing
    discipline_1 = Discipline(
        name = 'Calisthenics',
    )
    discipline_2 = Discipline(
        name = 'Yoga',
    )
    teacher_1 = Teacher(
        name = 'Dan K',
        discipline_id = 1,
        instagram_account = '@danK'
    )
    teacher_2 = Teacher(
        name = 'Francesco L',
        discipline_id = 2,
        instagram_account = '@FrancescoL'
    )
    session = Session(
        name = "Yoga with Francesco on Wed",
        gym_id = 1,
        teacher_id = 2,
        discipline_id = 2,
        start_time = "Wed, 1 June 2022 06:30:00 GMT",
        length_in_minutes = 90
    )
    gyms = [Gym(
        name = 'Blok',
        city = 'London',
        website = 'www.bloklondon.com'
    ),
    Gym(
        name = 'Zeus',
        city = 'Manchester',
        website = 'www.zeusmanchester.com'
    ),
    ]
    
    discipline_1.insert()
    discipline_2.insert()
    teacher_1.insert()
    teacher_2.insert()
    for gym in gyms:
      gym.insert()
    session.insert()


class Discipline(db.Model):
  __tablename__ = 'Disciplines'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      }

  def insert(self):
        db.session.add(self)
        db.session.commit()


class Teacher(db.Model):  
  __tablename__ = 'Teachers'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  discipline_id = Column(db.Integer, db.ForeignKey(Discipline.id, ondelete='CASCADE'), nullable=False )
  instagram_account = Column(String(120))

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'discipline_id': self.discipline_id,
      'instagram_account': self.instagram_account
      }

  def insert(self):
        db.session.add(self)
        db.session.commit()

  def update(self):
        db.session.commit()
  
  def delete(self):
        db.session.delete(self)
        db.session.commit()


class Gym(db.Model):  
  __tablename__ = 'Gyms'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  city = Column(String(120))
  website = Column(String(120))

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'city': self.city,
      'website': self.website
      }

  def insert(self):
        db.session.add(self)
        db.session.commit()




#Assocation table (A "Session" links "Teachers" with "Gyms" and "Disciplines")
class Session(db.Model):  
  __tablename__ = 'Sessions'

  id = Column(db.Integer, primary_key=True)
  name = Column(String)
  gym_id = Column(db.Integer, db.ForeignKey(Gym.id, ondelete='CASCADE'), nullable=False)
  teacher_id = Column(db.Integer, db.ForeignKey(Teacher.id, ondelete='CASCADE'), nullable=False)
  discipline_id = Column(db.Integer, db.ForeignKey(Discipline.id, ondelete='CASCADE'), nullable=False)
  start_time = Column(db.DateTime, default=func.now())
  length_in_minutes = Column(db.Integer, nullable=False)

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gym_id': self.gym_id,
      'teacher_id': self.teacher_id,
      'discipline_id': self.discipline_id,
      'start_time': self.start_time,
      'length_in_minutes': self.length_in_minutes
      }
    
  def insert(self):
    db.session.add(self)
    db.session.commit()