from .forms import InquiryForm, DiaryCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from diary.models import Diary
from django.contrib import messages
from django.urls import reverse_lazy
import logging
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from.forms import InquiryForm


logger = logging.getLogger(__name__)

# Create your views here.


def index(request):
    return render(request, 'satou/index.html')


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('satou:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


from.models import Diary


class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_list.html'

    def get_queryset(self):
        blogs = Blog.objects.filter(
            user=self.request.user).order_by('-created_at')
        return blogs


class BlogDetaillView(LoginRequiredMixin, generic.DetailView):
    model = Blog
    template_name = 'blog_detail.html'


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    template_name = 'blog_create.html'
    form_class = BlogCreateForm
    success_url = reverse_lazy('satou:blog_list')

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        messages.success(self.request, 'ブログを作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ブログの作成に失敗しました。')
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    form_class = BlogCreateForm

    def get_success_url(self):
        return reverse_lazy('satou:blog_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'ブログを更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'ブログの更新に失敗しました。')
        return super().form_invalid(form)


class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def delete(self,request,*args,**kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request, *args, **kwargs)
