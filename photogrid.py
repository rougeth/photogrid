import math
from pathlib import Path
from itertools import cycle

import click
from PIL import Image
from rich.progress import BarColumn, Progress, TimeRemainingColumn


def create_image(tiles, output, width, height):
    tile_size = round(math.sqrt((width * height) / len(tiles)))

    vertical_tiles = round(width / tile_size)
    horizontal_tiles = round(height / tile_size)

    final_image_width = horizontal_tiles * tile_size
    final_image_height = vertical_tiles * tile_size

    final_image = Image.new("RGB", (final_image_width, final_image_height))

    tiles = cycle(tiles)
    progress = Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.total]{task.completed}/{task.total}",
        TimeRemainingColumn(),
    )

    with progress:
        task = progress.add_task(
            "Rendering image", total=horizontal_tiles * vertical_tiles
        )

        for x in range(0, horizontal_tiles):
            for y in range(0, vertical_tiles):
                tile = next(tiles)
                tile = Image.open(tile)
                tile = tile.resize((tile_size, tile_size), Image.ANTIALIAS)
                final_image.paste(tile, (x * tile_size, y * tile_size))
                progress.update(task, advance=1)

    final_image.save(output)


@click.command()
@click.argument(
    "output",
    type=click.Path(dir_okay=False, exists=False),
    required=True,
)
@click.option(
    "-p",
    "--path",
    type=click.Path(file_okay=False, exists=True, path_type=Path),
    required=True,
    help="Folder with images to be used to create the grid",
)
@click.option(
    "-w", "--width", type=int, required=True, help="Approximate width of final image"
)
@click.option(
    "-h", "--height", type=int, required=True, help="Approximate height of final image"
)
def cli(height, width, path, output):
    photos = list(path.iterdir())
    create_image(photos, output, width, height)


if __name__ == "__main__":
    cli()
