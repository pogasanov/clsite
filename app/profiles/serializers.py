import json

from rest_framework import serializers

from profiles.models import (
    Profile,
    Language,
    Address,
    Education,
    WorkExperience,
    Organization,
    Award,
    Jurisdiction,
)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name", "proficiency_level"]
        extra_kwargs = {"id": {"read_only": False, "required": True}}


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["country", "state", "city"]


class JurisdictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = ["id", "country", "state", "city"]
        extra_kwargs = {"id": {"read_only": False, "required": True}}


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "school", "degree", "graduation_date"]
        extra_kwargs = {"id": {"read_only": False, "required": True}}


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ["id", "company_name", "position", "duration"]
        extra_kwargs = {"id": {"read_only": False, "required": True}}


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "position", "duration"]
        extra_kwargs = {"id": {"read_only": False, "required": True}}


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ["id", "title", "presented_by", "year"]
        extra_kwargs = {"id": {"read_only": False, "required": True}}


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    languages = LanguageSerializer(source="language_set", many=True)
    address = AddressSerializer()
    jurisdictions = JurisdictionSerializer(source="jurisdiction_set", many=True)
    educations = EducationSerializer(source="education_set", many=True)
    work_experiences = WorkExperienceSerializer(source="workexperience_set", many=True)
    organizations = OrganizationSerializer(source="organization_set", many=True)
    awards = AwardSerializer(source="award_set", many=True)

    class Meta:
        model = Profile
        fields = [
            "handle",
            "summary",
            "bio",
            "languages",
            "subjective_tags",
            "law_type_tags",
            "experience",
            "current_job",
            "address",
            "jurisdictions",
            "educations",
            "work_experiences",
            "organizations",
            "awards",
        ]

    def update(self, instance, validated_data):
        address = validated_data.pop("address", None)
        if address is not None:
            self._process_address(instance, address)

        languages = validated_data.pop("language_set", None)
        if languages is not None:
            self._sync_foreign_model(instance, languages, Language, "language_set")

        jurisdictions = validated_data.pop("jurisdiction_set", None)
        if jurisdictions is not None:
            self._sync_foreign_model(instance, jurisdictions, Jurisdiction, "jurisdiction_set")

        educations = validated_data.pop("education_set", None)
        if educations is not None:
            self._sync_foreign_model(instance, educations, Education, "education_set")

        work_experiences = validated_data.pop("workexperience_set", None)
        if work_experiences is not None:
            self._sync_foreign_model(instance, work_experiences, WorkExperience, "workexperience_set")

        organizations = validated_data.pop("organization_set", None)
        if organizations is not None:
            self._sync_foreign_model(instance, organizations, Organization, "organization_set")

        awards = validated_data.pop("award_set", None)
        if awards is not None:
            self._sync_foreign_model(instance, awards, Award, "award_set")

        return super().update(instance, validated_data)

    def _process_address(self, instance, address):
        if not address:
            if hasattr(instance, "address"):
                instance.address.delete()
                instance.address = None
            return

        if hasattr(instance, "address"):
            for key, attr in address.items():
                setattr(instance.address, key, attr)
            instance.address.save()
        else:
            Address.objects.create(profile=instance, **address)

    def _sync_foreign_model(self, instance, data, cls, manager_name):
        """
        Sync all foreign models in instance to data using their
        class object and manager name. More info
        https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
        """
        # Remove all foreign instances that are not featured in data
        data_ids = [item["id"] for item in data if "id" in item]
        for existing_foreigns in getattr(instance, manager_name).all():
            if existing_foreigns.id not in data_ids:
                existing_foreigns.delete()

        # Update all foreign instances using data
        for item in data:
            new_foreign = cls(**item, profile=instance)
            new_foreign.save()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data["subjective_tags"]:
            data["subjective_tags"] = []
        if not data["law_type_tags"]:
            data["law_type_tags"] = []
        if data["work_experiences"]:
            for exp in data["work_experiences"]:
                exp["duration"] = json.loads(exp["duration"])
        if data["organizations"]:
            for exp in data["organizations"]:
                exp["duration"] = json.loads(exp["duration"])
        return data

    def to_internal_value(self, data):
        new_data = data.copy()
        if "work_experiences" in new_data:
            for exp in new_data["work_experiences"]:
                exp["duration"] = json.dumps(exp["duration"])
        if "organizations" in new_data:
            for exp in new_data["organizations"]:
                exp["duration"] = json.dumps(exp["duration"])
        return super().to_internal_value(new_data)
