from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['handle', 'is_staff']
