from abc import ABC


class AbstractApi(ABC):
    """
    Abstract base class for API classes.

    Arguments:
        app: aiohttp web application,
        routes: aiohttp routes.
    """

    def __init__(self, app, routes):
        self._routes = routes
        app.add_routes(self._routes)
        app.setdefault("api", []).append(self)