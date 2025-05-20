from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

class Marka(models.Model):
    ad = models.CharField(max_length=100, unique=True, verbose_name="Marka Adı")

    def __str__(self):
        return self.ad
    
    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Markalar"

class ModelAdi(models.Model):
    ad = models.CharField(max_length=100, unique=True, verbose_name="Model Adı")
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE, related_name='modeller')

    def __str__(self):
        return self.ad
    
    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Modeller"

class Makine(models.Model):
    no = models.CharField(max_length=50, unique=True, verbose_name="Makine No", error_messages={
        "unique": "Bu makine numarası zaten mevcut."
    })
    model_adi = models.ForeignKey(ModelAdi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Model")
    tur = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tür")
    cins = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cins")
    marka = models.ForeignKey(Marka, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Marka")
    ait_oldugu_yer = models.CharField(max_length=100, verbose_name='Yer Adı')
    
    @property
    def calisma_durumu(self):
        son_takip = self.takipler.order_by("-id").first()
        if son_takip:
            return son_takip.isin_durumu
        return "bitti"
    
    def __str__(self):
        return self.no
    
    class Meta:
        verbose_name = 'Makine'
        verbose_name_plural = 'Makineler'

class IsTanimi(models.Model):
    id = models.AutoField(primary_key=True)
    tanim = models.CharField(max_length=255, verbose_name="İş Tanımı")
    
    def __str__(self):
        return self.tanim

    class Meta:
        verbose_name = "İş Tanımı"
        verbose_name_plural = "İş Tanımları"

class MakineTakip(models.Model):
    makina = models.ForeignKey(Makine, on_delete=models.CASCADE, verbose_name="Makine No", related_name="takipler", null=True, blank=True)
    calistigi_yer = models.CharField(max_length=200, blank=True, null=True, verbose_name="Çalıştığı Yer")
    konum = models.PointField(blank=True, null=True, verbose_name="Konum")
    
    IS_DURUMU_SECENEKLERI = [
        ('devam', 'Devam ediyor'),
        ('bitti', 'Bitti'),
    ]
    isin_durumu = models.CharField(max_length=10, choices=IS_DURUMU_SECENEKLERI, default='bitti', verbose_name="İş Durumu")
    ise_baslama = models.DateField(blank=True, null=True, verbose_name="İşe Başlama Tarihi")
    ise_bitis = models.DateField(blank=True, null=True, verbose_name="İşin Bittiği Tarih")
    aciklama = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    is_tanimi = models.ForeignKey(IsTanimi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="İş Tanımı")
    
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def clean(self):
        if self.isin_durumu == 'bitti' and not self.ise_bitis:
            raise ValidationError('İş bitiş tarihi gereklidir.')
        if self.isin_durumu == 'devam' and self.ise_bitis:
            raise ValidationError('İş bitiş tarihi sadece iş durumu "bitti" olduğunda girilebilir.')

    def __str__(self):
        return f"{self.makina.no} - {self.isin_durumu}"
    
    class Meta:
        verbose_name = "Makine Takibi"
        verbose_name_plural = "Makine Takipleri"
