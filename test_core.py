import os


os.environ.setdefault(
    "IMAGE_PROVIDER",
    "placeholder"
)

os.environ.setdefault(
    "GEMINI_API_KEY",
    ""
)


from fastapi.testclient import (
    TestClient
)

from app.main import app

from app.services.gemini_flash import (
    generate_outline
)

from app.services.gemini_pro import (
    generate_story
)

from app.schemas import (
    PromptRequest
)


client = TestClient(app)


def sample_request():

    return PromptRequest(

        story_prompt=(
            "A brave fox discovers "
            "a glowing door in an "
            "enchanted forest."
        ),

        character_name="Milo",

        setting="Enchanted forest",

        tone="Funny",

        art_style="Comic book"
    )


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()[
        "status"
    ] == "ok"


def test_outline_and_story_fallback():

    request = sample_request()

    outline = generate_outline(
        request
    )

    assert len(
        outline.panels
    ) == 5


    story = generate_story(
        request,
        outline
    )

    assert len(
        story.panels
    ) == 5


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in (
        response.text
    )


def test_full_generation_in_demo_mode():

    response = client.post(

        "/generate-comic/json",

        json=sample_request().model_dump()
    )

    assert response.status_code == 200

    data = response.json()

    assert len(
        data["panels"]
    ) == 5

    assert data[
        "pdf_url"
    ].endswith(".pdf")