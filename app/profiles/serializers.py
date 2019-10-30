from rest_framework import serializers

from profiles.models import Profile, Language, Address, Education


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'proficiency_level']
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': True
            }
        }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'state', 'city']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school', 'degree', 'graduation_date']
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': True
            }
        }


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    languages = LanguageSerializer(source='language_set', many=True)
    address = AddressSerializer()
    educations = EducationSerializer(source='education_set', many=True)

    class Meta:
        model = Profile
        fields = [
            'handle',
            'summary',
            'bio',
            'languages',
            'subjective_tags',

            'law_type_tags',
            'experience',
            'current_job',

            'address',

            'educations',
        ]

    def update(self, instance, validated_data):
        # Update the book instance
        languages = validated_data.pop('language_set', None)
        if languages is not None:
            self._process_languages(instance, languages)

        address = validated_data.pop('address', None)
        if address is not None:
            self._process_address(instance, address)

        educations = validated_data.pop('education_set', None)
        if educations is not None:
            self._process_educations(instance, educations)

        return super().update(instance, validated_data)

    def _process_languages(self, instance, languages):
        # Delete any pages not included in the request
        language_ids = [item['id'] for item in languages if 'id' in item]
        for language in instance.language_set.all():
            if language.id not in language_ids:
                language.delete()

        # Create or update page instances that are in the request
        for item in languages:
            language = Language(**item, profile=instance)
            language.save()

    def _process_address(self, instance, address):
        if not address:
            if hasattr(instance, 'address'):
                instance.address.delete()
                instance.address = None
            return

        if hasattr(instance, 'address'):
            for key, attr in address.items():
                setattr(instance.address, key, attr)
            instance.address.save()
        else:
            Address.objects.create(profile=instance, **address)

    def _process_educations(self, instance, educations):
        # Delete any pages not included in the request
        language_ids = [item['id'] for item in educations if 'id' in item]
        for education in instance.education_set.all():
            if education.id not in language_ids:
                education.delete()

        # Create or update page instances that are in the request
        for item in educations:
            education = Education(**item, profile=instance)
            education.save()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['subjective_tags']:
            data['subjective_tags'] = []
        if not data['law_type_tags']:
            data['law_type_tags'] = []
        addresses = data.pop('address', [])
        if addresses:
            data['addresses'] = [addresses, ]
        else:
            data['addresses'] = []
        return data

    def to_internal_value(self, data):
        addresses = data.pop('addresses', None)
        if addresses:
            data['address'] = addresses[0]
        else:
            data['address'] = {}
        return super().to_internal_value(data)
