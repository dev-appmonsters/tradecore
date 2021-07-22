from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import permissions

from users.serializers import SignupSerializer, UserSerializer


User = get_user_model()


class SignupView(generics.CreateAPIView):

    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        serializer.save(ip_address=self.request.META["REMOTE_ADDR"])


signup_view = SignupView.as_view()


class UserDetailView(generics.RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


user_detail_view = UserDetailView.as_view()
