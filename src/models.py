"""
Module containing models for SQLAlchemy
"""

# pylint: disable=too-few-public-methods, import-error

from datetime import datetime

from flask import current_app as app, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# associative tables for many-to-many cert/tag relationships
tags_table = db.Table(
    'tag_association',
    db.Column('cert_id', db.ForeignKey('certs.id'), primary_key=True),
    db.Column('tag_id', db.ForeignKey('tags.id'), primary_key=True),
)

resources_table = db.Table(
    'resource_association',
    db.Column('cert_id', db.ForeignKey('certs.id'), primary_key=True),
    db.Column('resource_id', db.ForeignKey('resources.id'), primary_key=True),
)

course_table = db.Table(
    'course_association',
    db.Column('cert_id', db.ForeignKey('certs.id'), primary_key=True),
    db.Column(
        'course_id',
        db.ForeignKey('courses.id'),
        primary_key=True
    ),
)

section_table = db.Table(
    'section_association',
    db.Column('course_id', db.ForeignKey('courses.id'), primary_key=True),
    db.Column(
        'section_id',
        db.ForeignKey('sections.id'),
        primary_key=True
    ),
)


class Cert(db.Model):
    """
    Model defining cert specific data
    """

    __tablename__ = "certs"

    # information data
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False, unique=True)
    route = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    code = db.Column(db.String(255), nullable=False, unique=True)
    date = db.Column(db.String(64), nullable=False)
    tags = db.relationship(
        'Tag',
        secondary=tags_table,
        backref=db.backref('cert', lazy='dynamic')
    )
    head_img = db.Column(db.String(255), nullable=False)
    badge_img = db.Column(db.String(255), nullable=False)
    exam_date = db.Column(db.String(64))
    published = db.Column(db.Boolean, default=False)

    # statistical data
    resources = db.relationship(
        'Resource',
        secondary=resources_table,
        backref=db.backref('cert', lazy='dynamic')
    )
    courses = db.relationship(
        'Course',
        secondary=course_table,
        backref=db.backref('cert', lazy='dynamic')
    )

    @classmethod
    def create_new(cls, form: FlaskForm) -> None:
        """
        Initialises a new Cert instance and
        writes it to the DB

        Args:
            form (FlaskForm): Flask-WTF form template object
        """
        formatted_name = "_".join(form.name.data.split(" ")).lower()
        formatted_code = "_" \
            .join(form.code.data.split(" ")) \
            .lower() \
            .replace("-", "")
        path = f"/{formatted_name}_{formatted_code}"
        route = f"data.{formatted_name}_{formatted_code}"
        cert = Cert(
            path=path,
            route=route,
            name=form.name.data,
            code=form.code.data,
            date=form.date.data,
            head_img=form.head_img.data,
            badge_img=form.badge_img.data,
            exam_date=form.exam_date.data,
        )
        for tag in form.tags.data.split(","):
            cert.tags.append(Tag(name=tag.strip()))
        # update published if the route exists
        for rule in app.url_map.iter_rules():
            if rule.endpoint == route:
                cert.published = True
                flash("Cert has been published", "message")
        if not cert.published:
            flash(f"""Cert created successfully. Run './new_route.sh
                  {formatted_name}_{formatted_code}' in your terminal
                  to allow publishing""", "message")
        db.session.add(cert)
        db.session.commit()

    @classmethod
    def exists(cls, name: str, code: str) -> str:
        """
        Checks to see if a Cert exists in the database
        that would cause this creation to raise an 
        integrity violation

        Args:
            name (str): form name value
            code (str): form code value

        Returns:
            str: first value causing an integrity violation
        """
        certs = Cert.query.all()
        for cert in certs:
            if cert.name == name:
                return "Name"
            if cert.code == code:
                return "Code"
        return None

    @classmethod
    def find_published(cls) -> list:
        """
        Gets all certs that are in a published state

        Returns:
            _type_: list
        """
        results = []
        certs = Cert.query.all()
        for cert in certs:
            if cert.published:
                results.append(cert)
        return results

    @classmethod
    def find_unpublished(cls) -> list:
        """
        Gets all certs that are in an unpublished state

        Returns:
            _type_: list
        """
        results = []
        certs = Cert.query.all()
        for cert in certs:
            if not cert.published:
                results.append(cert)
        return results

    @classmethod
    def find(cls, query: str) -> list:
        """
        Runs a query against this model to find
        all entries that match the query string.

        Searched fields are:
        - path
        - name
        - code
        - tags

        Args:
            query (str): term to match against

        Returns:
            list: matching entries
        """
        certs = Cert.query.all()
        results = []
        for cert in certs:
            if cert.published:
                if query in cert.path:
                    results.append(cert)
                    continue
                if query in cert.name:
                    results.append(cert)
                    continue
                if query in cert.code:
                    results.append(cert)
                    continue
                for tag in cert.tags:
                    if query in tag.name:
                        results.append(cert)
                        break
        return results

    @classmethod
    def find_by_path(cls, path: str) -> __name__:
        """
        Get a single Cert entry based on path value

        Args:
            path (str): app endpoint value

        Returns:
            Cert: Cert instance
        """
        return Cert.query.filter_by(path=path).first()

    @classmethod
    def find_by_route(cls, route: str) -> __name__:
        """
        Get a single Cert entry based on route value

        Args:
            route (str): flask route endpoint value

        Returns:
            Cert: Cert instance
        """
        return Cert.query.filter_by(route=route).first()

    def fetch_resources(self, t: str) -> list:
        """
        Fetches all Resource objects of type t

        Args:
            t (str): resource type
        Returns:
            list: list of courses for the cert
        """
        if t == "course":
            return self.courses
        resources = Resource.query.filter_by(cert_id=self.id).all()
        return [x for x in resources if x.resource_type == t]


