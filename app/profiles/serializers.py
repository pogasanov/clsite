from rest_framework import serializers

from profiles.models import Profile, Language


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


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    languages = LanguageSerializer(source='language_set', many=True)

    class Meta:
        model = Profile
        fields = ['handle', 'summary', 'bio', 'languages', 'law_type_tags']

    def update(self, instance, validated_data):
        # Update the book instance
        instance.summary = validated_data['summary']
        instance.bio = validated_data['bio']
        instance.save()

        # Delete any pages not included in the request
        language_ids = [item['id'] for item in validated_data['language_set'] if 'id' in item]
        for language in instance.language_set.all():
            if language.id not in language_ids:
                language.delete()

        # Create or update page instances that are in the request
        for item in validated_data['language_set']:
            language = Language(*item, profile=instance)
            language.save()

        return instance
