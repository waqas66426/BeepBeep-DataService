from .home import home
from .runs import runs_api
from .users import users_api
from .challenges import challenges_api

blueprints = [home, runs_api, users_api, challenges_api]
