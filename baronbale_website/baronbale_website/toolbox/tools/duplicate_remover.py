# /bin/python
import re


def __split_items(text):
    regex = re.compile(r"[^a-zA-Z0-9]+")
    return regex.split(text.strip())


def clear_duplicates(items, old_items):
    checked = set()
    unique = []
    duplicates = []

    items = __remove_comments_and_empty_lines(items)
    items = __split_items(items)
    old_items = __remove_comments_and_empty_lines(old_items)
    old_items = __split_items(old_items)

    for item in items:
        if item not in checked and item not in old_items:
            unique.append(item)
            checked.add(item)
        else:
            duplicates.append(item)

    return __build_output_dict(unique, duplicates)


def __build_output_dict(uniques, duplicates):
    output = dict()
    output["duplicate_count"] = len(duplicates)
    output["duplicate_items"] = duplicates
    output["unique_count"] = len(uniques)
    output["unique_items"] = uniques
    return output


def __remove_comments_and_empty_lines(text):
    lines = text.split("\n")
    new = []
    for line in lines:
        comment_index = line.find("#")
        if comment_index > -1:
            line = line[:comment_index].strip()
        if len(line) > 0:
            new += [line]

    return "\n".join(new)
