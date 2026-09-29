
from pydantic import BaseModel
from typing import List, Optional


class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


class OutlineResponse(BaseModel):
    outline: str


class StoryResponse(BaseModel):
    story: str


class ComicPanel(BaseModel):
    panel_number: int
    description: str
    dialogue: Optional[str] = None
    narration: Optional[str] = None
    image_prompt: Optional[str] = None


class ComicResponse(BaseModel):
    title: str
    panels: List[ComicPanel]
