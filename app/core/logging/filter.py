import logging

from app.core import config


class LogFilter(logging.Filter):
    """Subclass of `logging.Filter` used to filter log messages.
    ---
    Filters identify log messages to filter out, so that the logger does not log
    messages containing any of the filters. If any matches are present in a log
    message, the logger will not output the message.
    The environment variable `LOG_FILTERS` can be used to specify filters as a
    comma-separated string, like `LOG_FILTERS="/health, /heartbeat"`. To then
    add the filters to a class instance, the `LogFilter.set_filters()`
    method can produce the set of filters from the environment variable value.
    """

    __slots__ = "name", "nlen", "filters"

    def __init__(
            self,
            name: str = "",
            filters: set[str] | None = None,
    ) -> None:
        """Initialize a filter."""
        self.name = name
        self.nlen = len(name)
        self.filters = filters

    def filter(self, record: logging.LogRecord) -> bool:
        """Determine if the specified record is to be logged.
        Returns True if the record should be logged, or False otherwise.
        """
        if self.filters is None:
            return True
        message = record.getMessage()
        return all(match not in message for match in self.filters)

    @staticmethod
    def set_filters(input_filters: str | None = None) -> set[str] | None:
        """Set log message filters.
        Filters identify log messages to filter out, so that the logger does not
        log messages containing any of the filters. The argument to this method
        should be supplied as a comma-separated string. The string will be split
        on commas and converted to a set of strings.
        This method is provided as a `staticmethod`, instead of as part of `__init__`,
        so that it only runs once when setting the `LOG_FILTERS` module-level constant.
        In contrast, the `__init__` method runs each time a logger is instantiated.
        """
        return (
            {log_filter.strip() for log_filter in str(log_filters).split(sep=",")}
            if (log_filters := input_filters or config.LOG_FILTERS)
            else None
        )
