from app.config import get_settings
from app.schemas import (
    OutlineResponse,
    PromptRequest
)


def generate_outline(
    request: PromptRequest
) -> OutlineResponse:

    settings = get_settings()

    # Demo/fallback mode
    if not settings.gemini_api_key:
        return fallback_outline(request)

    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a cohesive five-panel comic outline.

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Requirements:

1. Create exactly 5 panels.
2. Number panels from 1 to 5.
3. Maintain character consistency.
4. Maintain setting consistency.
5. Give each panel a short title.
6. Give each panel a scene description.
7. Give each panel a detailed image-generation prompt.
8. Image prompts should include:
   - subject
   - action
   - composition
   - lighting
   - mood
   - art style
9. Do not include dialogue inside image prompts.
"""

    response = client.models.generate_content(

        model=settings.gemini_outline_model,

        contents=prompt,

        config=types.GenerateContentConfig(

            response_mime_type="application/json",

            response_schema=OutlineResponse,

            temperature=0.9
        )
    )

    return OutlineResponse.model_validate_json(
        response.text
    )


def fallback_outline(
    request: PromptRequest
) -> OutlineResponse:

    panels = [

        (
            "The Beginning",
            (
                f"{request.character_name} arrives in "
                f"{request.setting}, ready to face the mystery "
                f"hidden inside the story."
            ),
            "wide cinematic establishing shot"
        ),

        (
            "The Discovery",
            (
                f"{request.character_name} discovers the first "
                f"important clue connected to "
                f"{request.story_prompt}."
            ),
            "medium shot showing a mysterious discovery"
        ),

        (
            "The Challenge",
            (
                f"A difficult obstacle appears and tests "
                f"{request.character_name}."
            ),
            "dynamic action scene"
        ),

        (
            "The Turning Point",
            (
                f"{request.character_name} discovers a clever "
                f"way forward and changes the direction of "
                f"the adventure."
            ),
            "dramatic close-up with cinematic lighting"
        ),

        (
            "The New Dawn",
            (
                f"The adventure reaches a satisfying ending "
                f"while leaving a memorable final image."
            ),
            "heroic final wide shot"
        )
    ]

    result = []

    for index, (
        title,
        description,
        camera
    ) in enumerate(panels, start=1):

        image_prompt = (
            f"{request.character_name}, "
            f"{description}, "
            f"{camera}, "
            f"{request.art_style} comic illustration, "
            f"{request.tone} mood, "
            f"consistent character design, "
            f"cinematic lighting, "
            f"high detail, "
            f"clean composition"
        )

        result.append(
            {
                "panel_number": index,
                "title": title,
                "scene_description": description,
                "image_prompt": image_prompt
            }
        )

    return OutlineResponse(
        panels=result
    )