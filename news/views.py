from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin


def Registration(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully created an account")
            return redirect('login')
            # user = form.save()
            # login(request, user)
            # return redirect('home')
        else:
            messages.error(request, "")
    else:
        form = UserRegistration
    return render(request, 'news/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginUserForm()
    return render(request, 'news/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')


class HomeNews(ListView):
    model = News
    template_name = 'news/HomeNews.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "News for all world"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related(
            'category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/Home_news_list_by_categories.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True, ).select_related(
            'category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    template_name = 'news/News_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/CreateNews.html'
    login_url = '/admin/'
    # success_url = reverse_lazy('home')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'vitok1223@gmail.com',
                             ['petaykmirzoyan@mail.ru'], fail_silently=False)
            if mail:
                messages.success(request, "You have successfully sent an email")
                return redirect('contact')
            else:
                messages.error(request, 'Sent error')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': "News list",
#     }
#     return render(request, template_name='news/index.html', context=context)
#

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category,
#     }
#     return render(request, template_name='news/category.html', context=context)

# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     context = {
#         "news_item": news_item
#     }
#     return render(request, template_name='news/view_news.html', context=context)


# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     context = {
#         'form': form
#     }
#     return render(request, template_name="news/add_news.html", context=context)
