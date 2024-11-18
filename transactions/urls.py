from rest_framework import routers
from .views import TransactionViewSet, PDFTransactionAPIView, PDFTransactionListAPIView
from django.urls import path


router = routers.SimpleRouter(trailing_slash=False)
router.register("transactions", TransactionViewSet, basename="transactions")


urlpatterns = [
    path("pdf/transactions", PDFTransactionListAPIView.as_view()),
    path("pdf/transactions/<str:pk>", PDFTransactionAPIView.as_view()),
]

urlpatterns += router.urls
