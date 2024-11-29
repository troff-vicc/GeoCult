from rest_framework import serializers
from .models import MyModel, Pos, Buy


class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
        
        
class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pos
        fields = '__all__'
        

class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'
