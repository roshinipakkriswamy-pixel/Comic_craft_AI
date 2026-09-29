from app.schemas import (
    OutlineResponse,
    StoryResponse,
    ComicPanel
)


def build_comic_layout(
    outline: OutlineResponse,
    story: StoryResponse,
    image_urls: list[str]
) -> list[ComicPanel]:

    stories = {
        panel.panel_number: panel
        for panel in story.panels
    }

    result = []

    for outline_panel, image_url in zip(
        outline.panels,
        image_urls
    ):

        story_panel = stories[
            outline_panel.panel_number
        ]

        result.append(

            ComicPanel(

                panel_number=(
                    outline_panel.panel_number
                ),

                title=(
                    outline_panel.title
                ),

                scene_description=(
                    outline_panel.scene_description
                ),

                image_prompt=(
                    outline_panel.image_prompt
                ),

                image_url=image_url,

                caption=(
                    story_panel.caption
                ),

                narration=(
                    story_panel.narration
                ),

                dialogue=(
                    story_panel.dialogue
                )
            )
        )

    return result