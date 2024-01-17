from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
# from .tasks import send_message_reply_created, send_message_confirmed
from .forms import PostForm, ReplyForm
from .models import Author, Post, Categories, Reply


class PostList(ListView):
    model = Post
    ordering = '-time creating'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        f = form.save(commit=False)
        user = self.request.user
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            author = Author.objects.create(user=user)
        post = form.save(commit=False)
        post.author = author
        post.save()
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    template_name = 'reply_create.html'
    model = Reply

    def form_valid(self, form):
        reply = form.save(commit=False)
        if self.request.method == 'POST':
            pk = self.request.path.split('/')[-3]
            sender = self.request.user
            reply.post = Post.objects.get(id=pk)
            reply.sender = User.objects.get(username=sender)
        reply.save()

        post = reply.post
        author = post.author
        email = author.user.email
        send_message_reply_created.delay(email)
        return super().form_valid(form)

    def get_success_url(self):
        url = '/'.join(self.request.path.split('/')[0:-2])
        return url

class Replies(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'replies_user.html'
    context_object_name = 'replies'
    ordering = '-date_created'
    paginate_by = 5

    def get_queryset(self):
        self.queryset = Reply.objects.filter(post__author__user_id=self.request.user.id)
        return super().get_queryset()


class CategoryList(ListView):
    model = Post
    template_name = 'categories.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        self.category = get_object_or_404(Categories, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Categories.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Поздравляем! Вы  подписались на рассылку категории - '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class ReplyConfirmed(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'reply_confirmed.html'
    form_class = ReplyForm
    context_object_name = 'confirmed'
    success_url = 'replies/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        reply_id = self.kwargs.get('pk')
        Reply.objects.filter(pk=reply_id).update(confirmed=True)

        email = self.request.user.email
        send_message_confirmed(email)
        return data


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'reply_confirm_delete.html'
    success_url = reverse_lazy('my_replies')


class RepliesSorted(ListView):
    model = Reply
    template_name = 'sorted_replies.html'
    context_object_name = 'sorted_replies'
    paginate_by = 6

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post.replies.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

