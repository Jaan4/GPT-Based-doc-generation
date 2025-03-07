import os
import streamlit as st
import ollama
from typing import Dict, Any
import logging
import traceback# document_generator.py
import ollama
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self, model_name: str = 'deepseek-r1:1.5b'):
        self.model_name = model_name
    
    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        """
        Generate comprehensive documentation using the LLM model.
        
        Args:
            code (str): Source code
            analysis (Dict): Code analysis results
            
        Returns:
            str: Generated documentation
        """
        try:
            prompt = self._create_prompt(code, analysis)
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return "Error generating documentation. Please try again."
    
    def _create_prompt(self, code: str, analysis: Dict[str, Any]) -> str:
        return f"""
        Generate comprehensive documentation for the following Python code.
        Include:
        - Overview
        - Functions: {', '.join(analysis.get('functions', []))}
        - Classes: {', '.join(analysis.get('classes', []))}
        - Dependencies: {', '.join(analysis.get('relationships', {}).get('imports', []))}
        
        Code:
        {code}
        
        Please provide detailed documentation with examples and usage patterns.
        """

logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self, model_name: str = 'deepseek-r1:1.5b'):
        self.model_name = model_name
    
    def generate_documentation(self, code: str, analysis: Dict[str, Any]) -> str:
        # Retrieve the API token from environment variables or Streamlit secrets
        token = os.getenv("OLLAMA_API_TOKEN") or st.secrets.ollama.api_token

        try:
            prompt = self._create_prompt(code, analysis)
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            # Check if the response has the expected format
            if 'message' in response and 'content' in response['message']:
                return response['message']['content']
            else:
                logger.error("Unexpected response format: %s", response)
                st.error("Unexpected response format received from the API.")
                return "Error generating documentation. Please try again."
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Error generating documentation: {error_details}")
            st.error(f"Error generating documentation:\n{error_details}")
            return "Error generating documentation. Please try again."
    
    def _create_prompt(self, code: str, analysis: Dict[str, Any]) -> str:
        return f"""
        Generate comprehensive documentation for the following Python code.
        Include:
        - Overview
        - Functions: {', '.join(analysis.get('functions', []))}
        - Classes: {', '.join(analysis.get('classes', []))}
        - Dependencies: {', '.join(analysis.get('relationships', {}).get('imports', []))}
        
        Code:
        {code}
        
        Please provide detailed documentation with examples and usage patterns.
        """
