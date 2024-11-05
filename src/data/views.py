"""
User created routes for new certs
"""

# pylint: disable=unused-import

import json

from flask import abort, Blueprint, render_template, Response, request

from src.content.forms import AddResourceForm, AddSectionForm
from src.models import Cert

data_bp = Blueprint(
    "data",
    __name__,
    template_folder="templates"
)


def fetch_cert(cert: Cert, forms: tuple, template: str, og_data=None) -> str:
    """
    Fetches the cert data and returns the template with
    the data fields updated

    Args:
        cert (Cert): Cert object
        forms (tuple): creation forms
        template (str): template HTML file
        og_data (None | dict): data pulled from opengraph
        og_data (None | bool): was pulled from opengraph?

    Returns:
        str: template string
    """
    if og_data:
        og_result = json.loads(og_data)
        og_data_sent = True
    else:
        og_result = None
        og_data_sent = None
    courses = cert.fetch_resources("course")
    videos = cert.fetch_resources("video")
    articles = cert.fetch_resources("article")
    documents = cert.fetch_resources("documentation")
    resource_form, section_form = forms
    return render_template(
        template,
        resource_form=resource_form,
        section_form=section_form,
        cert=cert,
        course_data=courses,
        video_data=videos,
        article_data=articles,
        document_data=documents,
        title=f"CT: {cert.name}",
        og_data=og_result,
        has_og_data=og_data_sent,
    )
