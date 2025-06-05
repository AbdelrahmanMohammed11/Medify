from .LLMEnums import LLMEnums
from .provider import OpenAIProvider , CoHereProvider

class LLMProviderFactory:
    def __init__(self, config:dict):
        """
        Initializes the LLMProviderFactory with the given configuration.
        
        :param config: Configuration object containing LLM provider settings.
        """
        self.config = config

    def get_provider(self, provider:str):
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_URL,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_OUTPUT_TOKENS,
                default_generation_temperature= self.config.GENERATION_DEFAULT_TEMPERATURE,
                default_input_max_characters=self.config.INPUT_DEFUALT_MAX_CHARACTERS
                
            )
        
        
        if provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_OUTPUT_TOKENS,
                default_generation_temperature= self.config.GENERATION_DEFAULT_TEMPERATURE,
                default_input_max_characters=self.config.INPUT_DEFUALT_MAX_CHARACTERS
            )
        
        return None
        