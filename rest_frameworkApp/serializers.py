from rest_framework import serializers
from project.models import Project, Task, Comment




class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id',
            'description',
            'comments',
            'members',
            'project_admin',
            'tasks',
            'priority',
            'start_date',
            'end_date',
            'status',
            'is_completed',
        )
       


class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'comments',
            'status',
            'priority',
            'assignee',
        )

class TaskSerializer(serializers.ModelSerializer):
   
    length_of_title = serializers.SerializerMethodField()

    def get_length_of_title(self, obj):

        length = len(obj.title)
        # print(length)
        return length
    
    def validate(self, obj):

        if obj.length_of_title.length < 10:
            raise serializers.ValidationError("title length should be greater than 10")
        else:
            return obj



    class Meta:
        model = Task
        fields = '__all__'





class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__' # <-- Add this line



   