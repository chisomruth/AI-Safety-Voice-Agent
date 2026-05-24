import os
import vertexai 
from dotenv import load_dotenv

load_dotenv()


class LLMFactory:
    """
    Manages Google Generative AI configuration and model instantiation.
    """

    def __init__(self):
        """
        Initializes the factory by loading environment variables and configuring the API.
        
        :param self: The instance of the LLMFactory class.
        """
        self._location = os.getenv('PROJECT_LOCATION')
        self._project_id = os.getenv('PROJECT_ID')

        self._validate_config()
        self._initialize_api()


    def _validate_config(self):
        """Ensures all required environment variables are present."""
        if not self._project_id:
            raise EnvironmentError("Missing 'PROJECT_ID' in environment variables.")
        if not self._location:
            raise EnvironmentError("Missing 'PROJECT_LOCATION' in environment variables.")
        

    def _initialize_api(self):
        """Configures the Google AI SDK."""
        try:
            vertexai.init(project=self._project_id, location=self._location)
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Vertex AI: {e}")
        