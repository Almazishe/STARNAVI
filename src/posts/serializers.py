from rest_framework import serializers

from .models import Post, UserPostLike



class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image', 'text')
    
    def create(self, validated_data):
        user = self.context.get('request').user

        post = Post(**validated_data, owner=user)
        post.save()

        return post


class PostEvaluationSerializer(serializers.Serializer):
    LIKE = 1
    UNLINE = 0
    REMOVE_EVALUATION = 2
    EVALUATE_CHOICES = (
        (LIKE, "Like"), 
        (UNLINE, "Unlike"),
        (REMOVE_EVALUATION, "Remove")
    )

    slug = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())
    action = serializers.ChoiceField(choices=EVALUATE_CHOICES)


    def create(self, validated_data):
        user = self.context.get('request').user
        post = validated_data.get('slug')

        defaults = {
            'like': bool(validated_data.get('action')),
            'unlike': not bool(validated_data.get('action'))
        }

        if validated_data.get('action') == 2:
            # If user wants to remove like or dislike
            defaults['like'] = False
            defaults['unlike'] = False

        
        user_post_like, _ = UserPostLike.objects.update_or_create(
            user=user,
            post=post,
            defaults=defaults
        )

        return user_post_like