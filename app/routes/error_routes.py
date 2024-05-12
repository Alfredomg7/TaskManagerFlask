from flask import render_template

def register_error_routes(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        print("500 error handler triggered")
        return render_template('500.html'), 500
    
    @app.route('/500-error')
    def error500():
        raise Exception("500 error")