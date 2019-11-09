from django.urls import path, include, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'app'

urlpatterns = \
    [
        path('', views.BaseLayout.as_view(), name='default'),
        path('about/', views.About.as_view(), name='about'),
        path('map/', views.MapPage.as_view(), name='map_page'),

        path('login/', auth_views.LoginView.as_view(
            template_name='App/login.html',
            redirect_authenticated_user=True,
        ), name='login'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('password_change/', auth_views.PasswordChangeView.as_view(
            template_name='App/password_change_form.html',
            success_url=reverse_lazy('app:password_change_done'),
        ), name='password_change'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='App/password_change_done.html'
        ), name='password_change_done'),
        path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='App/password_reset_form.html',
            subject_template_name='App/password_reset_subject.txt',
            email_template_name='App/password_reset_email.html'
            # success_url=reverse_lazy('app:password_reset_done'),
        ), name='password_reset'),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='App/password_reset_done.html'
        ), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='App/password_reset_confirm.html'
        ), name='password_reset_confirm'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='App/password_reset_complete.html'
        ), name='password_reset_complete'),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
