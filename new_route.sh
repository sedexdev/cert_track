# Usage:
#
# ./new_route <route_name>
#
# scripts args:
#   - $1 = route (doubles up as HTML file name)

# ===== ADD NEW FLASK ROUTE =====

# append new route to certs data_routes.py file
cat << EOF >> src/data/views.py


@data_bp.route("/$1", methods=["GET"])
def $1() -> Response:
    """
    Returns the $1 cert template

    Returns:
        Response: app response object
    """
    resource_form = AddResourceForm()
    section_form = AddSectionForm()
    cert = Cert.find_by_path(request.path)
    if not cert:
        abort(404)
    return fetch_cert(
        cert,
        (resource_form, section_form),
        "$1.html"
    )
EOF

# ===== CREATE NEW HTML TEMPLATE =====

# create template file
touch src/data/templates/$1.html

# add cert data layout to html file
cat << EOF >> src/data/templates/$1.html
{% extends 'cert_heading.html' %}
{% from 'macros/data.html' import stats, courses, videos, articles, documentation with context %}

{% block cert_content %}

<div id="statistics" class="my-16">
    {{ stats(cert) }}
</div>

<div id="courses" class="hidden my-16">
    {{ courses(course_data) }}
</div>

<div id="videos" class="hidden my-16">
    {{ videos(video_data) }}
</div>

<div id="articles" class="hidden my-16">
    {{ articles(article_data) }}
</div>

<div id="documentation" class="hidden my-16">
    {{ documentation(document_data) }}
</div>

{% endblock %}
EOF

# ===== UPDATE PATH WHITELIST IN state.js =====

# set state.js file path
FILE_PATH="./src/static/js/state.js"

# find the line number of the closing ]; for the route whitelist array
LINE=$(grep -n -m 1 "];" $FILE_PATH)
LINE_NUM=$(cut -d ":" -f1 <<< $LINE)

# insert the new path at that line
sed -i -e "$(echo $LINE_NUM)i \"$1\"," $FILE_PATH

# ===== REDEPLOY APP =====

# destroy and rebuild containers
sudo docker compose down --rmi local
sudo docker compose up
