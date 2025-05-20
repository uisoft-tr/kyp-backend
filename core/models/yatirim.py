from django.db import models

class IsinAdi(models.Model):
    id = models.AutoField(primary_key=True)
    ad = models.CharField(max_length=255, verbose_name="İşin Adı",unique=True,)
    
    def __str__(self):
        return self.ad

    class Meta:
        verbose_name = "İşin Adı"
        verbose_name_plural = "İş Adları"

class Yatirim(models.Model):
    YIL_CHOICES = [(year, str(year)) for year in range(2025, 2050)]
    YAPILIS_SEKLI_CHOICES = [
        ('kamulastırma', 'Kamulaştırma'),
        ('kamulastırma_disi', 'Kamulaştırma Dışı'),
    ]
    isin_adi = models.ForeignKey(IsinAdi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="İşin Adı")
    toplam_kesif_ihale_bedeli = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Toplam Keşif ve İhale Bedeli")
    yil_sonuna_kadar_harcama = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Yıl Sonuna Kadar Harcama")
    yil_kesif_bedeli = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Yıl Keşif Bedeli")
    yil_nakti = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Yıl Nakdi")
    revize_odenk = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Revize Ödenek")
    bbb_ve_sonrasi_kesif_bedeli = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="BBB ve Sonrası Keşif Bedeli")
    yapilis_sekli = models.CharField( choices=YAPILIS_SEKLI_CHOICES, verbose_name="Yapılış Şekli")
    baslama_tarihi = models.IntegerField(choices=YIL_CHOICES, verbose_name="Başlama Yılı")
    bitis_tarihi = models.IntegerField(choices=YIL_CHOICES, verbose_name="Bitiş Yılı")
    talep = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Talep")
    tenkis = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Tenkis")

    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')
    
    def __str__(self):
        return f"{self.isin_adi} "

    class Meta:
        verbose_name = "Yatırım"
        verbose_name_plural = "Yatırımlar"
