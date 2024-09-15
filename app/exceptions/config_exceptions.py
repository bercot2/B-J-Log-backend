from app.exceptions.exceptions import ExceptionBase, ExceptionNoDataFound


def init_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, (ExceptionBase, ExceptionNoDataFound)):
            return e.return_exception()

        return ExceptionBase().return_exception()
