import json


def read_json(path):
    """
    Reads a json file and returns the results.
    """
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
        return data


def get_all_tags_tuple(file_path='app/profiles/lawtypetags/law-type-tags-ontology.json'):
    """
    Returns all the tags present in json file in the form of model choices readable tuple.
    """
    tags_dict = read_json(file_path)
    result_list = []
    for area in tags_dict:
        if area.get("subareas") != None:
            subarea_list = area.pop("subareas")  #only extracts two levels of ontology
            area_tuple = (area['name'], tuple([(subarea['name'], subarea['name']) for subarea in subarea_list]))
            result_list.append(area_tuple)
    return tuple(result_list)


LAW_TYPE_TAGS_CHOICES = get_all_tags_tuple()
