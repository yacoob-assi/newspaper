from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, FormView  # new
from django.views.generic.detail import SingleObjectMixin  # new
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse  # new
from .forms import CommentForm
from .models import Article


class CommentPost(SingleObjectMixin, FormView):  # new
    model = Article
    form_class = CommentForm
    template_name = "detail_article.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class CommentGet(DetailView):  # new
    model = Article
    template_name = "detail_article.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class DetailArticle(LoginRequiredMixin, View):  # new
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class CreateArticle(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "create_article.html"
    fields = ("title", "body")

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateArticle(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Article
    template_name = "update_article.html"
    fields = ("title", "body")

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class DeleteArticle(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Article
    template_name = "delete_article.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user
