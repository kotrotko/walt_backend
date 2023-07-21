from rest_framework import serializers

from .models import Employer


class EmployerSerializer(serializers.ModelSerializer):
    def get_role(self, obj):
        return obj.user.roles

    def create(self, validated_data):
        user = self.context['request'].user # Assuming user is authenticated
        roles = user.roles

        if roles == 'employer':
            # User is registered as an employer
            return Employer.objects.create(user=user, **validated_data)
        else:
            # User is not registered as an employer, handle
            raise serializers.ValidationError('User is not authorized to register as an employer.')

    class Meta:
        model = Employer
        fields = ['company_name', 'company_description', 'website']

