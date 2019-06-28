import json
import argparse


def read_json(path):
    """
    Reads a json file and returns the results.
    """
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
        return data


def get_all_tags_tuple(file_path='app/profiles/tags/law-type-tags.json'):
    """
    Returns all the tags present in json file in the form of model choices readable tuple.
    """
    tags_dict = read_json(file_path)
    result_list = []
    for area in tags_dict:
        if area.get("subareas") != None:
            subarea_list = area.pop("subareas")
            area_tuple = (area['name'], tuple([tuple(subarea.values()) for subarea in subarea_list]))
            result_list.append(area_tuple)
    return tuple(result_list)


def get_subareas_by_area(area_id, file_path='app/profiles/tags/law-type-tags.json'):
    """
    Returns all the subareas of a specific area_id
    """
    tags_dict = read_json(file_path)
    for area in tags_dict:
        if area['id'] == area_id:
            return area['subareas']
    return None


def get_latest_subarea_id(file_path='app/profiles/tags/law-type-tags.json'):
    """
    Returns the id of last subarea
    """
    tags_dict = read_json(file_path)
    for area in reversed(tags_dict):
        if area['subareas']:
            return area['subareas'][-1]['id']
    return 0


def add_area(area_name, file_path='app/profiles/tags/law-type-tags.json'):
    """
    Adds a given area to the json file.
    """
    tags_dict = read_json(file_path)
    new_area = {
        'id': tags_dict[-1]['id'] + 1 if tags_dict else 0,
        'name': area_name,
        'subareas': []
    }
    tags_dict.append(new_area)
    with open(file_path, 'w') as tag_file:
        json.dump(tags_dict, tag_file, indent=2)
        tag_file.close()


def add_subarea(subarea_name, parent_id, file_path='app/profiles/tags/law-type-tags.json'):
    """
    Adds a given subarea to the json file under that specific area id
    """
    tags_dict = read_json(file_path)
    for area in tags_dict:
        if area['id'] == parent_id:
            area['subareas'].append({
                'id': get_latest_subarea_id() + 1,
                'name': subarea_name,
            })
            with open(file_path, 'w') as tag_file:
                json.dump(tags_dict, tag_file, indent=2)
                tag_file.close()

            return True
    return False


if __name__=='__main__':
    parser = argparse.ArgumentParser("law_type_tags")
    parser.add_argument('--operation', choices=['add-area', 'add-subarea'], type=str, help="Name of Operation.")
    parser.add_argument('--name', type=str, help="Name of Area or SubArea you want to add.")
    parser.add_argument('--parent', type=int, help="Id of parent Area.")
    args = parser.parse_args()
    if args.operation == "add-area":
        if not args.name:
            print("Please add a value for Area Name(--name).")
        else:
            success = add_area(args.name)
            print("A new area has been added successfully." if success else "Error occurred while adding area.")
    elif args.operation == "add-subarea":
        if not args.name or not args.parent:
            print("Please add a value for SubArea Name(--name) and SubArea Parent Id(--parent).")
        else:
            success = add_subarea(args.name, args.parent)
            print("A new subarea has been added successfully" if success else "No match found for parent id.")
