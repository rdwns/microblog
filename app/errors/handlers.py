from flask import render_template
from app import db
from app.errors import bp

@bp.app_errorhandler(404)
def notfound(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internalerror(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500