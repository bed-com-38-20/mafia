from rest_framework import serializers
from .models import Post ,ChatRoom, Message


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'post_type', 'text_content', 'image', 'video', 'likes_count', 'comments_count', 'created_at', 'updated_at']
        def get_user_full_name(self, obj):
            read_only_fields = ['user']
            return f"{obj.user.first_name} {obj.user.last_name}"
        

    def validate(self, data):
        post_type = data.get('post_type')
        if post_type == 'text' and not data.get('text_content'):
            raise serializers.ValidationError("Text content is required for text posts.")
        if post_type == 'image' and not data.get('image'):
            raise serializers.ValidationError("Image is required for image posts.")
        if post_type == 'video' and not data.get('video'):
            raise serializers.ValidationError("Video is required for video posts.")
        return data



class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Message
        fields = '__all__'