from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Rate
from .forms import PostForm, RateForm
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.models import User

from django.http import HttpRequest, HttpResponse


class PostListView(ListView):
    model = Post
    template_name = 'post/posts_home.html'
    context_object_name = 'posts'
    ordering = ['-created']

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query == None or query == " ":
            query = ''

        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tag__icontains=query) | Q(author_id__username__icontains=query)
            )
        return object_list.order_by('-created')
    
class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created')

def detail_post(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.rate_set.all().order_by('-updated')

    try:
        rated = comments.get(rater=request.user)
    except:
        rated = {''}

    if request.method == 'POST':
        rating = Rate.objects.create(
            rater = request.user,
            post = post,
            is_rated = request.POST.get('is_rated'),
            comment = request.POST.get('comment'),
        )

        if request.POST.get('is_rated') == '1':
            post.rate_one += 1
        if request.POST.get('is_rated') == '2':
            post.rate_two += 1
        if request.POST.get('is_rated') == '3':
            post.rate_three += 1
        if request.POST.get('is_rated') == '4':
            post.rate_four += 1
        if request.POST.get('is_rated') == '5':
            post.rate_five += 1

        post.save()
        return redirect('detail_post', pk=post.id)

    print(request.POST.get('is_rated'))


    context = {'post': post, 'comments':comments, 'rated':rated}
    return render(request, 'post/detail_post.html', context)


@login_required(login_url='login')
def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts_home')
        
    context = {'form':form}
    return render(request, 'post/posts_form.html', context)
    
@login_required(login_url='login')
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.user != post.author:
        return redirect('posts_home')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detail_post', pk)

    context = {'form':form}
    return render(request, 'post/posts_form.html', context)


@login_required(login_url='login')
def update_comment(request, pk):
    comment = Rate.objects.get(id=pk)
    form = RateForm(instance=comment)
    post = Post.objects.get(id=comment.post.id)

    if request.user != comment.rater:
        return redirect('posts_home')

    if request.method == 'POST':
        form = RateForm(request.POST, instance=comment)
        if form.is_valid():

            if comment.is_rated == 1:
                post.rate_one -= 1
            if comment.is_rated == 2:
                post.rate_two -= 1
            if comment.is_rated == 3:
                post.rate_three -= 1
            if comment.is_rated == 4:
                post.rate_four -= 1
            if comment.is_rated == 5:
                post.rate_five -= 1
                
            if request.POST.get('is_rated') == '1':
                form.instance.is_rated = 1
                post.rate_one += 1
            if request.POST.get('is_rated') == '2':
                form.instance.is_rated = 2
                post.rate_two += 1
            if request.POST.get('is_rated') == '3':
                form.instance.is_rated = 3
                post.rate_three += 1
            if request.POST.get('is_rated') == '4':
                form.instance.is_rated = 4
                post.rate_four += 1
            if request.POST.get('is_rated') == '5':
                form.instance.is_rated = 5
                post.rate_five += 1

            post.save()
            form.save()

            return redirect('detail_post', post.id)
            

    context = {'form':form}
    return render(request, 'components/edit_rating.html', context)

def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.author:
        return redirect('posts_home')

    if request.method == 'POST':
        post.delete()
        return redirect('posts_home')

    return render(request, 'components/delete.html', {'obj':post})

@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Rate.objects.get(id=pk)
    post = Post.objects.get(id=comment.post.id)

    if request.user != comment.rater:
        return redirect('posts_home')

    if request.method == 'POST':
        if comment.is_rated == 1:
            post.rate_one -= 1
        if comment.is_rated == 2:
            post.rate_two -= 1
        if comment.is_rated == 3:
            post.rate_three -= 1
        if comment.is_rated == 4:
            post.rate_four -= 1
        if comment.is_rated == 5:
            post.rate_five -= 1


        post.save()

        comment.delete()
        return redirect('detail_post', post.id)

    return render(request, 'components/delete.html', {'obj':comment})
