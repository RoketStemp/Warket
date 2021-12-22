from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from django.http.response import Http404

from rest_framework.views import APIView
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

import product

from .models import Computers, Laptops, Comment, Product
from .serializers import CommentSerializer, ComputerSerializer, LaptopSerializer


class ShowCategoryProductListView(APIView):
    """Show products by category_slug in product"""
    def get(self, request, category_slug, format=None):
        serializer = _getProductSerializer(category_slug)
        return Response(serializer.data)


class ShowProductDetailsView(APIView):
    """Show product details by product_slug in product"""
    def get(self, request, category_slug, product_slug, format=None):
        serializer = _getProductSerializer(category_slug, product_slug)
        return Response(serializer.data)


class ShowProductCommentsListView(APIView):
    """Show comments related to product"""
    def get(self, request, category_slug, product_slug, format=None):
        serializer = _getProductSerializer(category_slug, product_slug)
        return Response(serializer.data['comments'])


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def addComment(request, category_slug, product_slug):
    """Validate comment data and add comment to product"""
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        
        try:
            comment = _createCommentFromProduct(
                author=request.user.id,
                data=serializer.data,
                category_slug=category_slug,
                product_slug=product_slug
            )

            return Response({
                    'username':request.user.username, 
                    'date_added': comment.date_added, 
                    'id':comment.id,
                    'text':comment.text,
                    'rating':comment.rating,
                    'advantages':comment.advantages,
                    'disadvantages':comment.disadvantages,
                }, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def deleteComment(request, category_slug, product_slug):
    """Delete comment by comment id gotten from request.data['id']"""
    Comment.objects.filter(id=request.data['id']).delete()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def editComment(request, category_slug, product_slug):
    """Edit comment by comment id gotten from request.data['id']"""
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        
        try:
            comment = _editComment(
                comment_id=request.data['id'],
                data=serializer.data
            )
            
            return Response({
                    'username':request.user.username, 
                    'date_added': comment.date_added, 
                    'id':comment.id,
                    'text':comment.text,
                    'rating':comment.rating,
                    'advantages':comment.advantages,
                    'disadvantages':comment.disadvantages,
                }, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def addCommentReply(request, category_slug, product_slug):
    """Add reply to comment by comment id gotten from request.data['id']"""
    try:
        reply = _createReplyToComment(author=request.user, text=request.data['text'], comment_id=request.data['id'])
        
        return Response({
                    'username':request.user.username, 
                    'date_added': reply.date_added, 
                    'id':reply.id,
                    'text':reply.text,
                }, status=status.HTTP_202_ACCEPTED)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def searchProduct(request):
    """Search product by product name or description gotten from request.data['query']"""
    try:
        query = request.data.get('query', '')
        result = []
        for category in Product.__subclasses__():
            for product in category.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)):
                if product.category.name == 'Laptops':
                    result.append(LaptopSerializer(product).data)
                elif product.category.name == 'Computers':
                    result.append(ComputerSerializer(product).data)

        return Response(result, status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def _getProductSerializer(category_slug, product_slug=None):
    """Function choose product serializer by caregory and product slug"""
    try:
        if product_slug:
            if category_slug=='laptops':
                laptops = Laptops.objects.get(slug=product_slug)
                serializer = LaptopSerializer(laptops)
            elif category_slug=='computers':
                computers = Computers.objects.get(slug=product_slug)
                serializer = ComputerSerializer(computers)
        else:
            if category_slug=='laptops':
                laptops = Laptops.objects.all()
                serializer = LaptopSerializer(laptops, many=True)
            elif category_slug=='computers':
                computers = Computers.objects.all()
                serializer = ComputerSerializer(computers, many=True)
    except ObjectDoesNotExist:
        raise Http404

    return serializer


def _getProduct(category_slug):
    """Return product object by category slug"""
    if category_slug=='laptops':
        return Laptops
    elif category_slug=='computers':
        return Computers


def _createCommentFromProduct(author, data, category_slug, product_slug):
    """Create new comment to product and return it"""
    comment = Comment.objects.create(
        author = author,
        text = data['text'],
        rating = data['rating'],
        advantages = data['advantages'],
        disadvantages = data['disadvantages'],
    )
            
    products = _getProduct(category_slug)

    p = products.objects.get(slug=product_slug)
    p.comments.add(comment)
    p.save()

    return comment


def _editComment(comment_id, data):
    """Edit comment"""
    comment = Comment.objects.get(id=comment_id)

    comment.text = data['text']
    comment.advantages = data['advantages']
    comment.disadvantages = data['disadvantages']
    comment.rating = data['rating']

    comment.save()


def _createReplyToComment(author, text, comment_id):
    """Create reply to comment and return it"""
    reply = Comment.objects.create(author=author, text=text, is_reply=True, rating=1)

    comment = Comment.objects.get(id=comment_id)
    comment.comment.add(reply)
    comment.save()

    return reply