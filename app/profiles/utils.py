import json
import os

from django.conf import settings

from clsite.settings import PROJECT_ROOT
from .choices import LANGUAGES_CHOICES


def _read_json(path):
    """
    Reads a json file and returns the results.
    """
    with open(path, "r") as file:
        data = json.load(file)
        return data


def _get_all_subjective_tags_tuple():
    """
    Returns all the subjective tags present in subjective-tags-ontology.json
    file in the form of choices readable tuple.
    """

    file_path = os.path.join(PROJECT_ROOT, "choices", "subjective-tags.json")
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

    file_path = os.path.join(PROJECT_ROOT, "choices", "law-type-tags-ontology.json")
    tags_dict = _read_json(file_path)
    result_list = []
    for area in tags_dict:
        if area.get("subareas") is not None:
            subarea_list = area.pop("subareas")
            subarea_names_list = []
            for subarea in subarea_list:
                subarea_names_list.append((subarea["name"], subarea["name"]))
                # throw value error if ontology exceeds two levels
                if subarea.get("subareas"):
                    raise ValueError("Only two levels are allowed in law-tag-type-ontology.json")

            area_tuple = (area["name"], tuple(subarea_names_list))
            result_list.append(area_tuple)
    return tuple(result_list)


def _get_all_countries_tuple():
    """
    Returns all countries in the form of choices readable tuple.
    """

    file_path = os.path.join(PROJECT_ROOT, "choices", "countries+states.json")
    countries_states_cities = _read_json(file_path)
    result_list = []
    for row in countries_states_cities:
        country_tuple = (row["name"], row["name"])
        result_list.append(country_tuple)

    return tuple(result_list)


def _get_states_for_country(country_name):
    """
    Returns all the states of a given country in the form of choices readable tuple.
    """

    file_path = os.path.join(PROJECT_ROOT, "choices", "countries+states.json")
    countries_states_cities = _read_json(file_path)
    result_list = []
    for row in countries_states_cities:
        if row["name"] == country_name:
            list_states = row["states"]
            result_list = [(state, state) for state in list_states]
            return tuple(result_list)

    return tuple(result_list)


def custom_language_choices():
    choices = list(LANGUAGES_CHOICES)
    choices.sort(key=lambda tup: tup[1])
    for i, lang in enumerate(choices):
        if lang[0] == settings.DEFAULT_USER_LANGUAGE:
            default_language = choices.pop(i)
    choices.insert(0, default_language)
    return choices


CUSTOM_SORTED_LANGUAGES_CHOICES = custom_language_choices()

LAW_TYPE_TAGS_CHOICES = _get_all_law_type_tags_tuple()

SUBJECTIVE_TAGS_CHOICES = _get_all_subjective_tags_tuple()

COUNTRIES_CHOICES = _get_all_countries_tuple()
