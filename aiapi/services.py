import os
from google import genai
from google.genai import types

class ApiServices:
    def __init__(self):
        self.client=genai.Client()
        self.model = 'gemeni-2.5-flash'
    def textQuery(self, prompt:str)-> str:
        try:
            reponse = self.content.models.generate_content(
                model = self.default_model,
                contents = prompt,
            )
            return response.text
        except Exception as e:
            return f"Error {e}"
        
    def generate_quiz(self, topic: str, num_questions: int, difficulty: int) -> dict | None:
        prompt = (
        f"Generate a {num_questions}-question multiple choice quiz about '{topic}'. "
        f"The difficulty level should be {difficulty} out of 10. "
        "Ensure the questions are accurate and the correct answer is always included in the options."
        )

        try:
            response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=Quiz,
                temperature=0.7,
            ),
        )
        # Use the parsed dataclass directly
            # 1. Parse the string response into our Pydantic validation model
            validated_quiz = Quiz.model_validate_json(response.text)
            
            # 2. CRITICAL FIX: Convert the Pydantic object tree into standard primitive dicts/lists
            # (If you are using an older version of Pydantic, use validated_quiz.dict() instead)
            return validated_quiz.model_dump()  # This is a Quiz object
        except Exception as e:
            return {"error": f"Error generating quiz: {e}"}