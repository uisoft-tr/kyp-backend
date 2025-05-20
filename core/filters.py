import django_filters
from .models import MakineTakip, Ilce, Makine, Planlamalar, IsinAdi, Yatirim, KanunMaddeleri
from django.db.models import Q, Count


class IlceFilter(django_filters.FilterSet):
    il = django_filters.NumberFilter(field_name="il", lookup_expr="exact")

    class Meta:
        model = Ilce
        fields = ["il"]

class MakineFilter(django_filters.FilterSet):
    no = django_filters.CharFilter(lookup_expr="icontains")
    tur = django_filters.CharFilter(lookup_expr="icontains")
    cins = django_filters.CharFilter(lookup_expr="icontains")
    marka = django_filters.CharFilter(field_name="marka__ad", lookup_expr="icontains")
    model_adi = django_filters.CharFilter(
        field_name="model_adi__ad", lookup_expr="icontains"
    )
    ait_oldugu_yer = django_filters.CharFilter(lookup_expr="icontains")
    calisma_durumu = django_filters.ChoiceFilter(
        choices=[("devam", "Devam ediyor"), ("bitti", "Bitti")],
        method="filter_calisma_durumu",
    )

    class Meta:
        model = Makine
        fields = [
            "no",
            "model_adi",
            "tur",
            "cins",
            "marka",
            "ait_oldugu_yer",
            "calisma_durumu",
        ]

    def filter_calisma_durumu(self, queryset, name, value):
        if value:
            if value == "devam":
                # 'devam' olan takipler
                return queryset.filter(takipler__isin_durumu="devam")
            elif value == "bitti":
                # Tüm takiplerin 'bitti' olduğu makineler
                return (
                    queryset.annotate(
                        completed_tasks=Count(
                            "takipler", filter=Q(takipler__isin_durumu="bitti")
                        )
                    )
                    .filter(
                        completed_tasks=Count("takipler")  # Tüm takipler 'bitti' olmalı
                    )
                    .distinct()
                )

        return queryset

class MakineTakipFilter(django_filters.FilterSet):
    makina = django_filters.ModelChoiceFilter(queryset=Makine.objects.all())
    calistigi_yer = django_filters.CharFilter(lookup_expr="icontains")
    isin_durumu = django_filters.ChoiceFilter(
        choices=MakineTakip.IS_DURUMU_SECENEKLERI, lookup_expr="exact"
    )
    is_tanimi = django_filters.CharFilter(
        field_name="is_tanimi__tanim", lookup_expr="icontains"
    )
    ise_baslama = django_filters.DateFilter(lookup_expr="exact")
    ise_bitis = django_filters.DateFilter(lookup_expr="exact")

    class Meta:
        model = MakineTakip
        fields = [
            "makina",
            "calistigi_yer",
            "isin_durumu",
            "is_tanimi",
            "ise_baslama",
            "ise_bitis",
        ]

class PlanlamaFilter(django_filters.FilterSet):
    bolge_no = django_filters.NumberFilter(field_name="bolge_no", lookup_expr="exact")
    il = django_filters.NumberFilter(field_name="il", lookup_expr="exact")
    ilce = django_filters.NumberFilter(field_name="ilce", lookup_expr="exact")
    ilk_inceleme_raporu = django_filters.ChoiceFilter(
        choices=[("var", "Var"), ("yok", "Yok")], method="filter_ilk_inceleme_raporu"
    )
    on_inceleme_raporu = django_filters.ChoiceFilter(
        choices=[("var", "Var"), ("yok", "Yok")], method="filter_on_inceleme_raporu"
    )
    kamulastirma_problemi = django_filters.ChoiceFilter(
        choices=[("var", "Var"), ("yok", "Yok")], method="filter_kamulastirma_problemi"
    )

    class Meta:
        model = Planlamalar
        fields = [
            "bolge_no",
            "il",
            "ilce",
            "ilk_inceleme_raporu",
            "on_inceleme_raporu",
            "kamulastirma_problemi",
        ]

    def filter_ilk_inceleme_raporu(self, queryset, name, value):
        if value:
            return queryset.filter(ilk_inceleme_raporu=value)
        return queryset

    def filter_on_inceleme_raporu(self, queryset, name, value):
        if value:
            return queryset.filter(on_inceleme_raporu=value)
        return queryset

    def filter_kamulastirma_problemi(self, queryset, name, value):
        if value:
            return queryset.filter(kamulastirma_problemi=value)
        return queryset

class YatirimFilter(django_filters.FilterSet):
    isin_adi = django_filters.ModelChoiceFilter(
        queryset=IsinAdi.objects.all(), field_name="isin_adi", label="İşin Adı"
    )
    yapilis_sekli = django_filters.ChoiceFilter(
        choices=Yatirim.YAPILIS_SEKLI_CHOICES,
        field_name="yapilis_sekli",
        label="Yapılış Şekli",
    )
    baslama_tarihi = django_filters.DateFilter(lookup_expr="exact")
    bitis_tarihi = django_filters.DateFilter(lookup_expr="exact")

    class Meta:
        model = Yatirim
        fields = [
            "isin_adi",
            "yapilis_sekli",
            "baslama_tarihi",
            "bitis_tarihi",
        ]

class KanunFilter(django_filters.FilterSet):
    no = django_filters.CharFilter(lookup_expr='icontains')  
    adi = django_filters.CharFilter(lookup_expr='icontains') 

    class Meta:
        model = KanunMaddeleri
        fields = ['no', 'adi']