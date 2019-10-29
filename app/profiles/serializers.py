from rest_framework import serializers

from profiles.models import Profile, Language, Address


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
        fields = ['id', 'country', 'state', 'city']
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': True
            }
        }


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    languages = LanguageSerializer(source='language_set', many=True)
    addresses = AddressSerializer(source='address')

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

            'addresses'
        ]

    def update(self, instance, validated_data):
        # Update the book instance
        languages = validated_data.pop('language_set', None)
        if languages:
            self._process_languages(instance, languages)

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['subjective_tags']:
            data['subjective_tags'] = []
        if not data['law_type_tags']:
            data['law_type_tags'] = []
        if not data['addresses']:
            data['addresses'] = []
        return data
