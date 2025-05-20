from django.db import models

class Il(models.Model):
    name = models.CharField(max_length=100, verbose_name="İl Adı")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Il"
        verbose_name_plural = "Iller"

class Ilce(models.Model):
    il = models.ForeignKey(Il, on_delete=models.CASCADE, related_name='ilceler')
    name = models.CharField(max_length=100, verbose_name="İlçe Adı")

    def __str__(self):
        return f"{self.il.name} - {self.name}"
    
    class Meta:
        verbose_name = "Ilce"
        verbose_name_plural = "Ilceler"

class Planlamalar(models.Model):
    CHOICES = [('var', 'Var'), ('yok', 'Yok')]
    
    sira_no = models.IntegerField(verbose_name="Sıra No")
    bolge_no = models.IntegerField(verbose_name="Bölge No")
    il = models.ForeignKey(Il, on_delete=models.SET_NULL, null=True, blank=True)
    ilce = models.ForeignKey(Ilce, on_delete=models.SET_NULL, null=True, blank=True)
    taskin_isi_adi = models.CharField(max_length=200, verbose_name="Taşkın İşi Adı")
    ilk_inceleme_raporu = models.CharField(choices=CHOICES, max_length=3, verbose_name="İlk İnceleme Raporu")
    on_inceleme_raporu = models.CharField(choices=CHOICES, max_length=3, verbose_name="Ön İnceleme Raporu")
    kamulastirma_problemi = models.CharField(choices=CHOICES, max_length=3, verbose_name="Kamulaştırma Problemi")
    yaklasik_insaat_maliyeti = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Yaklaşık İnşaat Maliyeti (TL)")
    korunan_yerlesim_yeri = models.CharField(max_length=200, verbose_name="Korunan Yerleşim Yeri")
    aciklama = models.TextField(verbose_name="Açıklama")
    
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturma Tarihi')
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return f"{self.il} - {self.ilce} - {self.taskin_isi_adi}"

    class Meta:
        verbose_name = "Planlama"
        verbose_name_plural = "Planlamalar"

