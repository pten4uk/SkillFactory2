from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
    path('', NewsList.as_view(), name='home'),
    path('add/', NewsCreate.as_view(), name='create'),
    path('<int:pk>', NewsDetail.as_view(), name='detail'),
    path('<int:pk>/edit', NewsUpdate.as_view(), name='update'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='delete'),
]
