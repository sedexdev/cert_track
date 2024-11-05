"""
Content operations test module
"""

# pylint: disable=duplicate-code

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.routing.rules import Rule

from src.models import Cert, Course, Resource, Section


class TestCerts:
    """
    Cert creation and management test class. Includes case for 
    all composite classes of Cert (Video/Article/Course etc) 
    """

    @classmethod
    def setup_class(cls) -> None:
        """
        Setup class before all tests run
        """
        cls.cert_data = None
        cls.resource_data = None
        cls.section_data = None

    def setup_method(self) -> None:
        """
        Setup class before all tests run
        """
        # create new cert from form
        self.cert_data = {
            "name": "Test",
            "code": "tst-101",
            "date": "01/01/2000",
            "head_img": "test/test.jpg",
            "badge_img": "etest/BADGE_test.png",
            "exam_date": "",
            "tags": ["test"],
        }
        # create a new resource on the cert
        self.resource_data = {
            "resource_type": "course",
            "url": "http://test.test",
            "title": "Test Course",
            "image": "test/test.png",
            "description": "This is a test course",
            "site_logo": "test.svg",
            "site_name": "Test",
        }
        # create a new section on a course
        self.section_data = {
            "number": "1",
            "title": "Test section",
            "cards_made": None,
            "complete": None,
        }

    def test_content_create_resource_creates_course(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert a Course object is created and saved in the DB

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.cert_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            self.resource_data["cert-id"] = cert.id
            self.resource_data["origin"] = "certs.certs"
        client.post("/create/resource", data=self.resource_data)
        with app.app_context():
            course = Course.query.filter_by(id=1).first()
        assert course is not None

    def test_content_create_resource_creates_article(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert a Resource object is created and saved in the DB

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.cert_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            self.resource_data["cert-id"] = cert.id
            self.resource_data["resource_type"] = "article"
            self.resource_data["origin"] = "certs.certs"
        client.post("/create/resource", data=self.resource_data)
        with app.app_context():
            resource = Resource.query.filter_by(id=1).first()
        assert resource is not None

    def test_content_create_section_creates_section(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert a Section object is created and saved in the DB

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # add rule first
        with app.app_context():
            rule = Rule("/test", endpoint="data.test_tst101")
            app.url_map.add(rule)
        # create test cert/course/section
        client.post("/create/", data=self.cert_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            self.resource_data["cert-id"] = cert.id
            self.resource_data["origin"] = "certs.certs"
        client.post("/create/resource", data=self.resource_data)
        with app.app_context():
            course = Course.query.filter_by(id=1).first()
            self.section_data["course-id"] = course.id
            self.section_data["cert-id"] = cert.id
        client.post("/create/section", data=self.section_data)
        with app.app_context():
            section = Section.query.filter_by(id=1).first()
        assert section is not None

    def test_content_update_section_updates_section(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert a Section object is updated and saved in the DB

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # add rule first
        with app.app_context():
            rule = Rule("/test", endpoint="data.test_tst101")
            app.url_map.add(rule)
        # create a cert
        client.post("/create/", data=self.cert_data)
        # update data to create a course
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            self.resource_data["cert-id"] = cert.id
            self.resource_data["origin"] = "certs.certs"
        # create a course resource on the cert
        client.post("/create/resource", data=self.resource_data)
        # update data to create a course section
        with app.app_context():
            course = Course.query.filter_by(id=1).first()
            self.section_data["course-id"] = course.id
            self.section_data["cert-id"] = cert.id
        # create a course section
        client.post("/create/section", data=self.section_data)
        # update the data on the section
        self.section_data["section-id"] = 1
        self.section_data["cards_made"] = True
        client.post("/update/section", data=self.section_data)
        # get the updated section
        with app.app_context():
            section = Section.query.filter_by(id=1).first()
        assert section.cards_made and not section.complete
