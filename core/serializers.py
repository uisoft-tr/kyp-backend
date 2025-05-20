from rest_framework import serializers
from .models import Makine, MakineTakip, Planlamalar, Yatirim, KanunMaddeleri, KanunDosyalari,Il,Ilce,IsTanimi,ModelAdi,Marka,IsinAdi
from rest_framework_gis.serializers import GeometryField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MarkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marka
        fields = ['id', 'ad']

class ModelAdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelAdi
        fields = ['id', 'ad', 'marka']

class MakineSerializer(serializers.ModelSerializer):
    calisma_durumu = serializers.SerializerMethodField()

    # ID alanları (write/read)
    marka = serializers.PrimaryKeyRelatedField(queryset=Marka.objects.all())
    model_adi = serializers.PrimaryKeyRelatedField(queryset=ModelAdi.objects.all())

    # İsim alanları (read-only)
    marka_ad = serializers.SerializerMethodField()
    model_adi_ad = serializers.SerializerMethodField()

    class Meta:
        model = Makine
        fields = ['id', 'no', 'model_adi', 'model_adi_ad', 'tur', 'cins', 'marka', 'marka_ad', 'ait_oldugu_yer', 'calisma_durumu']

    def get_calisma_durumu(self, obj):
        try:
            return obj.calisma_durumu
        except Exception as e:
            print(f"Error in calisma_durumu: {e}")
            return None

    def get_marka_ad(self, obj):
        return obj.marka.ad if obj.marka else None

    def get_model_adi_ad(self, obj):
        return obj.model_adi.ad if obj.model_adi else None


class MakineTakipSerializer(serializers.ModelSerializer):
    konum = GeometryField(write_only=True)
    makina_no = serializers.CharField(source="makina.no", read_only=True)
    konum_goster = serializers.SerializerMethodField()
    tur = serializers.CharField(source="makina.tur",read_only=True)
    is_tanimi_ad = serializers.SerializerMethodField()

    class Meta:
        model = MakineTakip
        fields = "__all__"

    def get_konum_goster(self, obj):
        if obj.konum:
            return [obj.konum.x, obj.konum.y]  
        return None
    
    def get_is_tanimi_ad(self, obj):
        return obj.is_tanimi.tanim if obj.is_tanimi else None
    
class IlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Il
        fields = ['id', 'name']  

class IlceSerializer(serializers.ModelSerializer):
    il = IlSerializer()  

    class Meta:
        model = Ilce
        fields = ['id', 'name', 'il']  
    
class PlanlamalarSerializer(serializers.ModelSerializer):
    il_adi = serializers.CharField(source='il.name', read_only=True)
    ilce_adi = serializers.CharField(source='ilce.name', read_only=True)
    class Meta:
        model = Planlamalar
        fields = '__all__'

class YatirimSerializer(serializers.ModelSerializer):
    isin_adi_ad = serializers.SerializerMethodField()

    class Meta:
        model = Yatirim
        fields = "__all__"
    
    def get_isin_adi_ad(self, obj):
        return obj.isin_adi.ad if obj.isin_adi else None

class KanunDosyalariSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanunDosyalari
        fields = ['id', 'dosya', 'dosya_tipi']

class KanunSerializer(serializers.ModelSerializer):
    dosyalar = KanunDosyalariSerializer(many=True, read_only=True)

    class Meta:
        model = KanunMaddeleri
        fields = ['id', 'no', 'adi', 'dosyalar']

class IsTanimiSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsTanimi
        fields = ['id', 'tanim',]
        
class IsinAdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsinAdi
        fields = ['id', 'ad',]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        })
        return data