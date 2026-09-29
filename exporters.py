from pathlib import Path
from uuid import uuid4
import unicodedata

from fpdf import FPDF

from app.config import get_settings
from app.schemas import ComicPanel


def _pdf_text(value: str) -> str:

    value = unicodedata.normalize(
        "NFKD",
        value
    )

    return (
        value
        .encode(
            "latin-1",
            "replace"
        )
        .decode("latin-1")
    )


def save_pdf(
    panels: list[ComicPanel]
) -> tuple[str, str]:

    settings = get_settings()

    export_directory = (
        settings.output_dir / "exports"
    )

    export_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    export_id = uuid4().hex

    filename = (
        f"comic-{export_id}.pdf"
    )

    output_path = (
        export_directory / filename
    )

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in panels:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.multi_cell(
            180,
            10,
            (
                f"Panel {panel.panel_number}: "
                f"{_pdf_text(panel.title)}"
            )
        )

        image_path = (
            settings.output_dir.parent
            / panel.image_url.lstrip("/")
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=35,
                w=180,
                h=105
            )

        pdf.set_y(148)

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        pdf.multi_cell(
            180,
            6,
            _pdf_text(
                panel.scene_description
            )
        )

        pdf.ln(3)

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        pdf.multi_cell(
            180,
            7,
            (
                "Caption: "
                + _pdf_text(panel.caption)
            )
        )

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        pdf.multi_cell(
            180,
            7,
            (
                "Narration: "
                + _pdf_text(panel.narration)
            )
        )

        if panel.dialogue:

            pdf.multi_cell(
                180,
                7,
                (
                    "Dialogue: "
                    + _pdf_text(
                        panel.dialogue
                    )
                )
            )

    pdf.output(
        str(output_path)
    )

    return (
        export_id,
        f"/static/exports/{filename}"
    )