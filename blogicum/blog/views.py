from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import MAX_POSTS_DISPLAYED
from blog.models import Category, Post


def get_posts(post_objects):
    """Посты из БД."""
    return post_objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('category', 'author', 'location')


def index(request):
    post_list = get_posts(Post.objects).order_by(
        '-pub_date'
    )[:MAX_POSTS_DISPLAYED]
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    posts = get_object_or_404(get_posts(Post.objects), id=post_id)
    context = {
        'post': posts
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_posts(category.posts)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
