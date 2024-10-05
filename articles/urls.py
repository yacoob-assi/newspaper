from django.urls import path
from .views import (
    ArticleListView,
    DeleteArticle,
    DetailArticle,
    UpdateArticle,
    CreateArticle,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("delete/<int:pk>", DeleteArticle.as_view(), name="article_delete"),
    path("detail/<int:pk>", DetailArticle.as_view(), name="article_detail"),
    path("update/<int:pk>", UpdateArticle.as_view(), name="article_edit"),
    path("new/", CreateArticle.as_view(), name="article_new"),
]
