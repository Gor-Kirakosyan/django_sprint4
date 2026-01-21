from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Post, Category, Comment
from .forms import CreationForm, PostForm, CommentForm
from django.http import HttpResponseForbidden

def index(request):
    posts = Post.objects.select_related('author', 'category', 'location').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        id=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {
        'post': post
    }
    return render(request, template, context)

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    posts = Post.objects.select_related('author', 'category', 'location').filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {'category': category, 'page_obj': page_obj})

def signup(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreationForm()
    return render(request, 'registration/registration.html', {'form': form})

def profile(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    
    # АВТОР ВИДИТ ВСЕ СВОИ ПОСТЫ (включая отложенные и неопубликованные)
    if request.user == user:
        posts = Post.objects.filter(author=user).order_by('-pub_date')
    else:
        # Другие видят только опубликованные посты
        posts = Post.objects.filter(
            author=user,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {
        'profile_user': user, 
        'page_obj': page_obj,
        'now': timezone.now()  # для проверки отложенных постов
    })

@login_required
def edit_profile(request):
    from django.contrib.auth.forms import UserChangeForm
    
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # ПЕРЕНАПРАВЛЯЕМ НА СТРАНИЦУ ПРОФИЛЯ АВТОРА
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})

@login_required
def edit_post(request, post_id):
    """Редактирование публикации."""
    post = get_object_or_404(Post, id=post_id)
    
    # Проверка прав: только автор может редактировать
    if post.author != request.user:
        return redirect('blog:post_detail', id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/create.html', {'form': form})

@login_required
def add_comment(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post_detail', id=post_id)

@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    
    # Проверка прав: только автор может редактировать
    if comment.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот комментарий")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=post_id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})

@login_required
def delete_post(request, post_id):
    """Удаление публикации."""
    post = get_object_or_404(Post, id=post_id)
    
    # Проверка прав: только автор может удалить
    if post.author != request.user:
        return redirect('blog:post_detail', id=post_id)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    
    # GET запрос: показываем страницу подтверждения
    return render(request, 'blog/create.html', {
        'form': None,  # Форма не нужна для удаления
        'delete_confirmation': True,
        'object': post,
        'object_type': 'post'
    })

@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    
    # Проверка прав: только автор может удалить
    if comment.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот комментарий")
    
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post_id)
    
    # GET запрос: показываем страницу подтверждения
    return render(request, 'blog/comment.html', {
        'form': None,
        'comment': comment,
        'delete_confirmation': True,
        'object_type': 'comment'
    })
