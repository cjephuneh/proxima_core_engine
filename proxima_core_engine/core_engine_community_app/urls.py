from django.urls import include, path, re_path

from core_engine_auth_app.views.signin import LoginAPIView
from core_engine_community_app.views import (
    CommunityView, ThreadView, IssueView, CommentView, JoinCommunityView, LeaveCommunityView,
    LikeCommentApiView, DislikeCommentApiView
)

app_name="core_engine_community_app"


urlpatterns = [
    re_path(r'^api/community/', include([
        # Signin
        re_path(r'^community/$', CommunityView.as_view(), name='core_community_setup'),
        re_path(r'^joincommunity/$', JoinCommunityView.as_view(), name='core_community_join'),
        re_path(r'^leavecommunity/$', LeaveCommunityView.as_view(), name='core_community_leave'),
        re_path(r'^thread/$', ThreadView.as_view(), name='core_community_thread'),
        re_path(r'^issue/$', IssueView.as_view(), name='core_community_issue'),
        re_path(r'^comment/$', CommentView.as_view(), name='core_community_comment'),
        re_path(r'^likecomment/$', LikeCommentApiView.as_view(), name='core_community_like_comment'),
        re_path(r'^dislikecomment/$', DislikeCommentApiView.as_view(), name='core_community_dislikecomment'),

    ]))
]