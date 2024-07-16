from projeto_pinterest import database, app
from projeto_pinterest.models import Usuario, Posts

with app.app_context():
    database.create_all()