"""
View module for new admin tasks
"""

from flask import (
    Blueprint,
    current_app as app,
    flash,
    redirect,
    render_template,
    request, Response,
    url_for
)

from src.models import Cert, db

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates"
)


@admin_bp.route("/manage_publishing", methods=["GET", "POST"])
def manage_publishing() -> Response:
    """
    Endpoint for managing cert publishing once
    the app routing and HTML files have been
    put in place

    Returns:
        Response: Flask Response object
    """
    if request.method == "POST":
        params = request.form["route"]
        for rule in app.url_map.iter_rules():
            if rule.endpoint == params:
                cert = Cert.find_by_route(params)
                cert.published = True
                db.session.commit()
                flash("Cert published successfully", "message")
                return redirect(url_for("certs.certs"))
        certs = Cert.find_unpublished()
        msg = f"Unable to publish cert as route '{params}' does not exists"
        return render_template("publish.html", certs=certs, msg=msg, title="CT: Manage Publishing")
    certs = Cert.find_unpublished()
    return render_template("publish.html", certs=certs, title="CT: Manage Publishing")
