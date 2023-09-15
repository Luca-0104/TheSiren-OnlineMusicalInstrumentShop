from flask import abort

from . import errors



@errors.route("/errors/403")
def abort_403():
    abort(403)


@errors.route("/errors/404")
def abort_404():
    abort(404)


@errors.route("/errors/500")
def abort_500():
    abort(500)
