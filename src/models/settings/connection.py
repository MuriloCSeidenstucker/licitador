# pylint: disable=C0209:consider-using-f-string

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from src.logging.logger_handler import LevelName, LoggerHandler

logger_handler = LoggerHandler(level=LevelName.DEBUG)
logger = logger_handler.get_logger()


class DBConnectionHandler:
    """Gerencia a conexão com o banco de dados utilizando SQLAlchemy."""

    def __init__(self, connection_string: str = None) -> None:
        self.__connection_string = connection_string or "{}://{}:{}@{}:{}/{}".format(
            "mysql+pymysql", "root", "root", "localhost", "3306", "licitador"
        )
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self) -> Engine:
        """
        Creates and returns a SQLAlchemy Engine instance.
        Ensures the target database exists. Includes structured error handling.

        Returns:
            Engine: SQLAlchemy Engine instance.
        """
        try:
            engine = create_engine(self.__connection_string)

            if not database_exists(engine.url):
                logger.info(
                    "Database '%s' does not exist. Attempting to create...",
                    engine.url.database,
                )
                create_database(engine.url)
                logger.info("Database '%s' created successfully.", engine.url.database)
            else:
                logger.info(
                    "Database '%s' already exists. Proceeding with engine initialization.",
                    engine.url.database,
                )

            return engine

        except OperationalError as op_err:
            logger.error(
                "Operational error while connecting to database: %s", str(op_err)
            )
            raise

        except SQLAlchemyError as sql_err:
            logger.error(
                "SQLAlchemy error occurred during engine creation: %s", str(sql_err)
            )
            raise

        except Exception as exc:
            logger.exception(
                "Unexpected error during database engine creation: %s", str(exc)
            )
            raise

    def get_engine(self) -> Engine:
        """Retorna a engine do banco de dados.

        Returns:
            sqlalchemy.engine.Engine: Instância da engine de conexão com o banco de dados.
        """
        return self.__engine

    def __enter__(self) -> "DBConnectionHandler":
        """Inicia uma sessão no banco de dados.

        Returns:
            DBConnectionHandler: Retorna a própria instância com a sessão ativa.
        """
        session_maker = sessionmaker(bind=self.__engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha a sessão do banco de dados ao sair do contexto.

        Args:
            exc_type (Exception, optional): Tipo da exceção, se houver.
            exc_val (Exception, optional): Valor da exceção, se houver.
            exc_tb (traceback, optional): Traceback da exceção, se houver.
        """
        self.session.close()
