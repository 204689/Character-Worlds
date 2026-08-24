from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from app.models import Article
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
import time


class ArticleListView(LoginRequiredMixin, ListView):
    template_name = "worlds/article_results.html"
    model = Article
    context_object_name = "articles"
    ordering = ["-updated_at"]
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        #time.sleep(2)
        search = self.request.GET.get("search")
        writing = self.request.GET.get("writing", "all")
        queryset = super().get_queryset()
        if writing == "your":
            queryset = queryset.filter(creator=self.request.user)
        else:
            queryset = queryset.filter(status="published")
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset.order_by("-updated_at")

class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = "worlds/create_article.html"
    model = Article
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "worlds/update_article.html"
    model = Article
    fields = ["title", "status", "content", "twitter_post"]
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "worlds/delete_article.html"
    model = Article
    success_url = reverse_lazy("home")
    context_object_name = "article"

    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().creator

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Article deleted successfully.", extra_tags="destructive")
        return super().post(request, *args, **kwargs)
