# pylint: disable=W0611:unused-import

from rich.console import Console
from sqlalchemy.exc import SQLAlchemyError

from src.logging.logger_handler import LevelName, LoggerHandler
from src.models.entities import BidEntity, CompanyEntity, DocumentEntity
from src.models.settings.base import Base
from src.models.settings.connection import DBConnectionHandler

logger_handler = LoggerHandler(level=LevelName.DEBUG)
logger = logger_handler.get_logger()

console = Console()


def create_database_schema() -> None:
    try:
        db = DBConnectionHandler()
        engine = db.get_engine()

        Base.metadata.create_all(engine)
        logger.debug("Database schema successfully created.")

    except SQLAlchemyError as exc:
        logger.error("Error creating database schema: %s", exc)
