"""
App routes test module
"""

from flask.testing import FlaskClient


class TestRoutes:
    """
    Tests correct responses from app routes
    """

    # ===== / =====

    def test_core_index_returns_correct_page(self, client: FlaskClient) -> None:
        """
        Asserts the correct page is returned by core.index

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert b"Cert Tracker" in response.data

    def test_core_index_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by core.index

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/")
        assert response.status_code == 200

    # ===== /certs =====

    def test_certs_certs_returns_correct_page(self, client: FlaskClient) -> None:
        """
        Asserts the correct page is returned by certs.certs

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/certs")
        assert b"Certifications" in response.data

    def test_certs_certs_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by certs.certs

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/certs")
        assert response.status_code == 200

    # ===== /search =====

    def test_certs_search_returns_correct_page(self, client: FlaskClient) -> None:
        """
        Asserts the correct page is returned by certs.search

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/search")
        assert b"Search" in response.data

    def test_certs_search_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by certs.search

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/search")
        assert response.status_code == 200

    def test_certs_search_returns_307(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by certs.search

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.post("/search", data={"search": "test"})
        assert response.status_code == 307

    def test_certs_search_displays_empty_search_message(self, client: FlaskClient) -> None:
        """
        Assert message is displayed to user if search box is empty on submit
        """
        response = client.post("/search", data={"search": ""})
        assert b"Please provide a term to search for" in response.data

    # ===== /results =====

    def test_certs_results_returns_search_page(self, client: FlaskClient) -> None:
        """
        Asserts the search page is returned by certs.results without POST data

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/results")
        assert b"Search" in response.data

    def test_certs_results_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by certs.results

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/results")
        assert response.status_code == 200

    def test_certs_results_returns_results_page_with_params(self, client: FlaskClient) -> None:
        """
        Asserts the results page is returned by certs.results without POST data

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.post("/results?search=test")
        assert b"Results" in response.data

    def test_certs_results_returns_200_with_params(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by certs.results

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.post("/results?search=test")
        assert response.status_code == 200

    # ===== /create/ =====

    def test_content_create_returns_search_page(self, client: FlaskClient) -> None:
        """
        Asserts the search page is returned by content.create without POST data

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/create/")
        assert b"Create new cert" in response.data

    def test_content_create_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by content.create

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/create/")
        assert response.status_code == 200

    # ===== /create/resource =====

    def test_content_create_resource_returns_405(self, client: FlaskClient) -> None:
        """
        Asserts the /create/resource page returns 405 for GET

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/create/resource")
        assert response.status_code == 405

    # ===== /admin/manage_publishing =====

    def test_admin_manage_publishing_returns_search_page(self, client: FlaskClient) -> None:
        """
        Asserts the search page is returned by admin.manage_publishing without POST data

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/admin/manage_publishing")
        assert b"Manage publishing" in response.data

    def test_admin_manage_publishing_returns_200(self, client: FlaskClient) -> None:
        """
        Asserts the correct code is returned by admin.manage_publishing

        Args:
            client (FlaskClient): client returned by fixture
        """
        response = client.get("/admin/manage_publishing")
        assert response.status_code == 200
