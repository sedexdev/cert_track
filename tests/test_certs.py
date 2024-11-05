"""
Cert operations test module
"""

# pylint: disable=duplicate-code, line-too-long, too-many-public-methods

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.routing.rules import Rule

from src.models import Cert, db


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
        cls.form_data = None

    def setup_method(self) -> None:
        """
        Setup class before all tests run
        """
        # create new cert from form
        self.form_data = {
            "name": "Test",
            "code": "tst-101",
            "date": "01/01/2000",
            "head_img": "test/test.jpg",
            "badge_img": "etest/BADGE_test.png",
            "exam_date": "",
            "tags": ["test_tag"],
        }

    # ===== find_published() =====

    def test_find_published_returns_empty_list(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find_published() returns empty list since test cert
        defaults to unpublished

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            result = Cert.find_published()
        assert isinstance(result, list) and not result

    def test_find_published_returns_list_of_certs(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find_published() returns empty list since test cert
        defaults to unpublished

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # add rule first
        with app.app_context():
            rule = Rule("/test", endpoint="data.test_tst101")
            app.url_map.add(rule)
        # then create to ensure published is True
        client.post("/create/", data=self.form_data)
        # get cert
        with app.app_context():
            result = Cert.find_published()
        assert len(result) == 1 and result[0].name == "Test"

    # ===== find_unpublished() =====

    def test_find_unpublished_returns_test_cert(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find_unpublished() returns list with test cert since test 
        cert defaults to unpublished

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            result = Cert.find_unpublished()
        assert isinstance(result, list) and result[0].name == "Test"

    # ===== find() =====

    def test_find_returns_test_cert_from_path(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find() search query '/test_tst101' returns the test cert in a list 

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            # get new cert and update published attribute so find() will see it
            cert = Cert.query.filter_by(name="Test").first()
            cert.published = True
            db.session.commit()
            result = Cert.find("/test_tst101")
        assert isinstance(result, list) and result[0].name == "Test"

    def test_find_returns_test_cert_from_code(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find() search query 'tst-101' returns the test cert in a list 

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            # get new cert and update published attribute so find() will see it
            cert = Cert.query.filter_by(name="Test").first()
            cert.published = True
            db.session.commit()
            result = Cert.find("tst-101")
        assert isinstance(result, list) and result[0].name == "Test"

    def test_find_returns_test_cert_from_name(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find() search query 'Test' returns the test cert in a list 

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            # get new cert and update published attribute so find() will see it
            cert = Cert.query.filter_by(name="Test").first()
            cert.published = True
            db.session.commit()
            result = Cert.find("Test")
        assert isinstance(result, list) and result[0].name == "Test"

    def test_find_returns_test_cert_from_tag(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find() search query 'test_tag' returns the test cert in a list 

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            # get new cert and update published attribute so find() will see it
            cert = Cert.query.filter_by(name="Test").first()
            cert.published = True
            db.session.commit()
            result = Cert.find("test_tag")
        assert isinstance(result, list) and result[0].name == "Test"

    # ===== find_by_path() =====

    def test_find_by_path_returns_test_cert(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find_by_path() returns test cert

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            result = Cert.find_by_path("/test_tst101")
        assert result.name == "Test"

    # ===== find_by_route() =====

    def test_find_by_route_returns_test_cert(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert find_by_route() returns test cert

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            result = Cert.find_by_route("data.test_tst101")
        assert result.name == "Test"

    # ===== fetch_resources() =====

    def test_fetch_resources_returns_courses(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert fetch_resources() returns a list of courses

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # create a new cert
        client.post("/create/", data=self.form_data)
        # update resource data
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            resource_data = {
                "cert-id": 1,
                "resource_type": "course",
                "url": "http://test.test",
                "title": "Test Course",
                "image": "test/COU_test.png",
                "description": "This is a test course",
                "site_logo": "test.svg",
                "site_name": "Test",
                "origin": "certs.certs",
            }
        # create the resource
        client.post("/create/resource", data=resource_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            courses = cert.fetch_resources("course")
        assert courses[0].resource.title == "Test Course"

    def test_fetch_resources_returns_videos(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert fetch_resources() returns a list of videos

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # create a new cert
        client.post("/create/", data=self.form_data)
        # update resource data
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            resource_data = {
                "cert-id": 1,
                "resource_type": "video",
                "url": "http://test.test",
                "title": "Test Video",
                "image": "test/VID_test.png",
                "description": "This is a test video",
                "site_logo": "test.svg",
                "site_name": "Test",
                "origin": "certs.certs",
            }
        # create the resource
        client.post("/create/resource", data=resource_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            videos = cert.fetch_resources("video")
        assert videos[0].title == "Test Video"

    def test_fetch_resources_returns_articles(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert fetch_resources() returns a list of articles

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # create a new cert
        client.post("/create/", data=self.form_data)
        # update resource data
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            resource_data = {
                "cert-id": 1,
                "resource_type": "article",
                "url": "http://test.test",
                "title": "Test Article",
                "image": "test/ART_test.png",
                "description": "This is a test articles",
                "site_logo": "test.svg",
                "site_name": "Test",
                "origin": "certs.certs",
            }
        # create the resource
        client.post("/create/resource", data=resource_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            articles = cert.fetch_resources("article")
        assert articles[0].title == "Test Article"

    def test_fetch_resources_returns_documents(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert fetch_resources() returns a list of documents

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # create a new cert
        client.post("/create/", data=self.form_data)
        # update resource data
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            resource_data = {
                "cert-id": 1,
                "resource_type": "documentation",
                "url": "http://test.test",
                "title": "Test Document",
                "image": "test/DOC_test.png",
                "description": "This is a test document",
                "site_logo": "test.svg",
                "site_name": "Test",
                "origin": "certs.certs",
            }
        # create the resource
        client.post("/create/resource", data=resource_data)
        with app.app_context():
            cert = Cert.query.filter_by(name="Test").first()
            documents = cert.fetch_resources("documentation")
        assert documents[0].title == "Test Document"

    # ===== /create/ =====

    def test_create_new_creates_object(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert create_new() creates a new Cert and updates database

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)
        with app.app_context():
            cert = Cert.query.filter_by(name=self.form_data["name"]).first()
        assert cert is not None and cert.name == "Test"

    def test_create_new_redirects(self, client: FlaskClient) -> None:
        """
        Assert create_new() creates a new Cert and redirects user

        Args:
            client (FlaskClient): Flask app test client
        """
        response = client.post("/create/", data=self.form_data)
        assert response.status_code == 302

    def test_create_new_returns_form_if_not_valid(self, client: FlaskClient) -> None:
        """
        Assert create_new() returns the form if form invalid

        Args:
            client (FlaskClient): Flask app test client
        """
        response = client.post("/create/", data={})
        assert b"Create new cert" in response.data

    def test_create_new_sets_published_to_true(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert create_new() returns the form if form invalid

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        # add rule first
        with app.app_context():
            rule = Rule("/test", endpoint="data.test_tst101")
            app.url_map.add(rule)
        # then create to ensure published is True
        client.post("/create/", data=self.form_data)
        # get cert
        with app.app_context():
            cert = Cert.find_by_path("/test_tst101")
        assert cert.published

    # ===== /admin/manage_publishing =====

    def test_admin_manage_published_lists_test_cert(self, client: FlaskClient) -> None:
        """
        Assert admin.manage_published has the test cert listed as unpublished

        Args:
            client (FlaskClient): _description_
        """
        client.post("/create/", data=self.form_data)
        response = client.get("/admin/manage_publishing")
        assert b"tst-101" in response.data

    def test_admin_manage_publishing_displays_error_message(self, client: FlaskClient) -> None:
        """
        Assert admin.manage_published displays an error if route not listed
        in the Flask url_map

        Args:
            client (FlaskClient): _description_
        """
        client.post("/create/", data=self.form_data)
        response = client.post(
            "/admin/manage_publishing",
            data={"route": "/test"},
        )
        assert b"Unable to publish cert" in response.data

    def test_admin_manage_publishing_redirects(self, app: Flask, client: FlaskClient) -> None:
        """
        Assert that the cert is published immediately if rule exists

        Args:
            app (Flask): Flask app instance
            client (FlaskClient): Flask app test client
        """
        client.post("/create/", data=self.form_data)

        with app.app_context():
            rule = Rule("/test", endpoint="data.test_tst101")
            app.url_map.add(rule)

        client.post(
            "/admin/manage_publishing",
            data={"route": "data.test_tst101"}
        )

        with app.app_context():
            cert = Cert.find_by_path("/test_tst101")

        assert cert.published
