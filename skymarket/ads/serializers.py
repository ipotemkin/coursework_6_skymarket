from rest_framework import serializers

from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source="id", required=False)
    author_first_name = serializers.CharField(source="author.first_name", required=False, read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", required=False, read_only=True)
    ad_id = serializers.IntegerField()
    author_id = serializers.IntegerField()

    class Meta:
        model = Comment
        exclude = ("id", "ad", "author")


class AdSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source="id")

    class Meta:
        model = Ad
        exclude = ("id", "author", "created_at")


class AdDetailSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source="id", required=False)
    author_first_name = serializers.CharField(source="author.first_name", required=False, read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", required=False, read_only=True)
    phone = serializers.CharField(source="author.phone", required=False, read_only=True)
    author_id = serializers.IntegerField()

    class Meta:
        model = Ad
        exclude = ("author", "id", "created_at")
