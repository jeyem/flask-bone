from flask import render_template, jsonify, request, redirect as flask_redirect



def path(link):
    """
    make template address
    """
    return link


def render(template, **context):
    if request.is_xhr:
        return jsonify(html=render_template(path(template), **context))
    return render_template(path(template), **context)


def redirect(url):
    if request.is_xhr:
        return jsonify(redirect=url)
    return flask_redirect(url)
