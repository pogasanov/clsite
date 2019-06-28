import json


def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
        return data


def get_all_tags_tuple(file_path='app/profiles/tags/law-type-tags.json'):
    tags_dict = read_json(file_path)
    result_list = []
    for area in tags_dict:
        if area.get("subareas") != None:
            subarea_list = area.pop("subareas")
            area_tuple = (area['name'], tuple([tuple(subarea.values()) for subarea in subarea_list]))
            result_list.append(area_tuple)
    return tuple(result_list)


def get_subareas_by_area(area_id, file_path='app/profiles/tags/law-type-tags.json'):
    tags_dict = read_json(file_path)
    for area in tags_dict:
        if area['id'] == area_id:
            return area['subareas']
    return None
