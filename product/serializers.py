from rest_framework import serializers

from .models import Category, Computers, Laptops, Comment

class ReplySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username', required=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'username',
            'text',
            'date_added',
            'is_reply',
        )

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username', required=False)
    comment = ReplySerializer(many=True, required=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'username',
            'comment',
            'text',
            'date_added',
            'rating',
            'advantages',
            'disadvantages',
            'is_reply',
        )


class LaptopSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Laptops
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'description',
            'category',
            'price',
            'screen_resolution',
            'screen_type',
            'processor',
            'ram',
            'drive_type',
            'video',
            'battery',
            'get_image',
            'get_thumbnail',
            'comments'
        )


class ComputerSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Computers
        fields = (
            'id',
            'name',
            'get_absolute_url',
            'description',
            'price',
            'category',
            'screen_resolution',
            'screen_type',
            'processor',
            'ram',
            'drive_type',
            'video',
            'get_image',
            'get_thumbnail',
            'comments'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'get_absolute_url',
        )


