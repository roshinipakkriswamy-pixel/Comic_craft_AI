from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from app.config import get_settings

from app.schemas import (
    PromptRequest
)

from app.services.gemini_flash import generate_outline

from app.services.gemini_pro import (
    generate_story
)

from app.services.image_generator import (
    generate_image
)

from app.services.layout_builder import (
    build_comic_layout
)

from app.services.exporters import (
    save_pdf
)


router = APIRouter()


templates = Jinja2Templates(

    directory=str(
        Path(__file__).resolve()
        .parent.parent
        / "templates"
    )
)


def _make_request(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
) -> PromptRequest:

    try:

        return PromptRequest(

            story_prompt=story_prompt,

            character_name=character_name,

            setting=setting,

            tone=tone,

            art_style=art_style
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        ) from exc


def generate_comic(
    request_data: PromptRequest
):

    # 1. Generate five-panel outline
    outline = generate_outline(
        request_data
    )

    # 2. Generate narration/dialogue
    story = generate_story(
        request_data,
        outline
    )

    # 3. Generate image for every panel
    image_urls = []

    for panel in outline.panels:

        image_url = generate_image(
            panel.image_prompt,
            panel.panel_number
        )

        image_urls.append(
            image_url
        )

    # 4. Build final layout
    layout = build_comic_layout(
        outline,
        story,
        image_urls
    )

    # 5. Export PDF
    export_id, pdf_url = save_pdf(
        layout
    )

    return (
        layout,
        export_id,
        pdf_url
    )


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={
            "title": "ComicCraft"
        }
    )


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    data = _make_request(

        story_prompt,

        character_name,

        setting,

        tone,

        art_style
    )

    try:

        layout, export_id, pdf_url = (
            generate_comic(data)
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={
                "title": "ComicCraft",

                "error": (
                    "Comic generation failed: "
                    f"{exc}"
                )
            },

            status_code=500
        )

    return templates.TemplateResponse(

        request=request,

        name="comic_preview.html",

        context={

            "title": "Your Comic",

            "layout": layout,

            "export_id": export_id,

            "pdf_url": pdf_url,

            "request_data": data
        }
    )


@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(
    payload: PromptRequest
):

    try:

        layout, export_id, pdf_url = (
            generate_comic(payload)
        )

        return JSONResponse(

            {
                "export_id": export_id,

                "pdf_url": pdf_url,

                "panels": [
                    panel.model_dump()
                    for panel in layout
                ]
            }
        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                "Comic generation failed: "
                f"{exc}"
            )

        ) from exc


@router.post(
    "/test-image"
)
async def test_image(
    prompt: str = Form(...)
):

    if not prompt.strip():

        raise HTTPException(
            status_code=422,
            detail="Prompt is required"
        )

    try:

        image_url = generate_image(
            prompt.strip(),
            0
        )

        return {
            "image_url": image_url
        }

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=(
                "Image generation failed: "
                f"{exc}"
            )

        ) from exc


@router.get(
    "/download/{export_id}"
)
async def download(
    export_id: str
):

    if (
        not export_id.isalnum()
        or len(export_id) != 32
    ):

        raise HTTPException(
            status_code=404,
            detail="Export not found"
        )

    path = (
        get_settings().output_dir
        / "exports"
        / f"comic-{export_id}.pdf"
    )

    if not path.exists():

        raise HTTPException(
            status_code=404,
            detail="Export not found"
        )

    return FileResponse(

        path,

        media_type="application/pdf",

        filename=path.name
    )


@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(
    request: Request
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={
            "title": "Export Complete"
        }
    )