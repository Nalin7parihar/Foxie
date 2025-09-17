from google import genai
from dotenv import load_dotenv
import os


class LLMService:
  def __init__(self):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    self.client = genai.Client(api_key=api_key)
    
    if not self.client:
      raise ValueError("Failed to initialize Gemini client. Check your API key.")
    
  def generate_docstring(self, code : str,type:str) ->str:
    prompt=f"""You are an expert Python programmer specializing in writing documentation.
    Generate a concise, {type}-style docstring for the following Python code. 
    Only return the docstring itself, with no other explanation or text.
    ---CODE START---
    {code}
    ---CODE END---
    """
    try:
      response=self.client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt                                      
      )
      return response.text
    
    except Exception as e:
      print("Error calling Gemini API:",e)
      raise
    
llm_service = LLMService()