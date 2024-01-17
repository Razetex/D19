from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ReplyCreate, Replies, ReplyConfirmed,\
   ReplyDelete, CategoryList, subscribe, RepliesSorted


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/reply/', ReplyCreate.as_view(), name='reply_create'),

    path('my_replies/', Replies.as_view(), name='replies_user'),
    path('reply/<int:pk>/update/', ReplyConfirmed.as_view(), name='reply_update'),
    path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),

    path('categories/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('replies_sorted/<int:pk>/', RepliesSorted.as_view(), name='replies_sorted_list'),
    ]