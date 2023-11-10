from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.core.cache import cache
from sitewomen import settings
from .forms import AddPostForm, UploadFileForm, ContactForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        w_lst=cache.get('women_posts')
        if not w_lst:
            w_lst=Women.published.all().select_related('cat')
            cache.set('women_posts', w_lst, 60)
        return w_lst
        # return Women.published.all().select_related('cat')

@login_required
def about(request):
    contact_list=Women.published.all()
    paginator=Paginator(contact_list,3)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(LoginRequiredMixin,DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w=form.save(commit=False)
        w.author=self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model=Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = "women.change_women" #<приложение>.<действие>_<таблица>


class DeletePage(LoginRequiredMixin, DataMixin,DeleteView):
    model = Women
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page= 'Удаление статьи'


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        message = f"{form.cleaned_data['content']}.Будьте любезны ответить на E-mail {form.cleaned_data['email']}"
        send_mail(
            form.cleaned_data['name'],
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return super().form_valid(form)





class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        # cat = Category.objects.get(slug=self.kwargs['cat_slug']) можно и так
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        # tag = context['posts'][0].tags.first() # можно так
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
