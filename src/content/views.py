"""
View module for new cert creation
"""

# pylint: disable=inconsistent-return-statements

import json

from urllib.error import HTTPError, URLError

import opengraph_py3

from flask import Blueprint, flash, redirect, render_template, request, Response, url_for
from sqlalchemy.exc import IntegrityError

from src.content.forms import AddResourceForm, AddSectionForm, CreateCertForm
from src.models import db, Cert, Course, Resource, Section


content_bp = Blueprint(
    "content",
    __name__,
    template_folder="templates"
)


@content_bp.route("/create/", methods=["GET", "POST"])
def create() -> Response:
    """
    Returns the cert creation form template

    Returns:
        Response: Response object
    """
    form = CreateCertForm()
    if request.method == "POST" and form.validate_on_submit():
        failed_constraint = Cert.exists(form.name.data, form.code.data)
        if failed_constraint:
            flash(f"{failed_constraint} must be unique", "error")
            return redirect(url_for("certs.certs"))
        Cert.create_new(form)
        return redirect(url_for("certs.certs"))
    return render_template("new_cert.html", form=form, title="CT: Create")


@content_bp.route("/create/resource", methods=["POST"])
def create_resource() -> None:
    """
    Creates a new resource on a Cert object
    """
    form = AddResourceForm()
    if request.method == "POST" and form.validate_on_submit():
        # get the resource type and create new resource of that type
        data = {
            "cert_id": request.form["cert-id"],
            "resource_type": form.resource_type.data,
            "url": form.url.data,
            "title": form.title.data,
            "image": form.image.data,
            "description": form.description.data,
            "site_logo": form.site_logo.data,
            "site_name": form.site_name.data,
        }
        has_og_data = request.form.get("has_og_data", None)
        if has_og_data:
            data["has_og_data"] = True
        if form.resource_type.data == "course":
            failed_constraint = Course.exists(form.url.data, form.title.data)
            if failed_constraint is not None:
                flash(f"{failed_constraint} must be unique", "error")
            else:
                Course.create_new(data)
                flash(
                    f"Course {form.title.data} created successfully", "success")
        else:
            try:
                Resource.create_new(data)
                flash(f"Resource {form.title.data} \
                      created successfully", "success")
            except IntegrityError:
                db.session.rollback()
                flash("Create resource failed", "error")
        return redirect(url_for(request.form["origin"]), 302)
    try:
        og_data = opengraph_py3.OpenGraph(form.url.data)
        og_dict = {}
        for key, value in og_data.items():
            og_dict[key] = value
        return redirect(
            url_for(
                request.form["origin"],
                og_data=json.dumps([og_dict]),
                has_og_data=True),
            307)
    except HTTPError:
        return Response(status=204)
    except ValueError:
        return Response(status=204)
    except URLError:
        return Response(status=204)


@content_bp.route("/create/section", methods=["POST"])
def create_section() -> None:
    """
    Creates a new section on a Course object
    """
    form = AddSectionForm()
    if request.method == "POST" and form.validate_on_submit():
        data = {
            "course_id": request.form["course-id"],
            "number": form.number.data,
            "title": form.title.data,
        }
        try:
            Section.create_new(data)
            flash(f"Section {data["number"]} added successfully", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Section data must be unique", "error")
        cert = Cert.query.filter_by(id=request.form["cert-id"]).first()
        return redirect(url_for(cert.route), 302)


@content_bp.route("/update/section", methods=["POST"])
def update_section() -> None:
    """
    Updates a section
    """
    form = AddSectionForm()
    if request.method == "POST" and form.validate_on_submit():
        section_id = request.form["section-id"]
        section = Section.query.filter_by(id=section_id).first()
        section.update({
            "cards_made": form.cards_made.data,
            "complete": form.complete.data,
        })
        return Response(status=204)
