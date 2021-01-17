from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Profile
from post.models import post
from django.views.generic import ListView, DetailView

@login_required
def follow_unfollow(request):                                       # initiated when follow or unfollow button is clicked
    template ='users/details.html'
    context={}
    context['post'] = 'Post'
    if request.method=='POST':
        my_profile=Profile.objects.get(user=request.user)           # retrieving profile of user who pressed follow/unfollow button
        pk1= request.POST.get('profile_pk')                         # primary key of user we visit
        obje = Profile.objects.get(pk=pk1)
        if obje.user in my_profile.following.all():
            my_profile.following.remove(obje.user)
        else:
            my_profile.following.add(obje.user)
        return redirect(request.META.get('HTTP_REFERER')   )
    return redirect('profile-detail' , kwargs={ 'post': Post})


def register(request):          # to register new users
    if request.method=='POST':
        form =UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')      # retrieve username from submitted form 
            messages.success(request, f'Account created successfully!')        # success message
            
            return redirect('login')
    else:
        form=UserRegisterForm()  
    return render(request, 'users/register.html',{'form':form})

@login_required
def profile(request):               # used to update profile of logged in user
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) 
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')    #  success message diplayeed on updating profile
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html',context)

class ProfileListView(ListView):                # find section of website (displays list of user signed up on website)
    model=Profile
    template_name='profile_list.html'
    context_object_name='profiles'
    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)   # list is passed excluding ourselves



class ProfileDetailView(ListView):           # detailed view of profile (showed when some user is logged in )
    model=Profile
    template_name='users/details.html'
    context_object_name = 'posts'
    paginate_by =  5
    
    def get_queryset(self):
        user=get_object_or_404(User, id=self.kwargs.get('pk'))
        self.posts=post.objects.filter(author=user).order_by('-Date')
        return post.objects.filter(author=user).order_by('-Date')

    def get_context_data(self, **kwargs):
        
        view_profile=Profile.objects.get(user__id=self.kwargs.get('pk'))        # profile of user whom we visit
        usp=get_object_or_404(Profile , user=self.request.user)        # profile of user who visit
        if view_profile.user in usp.following.all():
            follow=True
        else:
            follow=False
        post_u=post.objects.filter(author=view_profile.user)
        context={'user1':usp,'follow':follow,'posts':self.posts,'profile_v':view_profile}
        return context
        

    


