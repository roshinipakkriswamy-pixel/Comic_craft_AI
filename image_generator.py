from pathlib import Path
import re
from uuid import uuid4

from PIL import Image, ImageDraw

from app.config import get_settings


_PIPELINE = None


def _safe_name(text: str) -> str:

    clean = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "-",
        text
    )

    clean = clean.strip("-").lower()

    return clean[:50] or "panel"


def generate_image(
    prompt: str,
    panel_number: int
) -> str:

    settings = get_settings()

    output_directory = (
        settings.output_dir / "panels"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"panel-{panel_number}-"
        f"{_safe_name(prompt)}-"
        f"{uuid4().hex[:8]}.png"
    )

    path = output_directory / filename

    if settings.image_provider.lower() == "diffusers":

        _generate_diffusers(
            prompt,
            path
        )

    else:

        _generate_placeholder(
            prompt,
            panel_number,
            path,
            settings.image_width,
            settings.image_height
        )

    return (
        f"/static/panels/{filename}"
    )


def _generate_placeholder(
    prompt: str,
    panel_number: int,
    path: Path,
    width: int,
    height: int
) -> None:

    image = Image.new(
        "RGB",
        (width, height),
        "#f7efe2"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        (
            10,
            10,
            width - 10,
            height - 10
        ),
        outline="#222222",
        width=5
    )

    draw.text(
        (30, 35),
        f"PANEL {panel_number}",
        fill="#222222"
    )

    wrapped_text = prompt[:220]

    y = height // 2 - 40

    lines = [
        wrapped_text[i:i + 42]
        for i in range(
            0,
            len(wrapped_text),
            42
        )
    ]

    for line in lines[:6]:

        draw.text(
            (30, y),
            line,
            fill="#333333"
        )

        y += 28

    draw.text(
        (30, height - 55),
        "ComicCraft demo image",
        fill="#555555"
    )

    image.save(
        path,
        "PNG"
    )


def _generate_diffusers(
    prompt: str,
    path: Path
) -> None:

    global _PIPELINE

    import torch

    from diffusers import (
        AutoPipelineForText2Image
    )

    settings = get_settings()

    if _PIPELINE is None:

        dtype = (
            torch.float16
            if torch.cuda.is_available()
            else torch.float32
        )

        kwargs = {
            "torch_dtype": dtype,
            "use_safetensors": True
        }

        if settings.hf_token:

            kwargs["token"] = (
                settings.hf_token
            )

        _PIPELINE = (
            AutoPipelineForText2Image
            .from_pretrained(
                settings.image_model_id,
                **kwargs
            )
        )

        if torch.cuda.is_available():

            _PIPELINE = _PIPELINE.to(
                "cuda"
            )

        else:

            _PIPELINE = _PIPELINE.to(
                "cpu"
            )

    negative_prompt = (
        "blurry, distorted face, "
        "extra limbs, text, watermark, "
        "low quality, deformed"
    )

    result = _PIPELINE(

        prompt=prompt,

        negative_prompt=negative_prompt,

        num_inference_steps=(
            settings.image_steps
        ),

        width=settings.image_width,

        height=settings.image_height
    )

    result.images[0].save(
        path
    )