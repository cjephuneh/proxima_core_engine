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
            'thread_id': 'thread_id',
            'client_id': 'client_id',
        }

        # make sure thread is specified
        if not params.get('thread_id'):
            return Response({ 'error': 'thread_id missing' })
        
        filters = get_filter_from_params(params, allowed_params)

        comment_query = Comment.objects.prefetch_related('thread', 'likes').filter(**filters)
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
        if not created:
            return Response({'error': 'Failed to create comment'}, status=400)
        
        comment_info = CommentSerializer(comment)
        if created:
            response = { 'error': False, 'data': comment_info.data}
            return Response(response, status=201)
        # else:
        #     return Response(comment_info.data, status=200)


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
            'thread_id': 'thread_id',
            'comment_id': 'comment_id'
        }
        filters = get_filter_from_params(params, required_params, required=True)
        if filters is None:
            return Response({'error': 'Provide the required fields'}, status=400)

        comment_query = Comment.objects.filter(**filters)
        delete_count, delete_type = comment_query.delete()
        response_data = {
            'count': delete_count,
            'type': delete_type
        }

        if response_data['count'] == 0:
            return Response({'error': 'Does not exist'}, status=400)

        return Response(response_data, status=200)
    
    

class LikeCommentApiView(APIView):
    # def post(self, request, post_pk, comment_id, *args, **kwargs):
    def post(self, request,):
        comment_id = request.query_params.get('comment_id')
        client_id = request.query_params.get('client_id')
        # print(type(comment_id))

        # Retrieve the comment object based on provided comment_id parameter
        try:
            comment = Comment.objects.get(comment_id=comment_id)
        except Comment.DoesNotExist:
            return Response('Comment does not exist')
        
        is_dislike = False

        # 
        for dislike in comment.dislikes.all():
            # if dislike == request.client:
            if dislike == client_id:
                is_dislike = True
                break
        if is_dislike:
            # comment.dislikes.remove(request.client)
            comment.dislikes.remove(client_id)
        is_like = False
        for like in comment.likes.all():
            # if like == request.client:
            if like == client_id:
                is_like = True
                break
        if not is_like: 
            # comment.likes.add(request.client)
            comment.likes.add(client_id)
        
        if is_like:
            # comment.likes.remove(request.client)
            comment.likes.remove(client_id)
        return Response("Comment liked", status=200)

class LikeOrDislikeCommentApiView(APIView):
    def post(self, request):
        comment_id = request.query_params.get('comment_id')
        client_id = request.query_params.get('client_id')

        if not comment_id:
            return Response({'error': 'comment_id missing'}, status=400)
        
        if not client_id:
            return Response({'error': 'client_id missing'}, status=400)

        # Retrieve the comment object based on the provided comment_id parameter
        try:
            comment = Comment.objects.get(comment_id=comment_id)
        except Comment.DoesNotExist:
            return Response({ 'error':'Comment does not exist' }, status=400)

        # Check if the client_id already exists in the likes or dislikes
        is_like = comment.likes.filter(id=client_id).exists()
        is_dislike = comment.dislikes.filter(id=client_id).exists()

        if is_like:
            comment.likes.remove(client_id)  # Remove the like
        elif is_dislike:
            comment.dislikes.remove(client_id)  # Remove the dislike
            comment.likes.add(client_id)  # Add the like
        else:
            comment.likes.add(client_id)  # Add the like

        return Response({ "message": "Like toggled for comment" }, status=200)


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