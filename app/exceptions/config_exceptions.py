from app.exceptions.exceptions import ExceptionBase


def init_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, (ExceptionBase)):
            return e.return_exception()

        return ExceptionBase(message=str(e)).return_exception()