class Tag(db.Model):
    """
    Model defining a tag for a cert page
    """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Resource(db.Model):
    """
    Model defining a video for a cert page
    """

    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    cert_id = db.Column('cert_id', db.ForeignKey('certs.id'))
    resource_type = db.Column(db.String(64), nullable=False)
    url = db.Column(db.Text(), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    site_logo = db.Column(db.String(255), nullable=False)
    site_name = db.Column(db.String(255), nullable=False)
    has_og_data = db.Column(db.Boolean)
    timestamp = db.Column(db.String(64))

    @classmethod
    def create_new(cls, data: dict) -> None:
        """
        Initialises a new Resource instance and
        writes it to the DB

        Args:
            data (dict): dictionary of instance attribute values
        """
        data["timestamp"] = datetime.now().strftime("%m/%d/%Y:%H:%M:%S")
        resource = Resource(**data)
        cert = Cert.query.filter_by(id=data["cert_id"]).first()
        cert.resources.append(resource)
        db.session.add(resource)
        db.session.commit()


class Course(db.Model):
    """
    Model defining a full length course on the cert page
    """

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.PickleType(), nullable=False)  # Resource object
    sections = db.relationship(
        'Section',
        secondary=section_table,
        backref=db.backref('course', lazy='dynamic')
    )
    complete = db.Column(db.Boolean)

    @classmethod
    def create_new(cls, data: dict) -> None:
        """
        Initialises a new Course instance and
        writes it to the DB

        Args:
            data (dict): dictionary of instance attribute values
        """
        resource = Resource(**data)
        cert = Cert.query.filter_by(id=data["cert_id"]).first()
        course = Course(resource=resource)
        cert.courses.append(course)
        db.session.add(course)
        db.session.commit()

    @classmethod
    def exists(cls, url: str, title: str) -> str:
        """
        Checks the database to see if any unique form fields
        in a newly created Resource already exist

        Args:
            url (str): url for new Resource
            title (str): title for new Resource

        Returns:
            str: the first field that exists
        """
        courses = Course.query.all()
        for course in courses:
            if course.resource.url == url:
                return "URL"
            if course.resource.title == title:
                return "Title"
        return None


class Section(db.Model):
    """
    Model defining a course section
    """

    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column('course_id', db.ForeignKey('courses.id'))
    number = db.Column(db.Integer, nullable=False, unique=True)
    title = title = db.Column(db.String(255), nullable=False, unique=True)
    cards_made = db.Column(db.Boolean)
    complete = db.Column(db.Boolean)
    timestamp = db.Column(db.String(64))

    @classmethod
    def create_new(cls, data: dict) -> None:
        """
        Initialises a new Section instance and
        writes it to the DB

        Args:
            data (dict): dictionary of instance attribute values
        """
        data["timestamp"] = datetime.now().strftime("%m/%d/%Y:%H:%M:%S")
        section = Section(**data)
        course = Course.query.filter_by(id=data["course_id"]).first()
        course.sections.append(section)
        db.session.add(course)
        db.session.commit()

    def update(self, data: dict) -> None:
        """
        Updates this section instance with either the
        cards_made or complete value

        Args:
            data (dict): form data
        """
        self.cards_made = data["cards_made"]
        self.complete = data["complete"]
        db.session.commit()
