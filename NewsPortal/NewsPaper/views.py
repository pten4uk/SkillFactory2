import json
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Author, Category
from .filters import PostFilter


class NewsList(ListView):
    model = Post
    template_name = 'NewsPaper/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-datetime')
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        subscribed = False
        if os.path.exists('subscribers.json'):
            with open('subscribers.json', 'r', encoding='utf8') as f:
                info = json.load(f)

            if self.request.user.is_authenticated:
                for i in info.values():
                    if self.request.user.email in i:
                        subscribed = True
                        break
        return {
            **super().get_context_data(**kwargs),
            'filter': self.get_filter(),
            'is_not_author': not self.request.user.groups.filter(name='authors').exists(),
            'subscribed': subscribed,
        }


class NewsDetail(DetailView):
    model = Post
    template_name = 'NewsPaper/post.html'
    context_object_name = 'post'


class NewsCreate(LoginRequiredMixin, CreateView):
    template_name = 'NewsPaper/create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        if self.request.user.groups.filter(name='authors').exists():
            group = Group.objects.get(name='authors')
            group.user_set.add(self.request.user)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.author = Author.objects.get_or_create(polzovatel=self.request.user)[0]
        if not self.object.author.polzovatel.groups.filter(name='authors').exists():
            group = Group.objects.get(name='authors')
            group.user_set.add(self.request.user)
        self.object.save()

        cat = Category.objects.get(pk=self.request.POST['category'])
        self.object.category.add(cat)
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'NewsPaper/create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'NewsPaper/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def subscribe(r):
    categories = Category.objects.all()
    return render(r, 'NewsPaper/subscribe.html', {'categories': categories})


@login_required
def unsubscribe(r):
    user_email = r.user.email

    if os.path.exists('subscribers.json'):
        with open('subscribers.json', 'r', encoding='utf8') as f:
            info = json.load(f)

        for key, values in info.items():
            for i, row in enumerate(values):
                if row == user_email:
                    info[key].pop(i)

        with open('subscribers.json', 'w', encoding='utf8') as f:
            json.dump(info, f, indent=4, ensure_ascii=False)

    return redirect('/news/')


@login_required
def choice_sub(r, pk):
    email = r.user.email
    categories_in_db = Category.objects.all()
    current_cat = categories_in_db[pk-1].name

    categories = {}
    for category in categories_in_db:
        categories[category.name] = []

    if email:
        if os.path.exists('subscribers.json'):
            with open('subscribers.json', 'r', encoding='utf8') as f:
                categories = json.load(f)

            if current_cat not in categories:
                categories[current_cat] = []

            if email not in categories[current_cat]:
                categories[current_cat].append(email)

            with open('subscribers.json', 'w', encoding='utf8') as f:
                json.dump(categories, f, indent=4, ensure_ascii=False)
        else:
            categories[current_cat].append(email)
            with open('subscribers.json', 'w', encoding='utf8') as f:
                json.dump(categories, f, indent=4, ensure_ascii=False)

    return redirect('/news/')