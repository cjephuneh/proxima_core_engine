import logging

from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core_engine_community_app.models import Comment
from core_engine_community_app.serializers import CommentSerializer
from core_engine_community_app.utils import save_client_comment
from core_engine_utils_app.views import get_filter_from_params

log = logging.getLogger(__name__)


class CommentView(APIView):
    """
    Comments API View
    """

    def get(self, request, format=None):
        """
        GET
        Retrieve Comments matching query.

        Params:
        comment_id
        thread
        client
        issue
        """
        # Validate params args
        params = request.query_params
        allowed_params = {
            'comment_id': 'comment_id',
            'thread': 'thread',
            'client': 'client',
            'issue': 'issue'
        }
        filters = get_filter_from_params(params, allowed_params)

        comment_query = Comment.objects.prefetch_related('comment_id').filter(**filters)
        comment_set = CommentSerializer(comment_query, many=True)
        return Response(comment_set.data, status=200)


    def post(self, request, format=None):
        """
        POST
        Add client comment

        Params:
        comment_id
        thread
        """
        comment, created = save_client_comment(**request.data)
        if not comment:
            return Response(status=400)
        
        comment_info = CommentSerializer(comment)
        if created:
            return Response(comment_info.data, status=201)
        else:
            return Response(comment_info.data, status=200)


    def delete(self, request, format=None):
        """
        DELETE
        Remove a comment from the database.
        comment_id
        thread
        """
        # Validate params args
        params = request.query_params
        required_params = {
            'course_id': 'course_id',
            'thread': 'thread'
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response(status=400)

        comment_query = Comment.objects.prefetch_related('comment').filter(**filters)
        delete_count, delete_type = comment_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        return Response(response_data, status=200)
    
    

class LikeCommentApiView(APIView):
    def post(self, request, post_pk, comment_id, *args, **kwargs):
        comment = Comment.objects.get(pk=comment_id)
        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.client:
                is_dislike = True
                break
        if is_dislike:
            comment.dislikes.remove(request.client)
        is_like = False
        for like in comment.likes.all():
            if like == request.client:
                is_like = True
                break
        if not is_like: 
            comment.likes.add(request.client)
        
        if is_like:
            comment.likes.remove(request.client)
        return Response("Comment liked", status=200)

class DislikeCommentApiView(APIView):
    def post(self, request, post_pk, comment_id, *args, **kwargs):
        comment = Comment.objects.get(pk=comment_id)
        is_like = False
        for like in comment.likes.all():
            if like == request.client:
                is_like = True
                break
        if is_like:
            comment.likes.remove(request.client)
        is_dislike = False
        for dislike in comment.dislikes.all():
            if dislike == request.client:
                is_dislike = True
                break
        if not is_dislike: 
            comment.dislikes.add(request.client)
        
        if is_dislike:
            comment.dislikes.remove(request.client)

        return Response("Comment disliked", status=200)