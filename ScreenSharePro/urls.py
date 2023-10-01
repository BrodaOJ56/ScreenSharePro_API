# urls.py
from django.urls import path
from .views import VideoListCreateView, TranscriptAPIView


urlpatterns = [
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('transcript/<int:video_id>/', TranscriptAPIView.as_view(), name='transcript-api'),
    path('videos/<int:video_id>/', VideoListCreateView.as_view(), name='video-detail'),
]

