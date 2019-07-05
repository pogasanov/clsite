import json
import os
from clsite.settings import BASE_DIR


def read_json(path):
    """
    Reads a json file and returns the results.
    """
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
        return data


def get_all_tags_tuple(file_path=None):
    """
    Returns all the subjective tags present in subjective-tags-ontology.json
    file in the form of choices readable tuple.
    """
    if not file_path:
        path = 'profiles/subjectivetags/subjective-tags.json'
        file_path = os.path.join(BASE_DIR, path)

    tags_dict = read_json(file_path)
    result_list = []
    for area in tags_dict:
        area_tuple = area['name'], area['name']
        result_list.append(area_tuple)
    return tuple(result_list)


SUBJECTIVE_TAGS_CHOICES = get_all_tags_tuple()
