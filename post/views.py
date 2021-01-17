from django.shortcuts import render,get_object_or_404
from .models import post,Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView ,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from .forms import PostForm,CommentForm
from django.urls import reverse_lazy ,reverse,resolve
from django.http import HttpResponseRedirect
from users.models import Profile
from post.models import post

def home(request):
    follower=[]                       # list of follower following a particular user
    for fol in post.author.Profile.following:
        follower.append(fol)                         # appending list of follower following a particular user
    context={
        'title':'home',
        'post':post.objects.all(),
        'follower':follower
        
    }
    return render(request,'post/home.html',context)


class PostListView(ListView):           # home page of website
    model=post
    template_name='post/home.html'
    context_object_name='post'
    ordering=['-Date']
    paginate_by =  5

class UserPostListView(ListView):       # post posted by user (used only when no one is logged in )
    model=Profile
    template_name='post/user_post.html'
    context_object_name='post'
    ordering=['-Date']
    paginate_by =  5
    
    def get_queryset(self):
        user=get_object_or_404(User , username=self.kwargs.get('username'))
        self.post=post.objects.filter(author=user).order_by('-Date')
        return post.objects.filter(author=user).order_by('-Date')
    
    def get_context_data(self, **kwargs):
        view_profile=Profile.objects.get(user__username=self.kwargs.get('username'))
        context={'post':self.post,'user_v':view_profile}
        return context

class PostDetailView(DetailView):          # detailed view of a post
    model=post
    ordering=['-Date']
    paginate_by =  5
    

   

    
class PostCreateView(LoginRequiredMixin,CreateView):        # create new post
    model=post
    fields=['title','content','image_post']
    template_name='post/post_form.html'

    def form_valid(self, form ):
        form.instance.author=self.request.user       # adding current logged in user to author field of form
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin,UpdateView):  # update existng post
    model=post
    fields=['title','content',]
    def form_valid(self, form ):
        form.instance.author=self.request.user      # adding current logged in user to author field of form
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:          # checking if author of post is same as user trying to edit post
            return True
        return False

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):    # delete post
    model=post
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:           # checking if author of post is same as user trying to edit post
            return True
        return False
    success_url='/home'

def about(request):                                   # about page of website 
    return render(request,'post/about.html',{'title':'about'})  

@login_required            # for liking post
def like_view(request,pk):
    post2=get_object_or_404(post, pk=pk)                                     # retrieving current post queryset
    url_name = resolve(request.path).url_name
    print(url_name)
    if request.user in post2.dislike.all():
        post2.like.add(request.user)
        post2.dislike.remove(request.user)
        return HttpResponseRedirect(reverse('post', args=[str(pk)]))        # redirecting to same page
    else:
        post2.like.add(request.user)
        return HttpResponseRedirect(reverse('post', args=[str(pk)]))        # redirecting to same page


@login_required              # for cancel like on post
def unlike_view(request,pk):
    post2=get_object_or_404(post, pk=pk)                                    # retrieving current post queryset
    post2.like.remove(request.user)
    return HttpResponseRedirect(reverse('post', args=[str(pk)]))        # redirecting to same page


@login_required             # for disliking post
def dislike_view(request,pk):
    post2=get_object_or_404(post, pk=pk)                                 # retrieving current post queryset
    if request.user in post2.like.all():
        post2.dislike.add(request.user)
        post2.like.remove(request.user)
        return HttpResponseRedirect(reverse('post', args=[str(pk)]))        # redirecting to same page
    else:
        post2.dislike.add(request.user)
        return HttpResponseRedirect(reverse('post', args=[str(pk)]))        # redirecting to same page


@login_required            # for cancel dislike on post
def undislike_view(request,pk):
    post2=get_object_or_404(post, pk=pk)                                 # retrieving current post queryset
    post2.dislike.remove(request.user)
    return HttpResponseRedirect(reverse('post', args=[str(pk)]))        # redirecting to same page


@login_required
def post_following(request):
   
    post1=post.objects.filter(author=request.user)
    profile=Profile.objects.get(user=request.user)      #profile of current logged in user
    f_user=[user for user in profile.following.all()]  #list of users we are following 
    posts=[] 
    us=request.user
    usp=Profile.objects.get(user=us)
    for u in f_user:
        p=Profile.objects.get(user=u)
        p_posts=post.objects.filter(author=u)          #post by that user
        for p in p_posts:
            posts.append(p)
    my_posts=[post for post in post1]           # our post 
    posts+=my_posts                             # appending our post to list of posts to be displayed on feed page
    return render(request, 'post/myfeed.html' , {'post2':posts,'u_post':f_user} )

'''class post_following(LoginRequiredMixin,ListView):
    model= post
    paginate_by=5
    context_object_name='posts'
    ordering=['-Date']
    template_name='post/myfeed.html'
    def get_queryset(self,**kwargs):
        self.post_S=post.objects.filter(author=self.request.user)
        self.fol=Profile.objects.filter(user=self.request.user).values('following')
        return self.post_S
        

    def get_context_data(self,**kwargs):
        print(self.fol)
        


        context={'posts1':list(self.post_S)}
        return context'''





class AddCommentView(LoginRequiredMixin,CreateView):        # add comment on a post
    model=Comment
    fields=['body']
    template_name='post/add_comment.html'
    def form_valid(self, form ,*args,**kwargs):
        form.instance.post_id=self.kwargs['pk']               # to  automatically add id of post on which user is commenting
        form.instance.user=self.request.user                  # to automatically commenting user in user field of form
        return super().form_valid(form)

    def get_success_url(self,**kwargs):
        return reverse('post', args=[str(self.kwargs['pk'])])
        
def search(request):        
    if request.method == 'GET':       
        username =  request.GET.get('search')           # term user typed to searched
        status=[]                                   # list of queryset of user matching term searched
        post2=[]                                    # list of queryset of post matching term searched
        qs=Profile.objects.all()                    # full profile queryset
        post_qs=post.objects.all()                  # full profile queryset
        for q in qs :
            if username in q.user.username:
                status.append(q)
        for p in post_qs :
            if username in p.title:
                post2.append(p)
        return render(request,"post/search.html",{'user':status,'post':post2})
    else:
        return render(request,"post/search.html",{})