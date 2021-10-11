from api.db import db
from api.domains.routes import domain_router
from api.ruegen.routes import ruegen_router
from api.utility.routes import utility_router
from fastapi import FastAPI

api = FastAPI(
    title="web-of-web-trust-backend",
    description="The web of web trust backend. Making the web a bit more assessable ⚖️",
    version="0.0.1b0",
    contact={
        "name": "Cobalt",
        "url": "http://cobalt.rocks/",
        "email": "c0balt@disroot.org",
    },
    license_info={
        "name": "AGPL 3.0 (only)",
        "url": "https://www.gnu.org/licenses/agpl-3.0.txt",
    },
)
db.init_app(api)
api.include_router(domain_router)
api.include_router(ruegen_router)
api.include_router(utility_router)
