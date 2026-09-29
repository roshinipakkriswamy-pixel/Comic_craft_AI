from app.config import get_settings

from app.schemas import (
    OutlineResponse,
    PromptRequest,
    StoryResponse
)


def generate_story(
    request: PromptRequest,
    outline: OutlineResponse
) -> StoryResponse:

    settings = get_settings()

    if not settings.gemini_api_key:
        return fallback_story(
            request,
            outline
        )

    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    outline_text = "\n".join(

        f"""
Panel {panel.panel_number}

Title:
{panel.title}

Scene:
{panel.scene_description}
"""

        for panel in outline.panels
    )

    prompt = f"""
Write the narration and dialogue for a five-panel comic.

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Original story:
{request.story_prompt}

Outline:
{outline_text}

Requirements:

1. Return exactly five panels.
2. Match the outline panel numbers.
3. Each panel needs:
   - caption
   - narration
   - dialogue
4. Keep character continuity.
5. Keep story continuity.
6. Dialogue should be short and natural.
7. Narration should feel like a comic book.
8. Captions should describe the environment.
9. Do not create extra panels.
"""

    response = client.models.generate_content(

        model=settings.gemini_story_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=StoryResponse,

            temperature=0.9
        )
    )

    return StoryResponse.model_validate_json(
        response.text
    )


def fallback_story(
    request: PromptRequest,
    outline: OutlineResponse
) -> StoryResponse:

    panels = []

    for panel in outline.panels:

        if panel.panel_number < 5:

            dialogue = (
                f"{request.character_name}: "
                "We keep moving! "
                "The next clue is waiting!"
            )

        else:

            dialogue = (
                f"{request.character_name}: "
                "Every adventure begins "
                "with one brave step!"
            )

        panels.append(

            {
                "panel_number": panel.panel_number,

                "caption": (
                    f"{request.setting} — "
                    f"{request.tone}"
                ),

                "narration": (
                    panel.scene_description
                ),

                "dialogue": dialogue
            }
        )

    return StoryResponse(
        panels=panels
    )