from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MakineViewSet, MakineTakipViewSet, PlanlamalarViewSet,
    YatirimViewSet, KanunViewSet, IlceViewSet, IlViewSet,dashboard,IsTanimiViewSet,MarkaViewSet,ModelAdiViewSet,IsinAdiViewSet,yil_choices
)

router = DefaultRouter()

router.register(r'makine', MakineViewSet, basename='makine')
router.register(r'markalar', MarkaViewSet)
router.register(r'modeller', ModelAdiViewSet)
router.register(r'makine_takip', MakineTakipViewSet)
router.register(r'planlamalar', PlanlamalarViewSet)
router.register(r'yatirimlar', YatirimViewSet)
router.register(r'kanunlar', KanunViewSet)
router.register(r'iller', IlViewSet)
router.register(r'ilceler', IlceViewSet)
router.register(r'is_tanimi', IsTanimiViewSet)
router.register(r'isin_adi', IsinAdiViewSet)

urlpatterns = [
    path('yil-choices/', yil_choices, name='yil-choices'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', include(router.urls)),
]
