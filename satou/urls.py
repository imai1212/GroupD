from django.urls import path
from . import views

app_name = 'satou'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('blog_list/', views.BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>',
         views.BlogDetaillView.as_view(), name='blog_detail'),
    path('blog-create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog-update/<int:pk>/',
         views.BlogUpdateView.as_view(), name="blog_update"),
    path('blog-delete/<int:pk>/',
         views.BlogDeleteView.as_view(), name="blog_delete"),
]
