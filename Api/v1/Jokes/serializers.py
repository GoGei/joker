from rest_framework import serializers
from core.Joke.models import Joke
from core.Utils.validators import TelegramNicknameValidator


class JokeSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(read_only=True)
    is_seen = serializers.BooleanField(read_only=True)

    class Meta:
        model = Joke
        fields = (
            'id',
            'slug',
            'text',
            'is_liked',
            'is_seen',
        )


class JokeSeenSerializer(serializers.Serializer):
    seen_jokes = serializers.ListField(required=False)

    def validate(self, data):
        seen_jokes = data.get('seen_jokes', [])
        for pk in seen_jokes:
            try:
                Joke.objects.get(pk=pk)
            except Joke.DoesNotExist:
                raise serializers.ValidationError({'seen_jokes': 'Joke with ID %s does not found!' % pk})
        return data


class JokeSendToEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class JokeSendToTelegramSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=True, validators=[TelegramNicknameValidator])
