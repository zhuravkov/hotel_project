from django.urls import path

from api_app.views import apiLoginView, authenticateApi, categories_view



urlpatterns = [
    path('auth/me',  authenticateApi ),
    path('login', apiLoginView),
    path('categories', categories_view),

]






    # path('api/users/',  userProfileApi ),
    # path('api/posts/',  PostApiView.as_view() ),
    # path('api/profile/<int:pk>',  UserDetailView.as_view() ),
    # path('api/auth/me/',  authenticateApi ),
    # path('api/follow/<int:pk>', followToggle), #follow/unfollow

    # path('api/profile/status', StatusUpdateView.as_view()), #PUT change self status

    # path('api/profile/status/<int:id>', getStatus), #GET get user's status

    # path('api/login', apiLoginView),
    # # path('api/logout', logout_view),  