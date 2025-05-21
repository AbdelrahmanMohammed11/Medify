from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    """
    Base controller class to be inherited by all controllers.
    This class provides access to the application settings.
    """

    def __init__(self):
        self.app_settings: Settings = get_settings()

        # Get the base directory of the application
        
        self.base_directory = os.path.dirname(os.path.abspath("."))
        self.file_directory = os.path.join(self.base_directory,
                                            "src/assets/files")
        

    def generate_random_string(self, length: int = 10):
        """
        Generate a random string of fixed length.
        :param length: Length of the random string to be generated.
        :return: Random string of fixed length.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k = length))
