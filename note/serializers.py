from rest_framework import serializers
from note.models import ReportComment, TailoringComment, Notepad


class NotepadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notepad
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        workshop = validated_data['workshop']

        if workshop.notepad:
            raise serializers.ValidationError({'rejected': 'У этого цеха уже есть блокнот'})

        if user.account_type == 'head':
            head_workshops = user.head_workshops.all()
            if workshop in head_workshops:
                instance = super().create(validated_data)
                workshop.notepad = instance
                workshop.save()
                return instance

        raise serializers.ValidationError({'rejected': 'Вы должны быть руководителем данного цеха'})


class TailoringCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TailoringComment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
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


class ReportCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
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
