from bfly.db import db
import enum


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(255), nullable=False, primary_key=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(120))
    major1 = db.Column(db.String(120))
    major2 = db.Column(db.String(120))
    major3 = db.Column(db.String(120))
    college = db.Column(db.String(255))
    graduationMonth = db.Column(db.Integer)
    graduationYear = db.Column(db.Integer)
    preferredCity1 = db.Column(db.String(120))
    preferredCity2 = db.Column(db.String(120))
    preferredCity3 = db.Column(db.String(120))
    # research stuff
    research = db.relationship("MatchRequest")

    def __repr__(self):
        return 'User: {}, id: {}'.format(self.fullname, self.id)

    def to_dict(self):
        data = self.__dict__.copy()
        return data


def list_users(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (User.query
             .order_by(User.fullname)
             .limit(limit)
             .offset(cursor))
    users = [m.to_dict() for m in query.all()]
    next_page = cursor + limit if len(users) == limit else None
    return users, next_page


class MatchStatus(enum.Enum):
    pending = 0
    in_progress = 1
    done = 2


class MatchRequest(db.Model):
    __tablename__ = "match_request"
    id = db.Column(db.Integer, primary_key=True)
    requesting_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    worker_id = db.Column(db.String(255)) # admin key
    job = db.Column(db.String(255))
    status = db.Column(db.Enum(MatchStatus), default=MatchStatus.pending)


def get_user(id):
    result = User.query.get(id)
    if not result:
        return None
    return result.to_dict()


def update_user(id, params):
    user = User.query.get(id)
    if not user:
        raise ValueError("No user with that id")

    for key, value in params.items():
        setattr(user, key, value)
    db.session.add(user)
    db.session.commit()

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.String(255), nullable=False, primary_key=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(120))

    def __repr__(self):
        return '<Admin: {}, id: {}>'.format(self.fullname, self.id)


def get_admin(id):
    return Admin.query.get(id)


def create_tables():
    db.create_all()
    db.session.commit()

def initialize_data():
    george = User(
        id = "george",
        fullname = "George Sequeira",
        email = "george@butterflyone.co",
        major1 = "Public Relations",
        major2 = "Management",
        major3 = "Writing",
        college = "The City College of New York",
        graduationMonth = 5,
        graduationYear = 2021,
        preferredCity1 = "New York, New York",
        preferredCity2 = "San Francisco, CA",
        preferredCity3 = "")
    diego = User(
        id = "diego",
        fullname = "Diego Clare",
        email = "diego@butterflyone.co",
        major1 = "Biochemistry, Biophysics, Molecular Biology",
        major2 = "Computer Science",
        major3 = "Biotechnology",
        college = "The City College of New York",
        graduationMonth = 5,
        graduationYear = 2021,
        preferredCity1 = "New York, New York",
        preferredCity2 = "San Francisco, CA",
        preferredCity3 = "")

    jake = User(
        id = "jake",
        fullname = "Jake Rosenfeld",
        email = "jake@butterflyone.co",
        major1 = "Political Science",
        major2 = "Business Communications",
        major3 = "",
        college = "Lehman College",
        graduationMonth = 5,
        graduationYear = 2021,
        preferredCity1 = "New York, New York",
        preferredCity2 = "San Francisco, CA",
        preferredCity3 = "")

    andres = User(
        id = "andres",
        fullname = "Andres Palmiter",
        email = "andres@butterflyone.co",
        major1 = "Law",
        major2 = "Criminal Justice",
        major3 = "Legal Studies",
        college = "John Jay College of Criminal Justice",
        graduationMonth = 5,
        graduationYear = 2021,
        preferredCity1 = "New York, New York",
        preferredCity2 = "San Francisco, CA",
        preferredCity3 = "")

    db.session.add(george)
    db.session.add(diego)
    db.session.add(jake)
    db.session.add(andres)
    db.session.commit()
