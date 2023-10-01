# views.py
from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer
import os
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from io import BytesIO
from django.shortcuts import get_object_or_404

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    parser_classes = [MultiPartParser, FormParser]  # Specify the parsers here

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        video_blob = request.data.get('video_blob')  # Assuming the blob data is sent with the name 'video_blob'

        if title is None or video_blob is None:
            return Response({'error': 'Title and video_blob are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        video = Video(title=title, description=description)
        video.save()

        # Create a BytesIO buffer to append and store the video stream
        video_stream = BytesIO()

        # Iterate through chunks and append them to the buffer
        for chunk in video_blob.chunks():
            video_stream.write(chunk)

        # If this is the final chunk, save the compiled video
        if 'HTTP_X_FINAL_CHUNK' in request.META:
            video_blob_path = os.path.join(settings.MEDIA_ROOT, 'video_blob.mp4')  # Adjust file extension as needed
            with open(video_blob_path, "wb") as video_blob_file:
                video_blob_file.write(video_stream.getvalue())

        return Response({'status': 'Video chunk uploaded'}, status=status.HTTP_201_CREATED)

    def get_single_video(self, video_id):
        try:
            # Retrieve the video object by its ID, or return None if not found
            video = Video.objects.get(id=video_id)
            return video
        except Video.DoesNotExist:
            return None

    def get(self, request, video_id=None):
        # If video_id is provided in the URL, retrieve a single video by its ID
        if video_id is not None:
            video = self.get_single_video(video_id)
            if video:
                serializer = VideoSerializer(video)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        # If no video_id is provided in the URL, list all videos (default behavior)
        return super().list(request)

class TranscriptAPIView(APIView):
    def get(self, request, video_id):
        try:
            # Retrieve the video object by its ID, or return a 404 error if not found
            video = get_object_or_404(Video, id=video_id)
            transcript = video.transcript
            return Response({"transcript": transcript}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
