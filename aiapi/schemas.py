# aiapi/schemas.py
from pydantic import BaseModel, Field

class Question(BaseModel):
    question_text: str = Field(description="The multiple choice question text")
    options: list[str] = Field(description="Exactly 4 possible answers")
    correct_answer: str = Field(description="The exact text of the correct option")
    explanation: str = Field(description="A short explanation of why this is the answer")

class Quiz(BaseModel):
    questions: list[Question] = Field(description="List of quiz questions")