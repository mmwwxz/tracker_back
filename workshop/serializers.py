from rest_framework import serializers
from .models import Workshop, Tailoring, Expense, Report


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        head_workshops = user.head_workshops.all()

        if len(head_workshops.all()) < 5:
            validated_data['head'] = user
            instance = super().create(validated_data)
            return instance

        raise serializers.ValidationError({'rejected': 'У вас не может быть больше 5-и цехов'})


class TailoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tailoring
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        workshop = validated_data['workshop']

        if user.account_type == 'head':
            head_workshops = user.head_workshops.all()
            if workshop in head_workshops:
                instance = super().create(validated_data)
                return instance

        workers_workshops = user.workers_workshops.all()
        if workshop in workers_workshops:
            instance = super().create(validated_data)
            return instance

        raise serializers.ValidationError({'rejected': 'Вы должны быть членом цеха'})


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        workshop = validated_data['workshop']

        if user.account_type == 'head':
            head_workshops = user.head_workshops.all()
            if workshop in head_workshops:
                instance = super().create(validated_data)
                return instance

        workers_workshops = user.workers_workshops.all()
        if workshop in workers_workshops:
            instance = super().create(validated_data)
            return instance

        raise serializers.ValidationError({'rejected': 'Вы должны быть членом цеха'})


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        workshop = validated_data['workshop']

        if user.account_type == 'head':
            head_workshops = user.head_workshops.all()
            if workshop in head_workshops:
                instance = super().create(validated_data)
                return instance

        workers_workshops = user.workers_workshops.all()
        if workshop in workers_workshops:
            instance = super().create(validated_data)
            return instance

        raise serializers.ValidationError({'rejected': 'Вы должны быть членом цеха'})
