from django.db import models

class KanunMaddeleri(models.Model):
    id = models.AutoField(primary_key=True)
    no = models.CharField(max_length=50, unique=True, verbose_name='Kanun No', error_messages={
        "unique": "Bu kanun numarası zaten mevcut."
    })
    adi = models.CharField(max_length=100, verbose_name='Kanun Adı', unique=True)

    def __str__(self):
        return f"{self.no} - {self.adi}"

    class Meta:
        verbose_name = 'Kanun Maddesi'
        verbose_name_plural = 'Kanun Maddeleri'

class KanunDosyalari(models.Model):
    id = models.AutoField(primary_key=True)
    kanun_maddesi = models.ForeignKey(KanunMaddeleri, on_delete=models.CASCADE, related_name='dosyalar')
    dosya = models.FileField(verbose_name="Dosya")
    dosya_tipi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.kanun_maddesi.no} - {self.kanun_maddesi.adi}"
    
    class Meta:
        verbose_name = 'Kanun Dosya'
        verbose_name_plural = 'Kanun Dosyaları'
