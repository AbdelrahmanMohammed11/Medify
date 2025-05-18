from helpers.config import get_settings, Settings

class BaseController:
    """
    Base controller class to be inherited by all controllers.
    This class provides access to the application settings.
    """

    def __init__(self):
        self.app_settings: Settings = get_settings()