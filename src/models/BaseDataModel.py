from helpers.config import get_settings , Settings

class BaseDataModel:
    def __init__(self, db_clint: object ):
        self.app_settings = get_settings()
        self.database_client = db_clint