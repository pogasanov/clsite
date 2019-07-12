import json
import os

from django.conf.global_settings import LANGUAGES

from clsite.settings import BASE_DIR


LANGUAGES_PROFICIENCY_LEVEL = (('NS', 'Native speaker'),
                               ('PF', 'professional fluency'),
                               ('CF', 'conversational fluency'))


def _read_json(path):
    """
    Reads a json file and returns the results.
    """
    with open(path, 'r') as file:
        data = json.load(file)
        file.close()
        return data


def _get_all_subjective_tags_tuple():
    """
    Returns all the subjective tags present in subjective-tags-ontology.json
    file in the form of choices readable tuple.
    """

    path = 'profiles/subjectivetags/subjective-tags.json'
    file_path = os.path.join(BASE_DIR, path)

    tags = _read_json(file_path)
    result_list = []
    for name in tags:
        tag_tuple = name, name
        result_list.append(tag_tuple)
    return tuple(result_list)


def _get_all_law_type_tags_tuple():
    """
    Returns all the law type tags present in law-type-tags-ontology.json
    file in the form of choices readable tuple.
    """

    path = 'profiles/lawtypetags/law-type-tags-ontology.json'
    file_path = os.path.join(BASE_DIR, path)
    tags_dict = _read_json(file_path)
    result_list = []
    for area in tags_dict:
        if area.get("subareas") is not None:
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


def _get_language_selection_tuple():
    result_list = []
    for symbol, language in LANGUAGES:
        choices = []
        for i, level in LANGUAGES_PROFICIENCY_LEVEL:
            choices.append((symbol + '-' + i, language + ' ' + level))
        result_list.append((language, tuple(choices)))

    return tuple(result_list)


LAW_TYPE_TAGS_CHOICES = _get_all_law_type_tags_tuple()

SUBJECTIVE_TAGS_CHOICES = _get_all_subjective_tags_tuple()

LANGUAGES_CHOICES = _get_language_selection_tuple()
