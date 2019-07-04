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


def get_all_tags_tuple(file_path= os.path.join(BASE_DIR, 'profiles/lawtypetags/law-type-tags-ontology.json')):
    """
    Returns all the law type tags present in law-type-tags-ontology.json file in the form of choices readable tuple.
    """
    tags_dict = read_json(file_path)
    result_list = []
    for area in tags_dict:
        if area.get("subareas") != None:
            subarea_list = area.pop("subareas")
            subarea_names_list = []
            for subarea in subarea_list:
                subarea_names_list.append((subarea['name'], subarea['name']))
                # throw value error if ontology exceeds two levels
                if subarea.get('subareas'):
                    raise ValueError("Only two levels are allowed in law-tag-type-ontology.json")

            area_tuple = (area['name'], tuple(subarea_names_list))
            result_list.append(area_tuple)
    return tuple(result_list)


def get_all_tags_flat_list(tags_tuple=[]):
    flat_tags_list = []
    for area in tags_tuple:
        flat_tags_list.extend([subarea[0 ]for subarea in area[1]])
    return flat_tags_list


LAW_TYPE_TAGS_CHOICES = get_all_tags_tuple()
