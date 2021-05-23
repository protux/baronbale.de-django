from PIL import Image

COLOR_MODE = "RGB"
MAX_ALLOWED_DIFF = 50


def compare_images(image_data_1, image_data_2):
    image_1, image_2 = load_images(image_data_1, image_data_2)
    image_1, image_2 = resize_images(image_1, image_2)
    image_1, image_2 = convert_color(image_1, image_2)
    diff_image = get_diff(image_1, image_2)
    diff_image.show()
    # save_diff(diff_image)


def save_diff(diff_image):
    image_to_save = Image.new(COLOR_MODE, diff_image.size, (255, 255, 255))
    image_to_save.paste(diff_image, (diff_image.size[0], diff_image.size[1], 100))
    image_to_save.save("/home/nico/diff.jpg", "JPEG")


def get_diff(image_1, image_2):
    pixels = image_1.load()
    for x in range(0, image_1.size[0]):
        for y in range(0, image_1.size[1]):
            r_1, g_1, b_1 = image_1.getpixel((x, y))
            r_2, g_2, b_2 = image_2.getpixel((x, y))
            if (
                abs(r_1 - r_2) > MAX_ALLOWED_DIFF
                or abs(g_1 - g_2) > MAX_ALLOWED_DIFF
                or abs(b_1 - b_2) > MAX_ALLOWED_DIFF
            ):
                pixels[x, y] = max(r_1 + 20, 255), g_1, b_1

    return image_1


def load_images(image_data_1, image_data_2):
    image_1 = Image.open(image_data_1)
    image_2 = Image.open(image_data_2)

    return image_1, image_2


def convert_color(image_1, image_2):
    return image_1.convert(COLOR_MODE), image_2.convert(COLOR_MODE)


def resize_images(image_1, image_2):
    size_1 = image_1.size
    size_2 = image_2.size

    if size_1[0] > size_2[0] or size_1[1] > size_2[1]:
        return image_1.resize(size_2, Image.ANTIALIAS), image_2
    elif size_2[0] > size_1[0] or size_2[1] > size_1[1]:
        return image_1, image_2.resize(size_1, Image.ANTIALIAS)


if __name__ == "__main__":
    from sys import argv

    compare_images(argv[1], argv[2])
