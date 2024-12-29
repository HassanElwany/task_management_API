from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("The due date must be in the future.")
        return value
