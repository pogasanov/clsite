from rest_framework import serializers

from profiles.models import Profile, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'proficiency_level']


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    languages = LanguageSerializer(source='language_set', many=True)

    class Meta:
        model = Profile
        fields = ['handle', 'summary', 'bio', 'languages', 'law_type_tags']
