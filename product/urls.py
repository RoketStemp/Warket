from django.urls import path

from . import views


urlpatterns = [
    path('search/', views.searchProduct),
    path('<slug:category_slug>/', views.ShowCategoryProductListView.as_view()),

    path('<slug:category_slug>/<slug:product_slug>/', views.ShowProductDetailsView.as_view()),

    path('<slug:category_slug>/<slug:product_slug>/comments', views.ShowProductCommentsListView.as_view()),
    path('<slug:category_slug>/<slug:product_slug>/comments/add', views.addComment),
    path('<slug:category_slug>/<slug:product_slug>/comments/delete', views.deleteComment),
    path('<slug:category_slug>/<slug:product_slug>/comments/edit', views.editComment),
    path('<slug:category_slug>/<slug:product_slug>/comments/add_reply', views.addCommentReply),

    
]

