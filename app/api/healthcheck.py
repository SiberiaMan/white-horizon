from aiohttp import web

from app.abstracts import AbstractApi

class HealthCheckApi(AbstractApi):
    def __init__(self, app):
        routes = [
            web.get("/ready", self.ready),
        ]
        super().__init__(app=app, routes=routes)

    async def ready(self, request: web.Request) -> web.Response:
        """
        ---
        get:
          description: "Healthcheck"
          responses:
            '200':
              description: Ok
            '500':
              description: Internal Server Error
        """
        return web.HTTPOk(text="До 25")
