from django.urls import path
from django.contrib.auth import views

from user.views import( 
    signup,
    hobb, 
   	profile,
    # ProfileDetailView, 
    biodata,
    gallery, interest, profile_update,
    other_profiles, other_gallery,
    other_interest
    )

urlpatterns = [
    path('signup/', signup, name='signup' ),
    path('login/', views.LoginView.as_view(
        template_name='registration/login.html'
        ),
         name='login'),
    path('logout/', views.LogoutView.as_view(
        template_name='registration/logout.html'
        ),
         name='logout'),
    path('password-change/', views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'
        ),
         name='password_change'),
    path('password-reset/', views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'
        ),
         name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(
        template_name='registration/password_resetdone.html'
        ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(
        template_name='registration/password_resetconfirm.html'
        ),
         name='password_reset_confirm'),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(
        template_name='registration/password_complete.html'
        ),
         name='password_reset_complete'),

    #gallery url
    path('gallery', gallery, name='gallery'),

    path('hobbies/', hobb, name='hobbies'),

    path('profile/', profile, name='profile'),
    # path('otherprofiles/<slug:slug>/', ProfileDetailView.as_view(), name='otherprofiles'),
    

    path('biodata/', biodata, name='biodata'),
    path('interest/', interest, name='interest'),
    
    path('profile_update/', profile_update, name='profile_update'),

    path('otherprofiles/<slug:slug>/', other_profiles, name='otherprofiles'),
    path('othergallery/<slug:slug>/', other_gallery, name='other_gallery'),
    path('otherinterest/<slug:slug>/', other_interest, name='other_interest' ),

]
