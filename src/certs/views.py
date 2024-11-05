"""
Post app views module
"""

from flask import Blueprint, redirect, render_template, Response, request, url_for

from src.models import Cert

cert_bp = Blueprint(
    "certs",
    __name__,
    template_folder="templates"
)


@cert_bp.route("/certs")
def certs() -> Response:
    """
    Returns the certs template with data
    read from 'index.json'

    Returns:
        Response: app response object
    """
    data = Cert.find_published()
    return render_template("certs.html", certs=data, title="CT: Certs")


@cert_bp.route("/search", methods=["GET", "POST"])
def search() -> Response:
    """
    Returns the search template

    Returns:
        Response: app response object
    """
    if request.method == "POST":
        params = request.form["search"]
        if not params:
            message = "Please provide a term to search for"
            return render_template("search.html", message=message, title="CT: Search")
        return redirect(url_for("certs.results", search=params), code=307)
    return render_template("search.html", title="CT: Search")


@cert_bp.route("/results", methods=["GET", "POST"])
def results() -> Response:
    """
    Returns the results template

    Args:
        result (list): list of search results
    Returns:
        Response: app response object
    """
    if request.method == "POST":
        query = request.args.get("search")
        result = Cert.find(query)
        return render_template("results.html", query=query, certs=result, title="CT: Results")
    return render_template("search.html", title="CT: Search")
