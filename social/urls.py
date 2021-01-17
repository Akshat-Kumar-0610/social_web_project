from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from post import views as post_views
from post import urls as post_urls
from users.views import ProfileListView,ProfileDetailView,follow_unfollow
from users import views as users_views

from post.views import PostListView,UserPostListView, PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,AddCommentView
from post import views
urlpatterns = [
    path('admin/', admin.site.urls),                                                                                                                                                        # admin page
    path('home/', PostListView.as_view() , name='home'),                                                                                                                                    # home page
    path('', PostListView.as_view(), name='home'),                                                                                                                                          # home page
    path('about/', post_views.about, name='about'),                                                                                                                                         # about page
    path('register/', users_views.register, name='register'),                                                                                                                               # new registration page
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html') , name='login'),                                                                                          # login page
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html') , name='logout'),                                                                                      # logout view displaying "you have been logged out " message
    path('profile/', users_views.profile, name='profile'),                                                                                                                                  # Edit profile page where we can edit our profile 
    path('myfeed/', post_views.post_following, name='myfeed'),                                                                                                                              # my feed page
    path('post/<pk>/', PostDetailView.as_view(), name='post'),                                                                                                                              # post detail view (follow unfollow button here)
    path('create/', include('post.urls'), name='post-create'),                                                                                                                              # create new post
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),                                                                                                                # post update view
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),                                                                                                                # post delete view
    path('user/<username>', UserPostListView.as_view(), name='user'),                                                                                                                       # user profile page(displayed when not logged in)
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),                                                        # password reset form
    path('passwowrd-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),                                    # pass reset message(email) sent page
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),        # page to enter new password
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),                     # pass reset complete page
    path('post/<int:pk>/comment/',AddCommentView.as_view(), name='comment'),                                                                                                                # comment page to comment on post                                                                                                             # post detail view (dispalyed when someone loggd in)
    path('profile/list/', ProfileListView.as_view(), name='profile-list'),                                                                                                                  # find people page (list of users signed up)
    path('userprofile/<pk>/', ProfileDetailView.as_view(), name='profile-detail'),                                                                                                          # profile detail view (shown when someone logged in)
    path('follow/', users_views.follow_unfollow,name='follow_unfollow'),                                                                                                                    # for follow-unfollow (doesnt actually render anything)
    path('like/<pk>', post_views.like_view, name='like_post'),                                                                                                                              # to like
    path('dislike/<pk>', post_views.dislike_view, name='dislike_post'),                                                                                                                     # to dislike
    path('unlike/<pk>', post_views.unlike_view, name='unlike_post'),                                                                                                                        # to undo like 
    path('undislike/<pk>', post_views.undislike_view, name='undislike_post'),                                                                                                                # to undo dislike
    path('search/', post_views.search, name='search'),   
    path('accounts/', include('allauth.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


