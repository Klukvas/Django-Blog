import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post
from ..serializers import PostSerializer
import  datetime


client = Client()


    # initialize the APIClient app
class GetAllPuppiesTest(TestCase):
    """ Test module for GET all puppies API """
    # def setUp(self):
    #     Post.objects.create(
    #         title='TestCase1', text='TestCase1', date=datetime.now(), autor='admin')
    #     Post.objects.create(
    #         title='TestCase2', text='TestCase2', date=datetime.now(), autor='admin')

    def test_get_all_puppies(self):
        # get API response
        response = client.get(reverse('get_post_puppies'))
        # get data from db
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'id': 2})) self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)