# Import all the models, so that Base has them before being
# imported by Alembic

from app.database.base_class import Base  # noqa
from app.apps.mail.models import EMail  # noqa