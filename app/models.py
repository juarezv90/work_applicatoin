from datetime import date
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64),index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128),index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    attendances: so.WriteOnlyMapped['IssueReport'] = so.relationship(back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Location(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    location: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    employee: so.WriteOnlyMapped['Employee'] = so.relationship(back_populates='location')

class Employee(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    date_of_hire: so.Mapped[date] = so.mapped_column(sa.Date)
    date_of_term: so.Mapped[Optional[date]] = so.mapped_column(sa.Date, nullable=True)
    emp_active: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=True)
    location_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Location.id))

    location: so.Mapped[Location] = so.relationship(back_populates='employee')
    attendances: so.WriteOnlyMapped['IssueReport'] = so.relationship(back_populates='employee')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.date_of_hire} {self.location_id}'
    
class IssueReport(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    emp_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Employee.id), index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    issue: so.Mapped[str] = so.mapped_column(sa.Text, index=True)
    reason: so.Mapped[str] = so.mapped_column(sa.Text, index=True)
    date_of: so.Mapped[date] = so.mapped_column(sa.Date, default=lambda: date.today())

    user: so.Mapped[User] = so.relationship(back_populates='attendances')
    employee: so.Mapped[Employee] = so.relationship(back_populates='attendances')

    def __repr__(self):
        return '<Attendance_Tracking {}>'.format(self.issue)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))