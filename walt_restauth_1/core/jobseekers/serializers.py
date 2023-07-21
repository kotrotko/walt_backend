from rest_framework import serializers

from .models import JobSeeker


class JobseekerSerializer(serializers.ModelSerializer):

    def get_role(self, obj):
        return obj.user.roles

    # pnone_number: I should not write the unit tests for the packages you install using pip.

    class Meta:
        model = JobSeeker
        fields = ('id', 'first_name', 'phone_number', 'cv')
