import sys
from flask import _request_ctx_stack


def wrap_app_logger(app):
    """
    This function given Application and add logger for that.

    :param app: Application Object
    :type app: Object
    """
    app.debug_log_format = app.config['LOG_FORMAT']
    app._logger = None
    app._logger = LoggerWrapper(app.logger)
    app.logger.info('Starting project')


class LoggerWrapper(object):

    """
    This Class initial and make Logger wrapper.

    :param logger: Logger instance object
    :type logger: Object
    :param logger_name: Name for save logger as it
    "type logger_name: String
    """

    def __init__(self, logger, logger_name='shopify'):
        self.logger_name = logger_name
        self.logger = logger
        self.extra_handlers = []

    def process(self, msg, args, kwargs):
        """
        This function given message as msg and argument as args and kwargs, then create logger messages.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict

        :returns: Set of msg, args, kwargs.
        :rtype: Set
        """
        path = method = remote_addr = user_agent = url = u''

        ctx = _request_ctx_stack.top

        if ctx is not None:
            path = ctx.request.path
            url = ctx.request.url
            method = ctx.request.method
            remote_addr = ctx.request.remote_addr
            user_agent = ctx.request.headers.get('user-agent', u'')

        kwargs['extra'] = dict(
            logger_name=self.logger_name,
            http_path=path,
            http_url=url,
            http_method=method,
            http_remote_addr=remote_addr,
            http_user_agent=user_agent
        )

        for handler in self.extra_handlers:
            handler(kwargs['extra'], ctx)

        if args:
#            if isinstance(args[0], dict):
            msg = msg + ' ' + repr(args[0])

        return msg, [], kwargs

    def create_logger(self, name):
        """
        This Function create Logger with given name.

        :param name: Logger name for creating logger
        :type name: String
        """
        assert not hasattr(self, name)
        setattr(self, name, LoggerWrapper(self.logger, name))

    def debug(self, msg, *args, **kwargs):
        """
        This function create and execute log with Debug mode.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        This function create and execute log with Info mode.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        This function create and execute log with Warning mode.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        This function create and execute log with Error mode.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        This function create and execute log for exception raise error.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        kwargs['exc_info'] = sys.exc_info()
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        This function create and execute log with Critical mode.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        self.logger.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """
        This function create and execute log.

        :param msg: body of message
        :type msg: String
        :param args: list of parameter's
        :type args: List
        :param kwargs: Dict of arqument's attribute
        :type kwargs: Dict
        """
        msg, args, kwargs = self.process(msg, args, kwargs)
        self.logger.log(level, msg, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.logger, name)

    @property
    def inject(self, f):
        """
        :example:

        .. code-block:: python

            app.logger.inject
            def log_user(d, ctx):
                d['app_user'] = 'anonymous'
                if ctx is not None and ctx.g.user is not None:
                d['app_user'] = ctx.g.user.username
        """

        self.extra_handlers.append(f)
        return f
