from app.errors import errors
from flask import redirect, url_for, flash, current_app, request, render_template

@errors.app_errorhandler(404)
def page_not_found(e):
    '''
        Function to display the error 404 page whenever the required page is not found
    '''
    # note that we set the 404 status explicitly
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def access_forbidden(e):
    '''
        Function to display the error 403  page whenever access is forbidden to the user
    '''
    # note that we set the 403 status explicitly
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def internal_server(e):
    '''
        The function to display the error 500 page whenever the server encounters an unexpected error
    '''
    # note that we set the 500 status explicitly
    return render_template('errors/500.html'), 500