def read_file(file):
    with open(file, "rb") as in_file:
        return in_file.read()


def merge_files(outer_file, inner_file):
    return outer_file + inner_file


def save_merged_file(data, filename):
    with open(filename, "wb") as out_file:
        out_file.write(data)


def merge_file(outer_file, inner_file):
    return merge_files(outer_file, inner_file)
