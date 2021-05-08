from datetime import datetime, timedelta


from rest_framework import serializers

from src.accounts.serializers import CreateUserSerializer
from src.accounts.models import ActionLog
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


class DateRangeSerializer(serializers.Serializer):
    date_from = serializers.DateField(format='%Y-%m-%d')
    date_to = serializers.DateField(format='%Y-%m-%d')

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        today = datetime.now()

        if date_to > today.date():
            raise serializers.ValidationError({
                'date_to': "Can't be after today's date."
            })

        if date_from > today.date():
            raise serializers.ValidationError({
                'date_from': "Can't be after today's date."
            })

        if (date_to - date_from).days < 0:
            raise serializers.ValidationError({
                'date_to': "Can't be before 'date_from'."
            })
        
        return data

    

class PostAnalysisSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField('get_total_likes', read_only=True)
    total_unlikes = serializers.SerializerMethodField('get_total_unlikes', read_only=True)
    owner = CreateUserSerializer()

    class Meta:
        model = Post
        fields = ('title', 'slug', 'owner', 
                  'total_likes', 'total_unlikes')

    def get_date(self):
        # Returns date if it was declared
        request = self.context.get('request')

        if request is not None:
            date_range_data = request.GET
            date_range_serializer = DateRangeSerializer(data=date_range_data)
            if date_range_serializer.is_valid():
                date_from = date_range_serializer.validated_data['date_from']
                date_to = date_range_serializer.validated_data['date_to']
                return (date_from, date_to)
        return (None, None)
            

    def get_post_likes(self, obj, like, unlike):
        date_from, date_to = self.get_date()

        post_likes = UserPostLike.objects \
            .filter(post=obj, like=like, unlike=unlike) \
            .order_by('-updated_at')

        # If date_from and date_to declared
        if date_from and date_to:    
            # Added +1 day to date_to because updated_at field is datetime field with hours, minutes ...
            # For example:
            #   updated_at = 2020-09-03T06:32:35
            #   date_to = 2020-09-03T00:00:00 -> That is before than updated_at date
            # So we converted date_to -> 2020-09-04T00:00:00
            
            date_to_end = date_to + timedelta( days=1 ) 
            post_likes = post_likes \
                .filter(updated_at__range=(date_from, date_to_end)) \
                            
        return post_likes
    

    def get_total_likes(self, obj):
        post_likes = self.get_post_likes(obj, True, False)
        return post_likes.count()


    def get_total_unlikes(self, obj):
        post_likes = self.get_post_likes(obj, False, True)
        return post_likes.count()

class ByDateLikesAnalysisSerializer(serializers.Serializer):
    date = serializers.DateField(format='%Y-%m-%d')
    total_likes = serializers.SerializerMethodField('get_total_likes', read_only=True)
    total_unlikes = serializers.SerializerMethodField('get_total_unlikes', read_only=True)
    new_posts = serializers.SerializerMethodField('get_new_posts', read_only=True)
    new_users = serializers.SerializerMethodField('get_new_users', read_only=True) 

    def get_user_actions_count(self, obj, action_type):
        date = obj['date']
        date_end = date + timedelta( days=1 ) 
        post_likes_count = ActionLog.objects \
            .filter(action_type=action_type) \
            .filter(created_at__range=(date, date_end)) \
            .order_by('-updated_at').count()

        return post_likes_count



    def get_total_likes(self, obj):
        post_likes_count = self.get_user_actions_count(obj, ActionLog.LIKE)
        return post_likes_count

    def get_total_unlikes(self, obj):
        post_unlikes_count = self.get_user_actions_count(obj, ActionLog.UNLIKE)
        return post_unlikes_count

    def get_new_users(self, obj):
        new_users_count = self.get_user_actions_count(obj, ActionLog.REGISTER)
        return new_users_count

    

    def get_new_posts(self, obj):
        date = obj['date']
        date_end = date + timedelta( days=1 )
        posts_count = Post.objects.filter(created_at__range=(date, date_end)).count()

        return posts_count


    