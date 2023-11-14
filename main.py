from itertools import cycle
from math import sqrt
from pathlib import Path
from random import randint
from uuid import uuid4

from PIL import Image

PHOTOS_DIR = Path("fotos")

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
MAIN_PHOTO_WIDTH = int((IMAGE_WIDTH / 3) * 2)
MAIN_PHOTO_HEIGHT = int((IMAGE_HEIGHT / 3) * 2)
MAIN_PHOTO_FILENAME = "main.png"


def get_total_avatars():
    return len(list(PHOTOS_DIR.iterdir()))


def avatar_final_size(total_avatars):
    total_pixels = (
        IMAGE_WIDTH * IMAGE_HEIGHT - MAIN_PHOTO_WIDTH * MAIN_PHOTO_HEIGHT
    ) / total_avatars

    # only square avatars allowed
    return int(sqrt(total_pixels))


def avatars_iter(size):
    PHOTOS_DIR = Path("fotos")
    photos = [
        photo for photo in PHOTOS_DIR.iterdir() if photo.name.endswith("png")
    ]
    for photo in cycle(photos):
        image = Image.open(photo).resize((size, size))
        yield image


def build(image, avatars, avatar_size, x0, x1, y0, y1):
    print(f"x = ({x0}, {x1})")
    print(f"y = ({y0}, {y1})")
    for x in range(int(x0), int(x1)):
        for y in range(int(y0), int(y1)):
            avatar = next(avatars)
            image.paste(avatar, (x * avatar_size, y * avatar_size))
    return image


def generate_photo():
    final_photo_width = IMAGE_WIDTH
    final_photo_height = IMAGE_HEIGHT

    photo_width = MAIN_PHOTO_WIDTH
    photo_height = MAIN_PHOTO_HEIGHT

    padding_width = (final_photo_width - photo_width) / 2
    padding_height = (final_photo_height - photo_height) / 2

    total_avatars = get_total_avatars()
    avatar_size = avatar_final_size(total_avatars)
    avatars = avatars_iter(avatar_size)

    x0_remainder = 0
    x1_remainder = 0
    y0_remainder = 0
    y1_remainder = 0

    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))

    # TOP
    tx0 = 0
    tx1 = final_photo_width // avatar_size
    ty0 = 0
    ty1 = padding_height // avatar_size
    y0_reminder = padding_height % avatar_size
    print("top")
    image = build(image, avatars, avatar_size, tx0, tx1, ty0, ty1)
    # BOTTOM
    bx0 = 0
    bx1 = final_photo_width // avatar_size
    by0 = (padding_height + photo_height) // avatar_size
    y1_reminder = (padding_height + photo_height) % avatar_size
    by1 = final_photo_height // avatar_size
    print("bottom")
    image = build(image, avatars, avatar_size, bx0, bx1, by0, by1)
    # LEFT
    lx0 = 0
    lx1 = padding_width // avatar_size
    x0_remainder = padding_width % avatar_size
    ly0 = padding_height // avatar_size
    ly1 = (padding_height + final_photo_height) // avatar_size
    print("left")
    image = build(image, avatars, avatar_size, lx0, lx1, ly0, ly1)
    # RIGHT
    rx0 = (padding_width + photo_width) // avatar_size
    rx1 = final_photo_width // avatar_size
    x1_remainder = final_photo_width % avatar_size
    ry0 = padding_height // avatar_size
    ry1 = (padding_height + final_photo_height) // avatar_size
    print("right")
    image = build(image, avatars, avatar_size, rx0, rx1, ry0, ry1)

    main_x0 = (padding_width - x0_remainder)
    main_x1 = (photo_width + padding_width - x1_remainder)
    main_y0 = (padding_height - y0_remainder)
    main_y1 = (photo_height + padding_height - y1_remainder)

    main = Image.open(MAIN_PHOTO_FILENAME).resize((
        int(rx0 - lx1) * avatar_size,
        int(by0 - ty1) * avatar_size,
    ))
    image.paste(main, (int(lx1) * avatar_size, int(ty1) * avatar_size))


    with Path("photo.png").open(mode="wb") as fp:
        image.save(fp)

    # Top
    # x = 0, IMAGE_WIDTH
    # y = 0, available_width / 2
    # Right
    # x = available_width / 2 + MAIN_PHOTO_WIDTH, IMAGE_WIDTH
    # y = available_height / 2, available_height / 2 + MAIN_PHOTO_HEIGHT
    # Left
    # x = 0, available_width / 2
    # y = available_height / 2, available_height / 2 + MAIN_PHOTO_HEIGHT

    # 0, IMAGE_HEIGHT - MAIN_PHOTO_HEIGHT / 2


def generate_avatar(width=512, height=512, rgb=None):
    if not rgb:
        rgb = (
            randint(0, 256),
            randint(0, 256),
            randint(0, 256),
        )
    image = Image.new("RGB", (width, height))
    for i in range(width):
        for j in range(height):
            image.im.putpixel((i, j), rgb)

    return image


def generate_main_photo():
    image = generate_avatar(
        width=MAIN_PHOTO_WIDTH,
        height=MAIN_PHOTO_HEIGHT,
        rgb=(255, 255, 255),
    )
    file = Path(MAIN_PHOTO_FILENAME)
    with file.open(mode="wb") as fp:
        image.save(fp)


def generate_random_avatars():
    total = 1000
    for i in range(total):
        name = str(uuid4())[:4]
        image = generate_avatar()
        file = PHOTOS_DIR / f"{name}.png"
        with file.open(mode="wb") as fp:
            image.save(fp)


if __name__ == "__main__":
    # generate_main_photo()
    # generate_random_avatars()
    generate_photo()
