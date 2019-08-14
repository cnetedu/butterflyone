from bfly.db import db
import enum


class Resume(db.Model):
    __tablename__ = "resume"
    id = db.Column(db.String(255), primary_key=True)
    data = db.Column(db.BLOB)
    name = db.Column(db.String(45))
    contentType = db.Column(db.String(120))


def get_resume(id):
    return Resume.query.get(id)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(255), nullable=False, primary_key=True)
    fullname = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(120))
    major = db.Column(db.String(120))
    college = db.Column(db.String(255))
    graduationMonth = db.Column(db.Integer)
    graduationYear = db.Column(db.Integer)
    gpa = db.Column(db.String(10))
    currentLocation = db.Column(db.String(120))
    desiredLocation1 = db.Column(db.String(120))
    desiredLocation2 = db.Column(db.String(120))
    desiredLocation3 = db.Column(db.String(120))
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
    requesting_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
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

    if 'id' in params:
        del params['id']

    for key, value in params.items():
        setattr(user, key, value)
    ret_dict = user.to_dict()
    db.session.add(user)
    db.session.commit()
    return ret_dict


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
        id = "1",
        fullname = "George Sequeira",
        phone = "3016936356",
        email = "george@butterflyone.co",
        major = "Public Relations",
        college = "The City College of New York",
        graduationMonth = 5,
        graduationYear = 2021,
        gpa = "3.2",
        currentLocation = "New York City, NY",
        desiredLocation1 = "San Francisco, CA")

    diego = User(
        id = "diego",
        fullname = "Diego Clare",
        phone = "3016936357",
        email = "diego@butterflyone.co",
        major = "Biochemistry, Biophysics, Molecular Biology",
        college = "The City College of New York",
        graduationMonth = 5,
        graduationYear = 2021,
        gpa = "3.5",
        currentLocation = "New York City, NY",
        desiredLocation1 = "San Francisco, CA")

    jake = User(
        id = "jake",
        fullname = "Jake Rosenfeld",
        phone = "3016936357",
        email = "jake@butterflyone.co",
        major = "Political Science",
        college = "Lehman College",
        graduationMonth = 5,
        graduationYear = 2021,
        gpa = "3.0",
        currentLocation = "New York City, NY",
        desiredLocation1 = "San Francisco, CA")

    andres = User(
        id = "andres",
        fullname = "Andres Palmiter",
        phone = "3016936357",
        email = "andres@butterflyone.co",
        major = "Law",
        college = "John Jay College of Criminal Justice",
        graduationMonth = 5,
        graduationYear = 2021,
        gpa = "4.0",
        currentLocation = "New York City, NY",
        desiredLocation1 = "San Francisco, CA")

    db.session.add(george)
    db.session.add(diego)
    db.session.add(jake)
    db.session.add(andres)
    db.session.commit()

    george_resume = Resume(
        id=george.id,
        data=b'George Resume',
        name='george_resume.txt',
        contentType='txt')

    db.session.add(george_resume)
    db.session.commit()
