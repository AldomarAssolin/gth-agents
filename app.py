from flask import Flask

from app.config import Config
from app.extensions import db
from infrastructure.database.models import *  # noqa: F401,F403
from interface.error_handler import register_error_handlers
from interface.routes.avaliacoes_routes import avaliacoes_interface_bp
from interface.routes.cadastros_routes import cadastros_interface_bp
from interface.routes.colaboradores_routes import colaboradores_interface_bp
from interface.routes.feedbacks_routes import feedbacks_interface_bp
from interface.routes.health_routes import health_bp
from interface.routes.metas_routes import metas_interface_bp
from interface.routes.auth_routes import auth_bp
from interface.routes.pdis_routes import pdis_interface_bp
from interface.routes.reconhecimentos_routes import reconhecimentos_interface_bp
from interface.routes.dashboard_routes import dashboard_interface_bp


def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cadastros_interface_bp)
    app.register_blueprint(colaboradores_interface_bp)
    app.register_blueprint(avaliacoes_interface_bp)
    app.register_blueprint(metas_interface_bp)
    app.register_blueprint(feedbacks_interface_bp)
    app.register_blueprint(pdis_interface_bp)
    app.register_blueprint(reconhecimentos_interface_bp)
    app.register_blueprint(dashboard_interface_bp)




    register_error_handlers(app)

    return app
