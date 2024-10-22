from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .enums import TokenType
from .services import TokenService, UserService, SendEmailService
import random
from .models import CustomUser, Author, Follow, Notification

from rest_framework import status, permissions, parsers, exceptions, generics
from rest_framework.generics import ListAPIView

from .serializers import (
    UserSerializer,LoginSerializer,
    ValidationErrorSerializer,
    TokenResponseSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    ForgotPasswordRequestSerializer,
    ForgotPasswordVerifyRequestSerializer,
    ResetPasswordResponseSerializer,
    ForgotPasswordVerifyResponseSerializer,
    ForgotPasswordResponseSerializer,
    RecommendationSerializer, FollowSerializer,
    NotificationSerializer)
from .services import TokenService, UserService, SendEmailService, OTPService

from django.contrib.auth.hashers import make_password
from secrets import token_urlsafe
from .errors import ACTIVE_USER_NOT_FOUND_ERROR_MSG
from django.contrib.auth import get_user_model
from django.db.models import Sum

from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import  Recommendation

User = get_user_model()

@extend_schema_view(
    post=extend_schema(
        summary="Sign up a new user",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: ValidationErrorSerializer
        }
    )
)
class SignupView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
                'user': user_data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@extend_schema_view(
    post=extend_schema(
        summary="Log in a user",
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            400: ValidationErrorSerializer,
        }
    )
)
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Hisob maʼlumotlari yaroqsiz'}, status=status.HTTP_401_UNAUTHORIZED)



@extend_schema_view(
    get=extend_schema(
        summary="Get user information",
        responses={
            200: UserSerializer,
            400: ValidationErrorSerializer
        }
    ),
    patch=extend_schema(
        summary="Update user information",
        request=UserUpdateSerializer,
        responses={
            200: UserUpdateSerializer,
            400: ValidationErrorSerializer
        }
    )
)
class UsersMe(generics.RetrieveAPIView, generics.UpdateAPIView):
    http_method_names = ['get', 'patch']
    queryset = User.objects.filter(is_active=True)
    parser_classes = [parsers.MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer

    def patch(self, request, *args, **kwargs):
        redis_conn = get_redis_connection('default')
        redis_conn.set('test_key', 'test_value', ex=3600)
        cached_value = redis_conn.get('test_key')
        print(cached_value)

        return super().partial_update(request, *args, **kwargs)

@extend_schema_view(
    post=extend_schema(
        summary="Log out a user",
        request=None,
        responses={
            200: ValidationErrorSerializer,
            401: ValidationErrorSerializer
        }
    )
)
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=None)
    def post(self, request, *args, **kwargs):
        UserService.create_tokens(request.user, access='fake_token', refresh='fake_token', is_force_add_to_redis=True)
        return Response({"detail": "Mufaqqiyatli chiqildi."})

@extend_schema_view(
    put=extend_schema(
        summary="Change user password",
        request=ChangePasswordSerializer,
        responses={
            200: TokenResponseSerializer,
            401: ValidationErrorSerializer
        }
    )
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=request.user.username,
            password=serializer.validated_data['old_password']
        )

        if user is not None:
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            tokens = UserService.create_tokens(user, is_force_add_to_redis=True)
            return Response(tokens)
        else:
            raise ValidationError("Eski parol xato.")
@extend_schema_view(
    post=extend_schema(
        summary="Forgot Password",
        request=ForgotPasswordRequestSerializer,
        responses={
            200: ForgotPasswordResponseSerializer,
            401: ValidationErrorSerializer
        }
    )
)
class ForgotPasswordView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordRequestSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        users = User.objects.filter(email=email, is_active=True)
        if not users.exists():
            raise exceptions.NotFound(ACTIVE_USER_NOT_FOUND_ERROR_MSG)

        otp_code, otp_secret = OTPService.generate_otp(email=email, expire_in=2 * 60)

        try:
            SendEmailService.send_email(email, otp_code)
            return Response({
                "email": email,
                "otp_secret": otp_secret,
            })
        except Exception:
            redis_conn = OTPService.get_redis_conn()
            redis_conn.delete(f"{email}:otp")
            raise ValidationError("Emailga xabar yuborishda xatolik yuz berdi")

@extend_schema_view(
    post=extend_schema(
        summary="Forgot Password Verify",
        request=ForgotPasswordVerifyRequestSerializer,
        responses={
            200: ForgotPasswordVerifyResponseSerializer,
            401: ValidationErrorSerializer
        }
    )
)
class ForgotPasswordVerifyView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordVerifyRequestSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        redis_conn = OTPService.get_redis_conn()
        otp_secret = kwargs.get('otp_secret')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data['otp_code']
        email = serializer.validated_data['email']
        users = User.objects.filter(email=email, is_active=True)
        if not users.exists():
            raise exceptions.NotFound(ACTIVE_USER_NOT_FOUND_ERROR_MSG)
        OTPService.check_otp(email, otp_code, otp_secret)
        redis_conn.delete(f"{email}:otp")
        token_hash = make_password(token_urlsafe())
        redis_conn.set(token_hash, email, ex=2 * 60 * 60)
        return Response({"token": token_hash})

@extend_schema_view(
    patch=extend_schema(
        summary="Reset Password",
        request=ResetPasswordResponseSerializer,
        responses={
            200: TokenResponseSerializer,
            401: ValidationErrorSerializer
        }
    )
)
class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordResponseSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['patch']
    authentication_classes = []

    def patch(self, request, *args, **kwargs):
        redis_conn = OTPService.get_redis_conn()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_hash = serializer.validated_data['token']
        email = redis_conn.get(token_hash)

        if not email:
            raise ValidationError("Token yaroqsiz")

        users = User.objects.filter(email=email.decode(), is_active=True)
        if not users.exists():
            raise exceptions.NotFound(ACTIVE_USER_NOT_FOUND_ERROR_MSG)

        password = serializer.validated_data['password']
        user = users.first()
        user.set_password(password)
        user.save()

        update_session_auth_hash(request, user)
        tokens = UserService.create_tokens(user, is_force_add_to_redis=True)
        redis_conn.delete(token_hash)
        return Response(tokens)

from .models import Article, Recommendation, ArticleStatus
class RecommendationView(APIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Recommendation.objects.all()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = request.user.id
            data = {
                'message': 'Hello, authenticated user!',
                'user_id': user_id,
                'status': 'success',
            }
        else:
            data = {
                'message': 'Hello, Guest!',
                'status': 'success',
            }
        return Response(data)

    def post(self, request, *args, **kwargs):
        serializer = RecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        more_article_id = serializer.validated_data.get('more_article_id')
        less_article_id = serializer.validated_data.get('less_article_id')

        user_recommendations, created = Recommendation.objects.get_or_create(user=request.user)

        # Handle more recommendations
        if more_article_id is not None:
            article = Article.objects.filter(id=more_article_id).first()
            if article:
                # Remove from less if it exists
                if article in user_recommendations.less_recommend.all():
                    user_recommendations.less_recommend.remove(article)
                # Add to more
                user_recommendations.more_recommend.add(article)

        # Handle less recommendations
        if less_article_id is not None:
            article = Article.objects.filter(id=less_article_id).first()
            if article:
                # Only add to less if it's NOT in more
                if article in user_recommendations.more_recommend.all():
                    user_recommendations.more_recommend.remove(article)
                user_recommendations.less_recommend.add(article)

        return Response(status=status.HTTP_204_NO_CONTENT)

class PopularAuthorsView(LoginRequiredMixin, ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        # Filter active users who have published articles
        active_users_with_articles = CustomUser.objects.filter(
            article_set__is_published=True,
            is_active=True
        ).distinct()

        # Prepare the response data
        results = []
        for user in active_users_with_articles:
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'email': user.email,
                'avatar': user.avatar.url if user.avatar else None  # Adjust according to your model
            }
            results.append(user_data)

        return Response({
            'count': len(results),
            'next': None,
            'previous': None,
            'results': results
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        return (
            User.objects.filter(is_active=True)
            .annotate(total_reads=Sum('article_set__reads_count'))
            .order_by('-total_reads')[:5]  # Get top 5 authors by reads count
        )

class AuthorFollowView(APIView):
    # queryset = Follow.objects.all()
    # serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        return Response({'GetOK!'}, status=status.HTTP_200_OK)

    def post(self, request, id):
        try:
            followed_user = User.objects.get(id=id)
            if Follow.objects.filter(follower=request.user, followee=followed_user).exists():
                return Response({"detail": "Siz allaqachon ushbu foydalanuvchini kuzatyapsiz."}, status=status.HTTP_200_OK)

            Follow.objects.create(
            follower=request.user,
            followee=followed_user,
            username=followed_user.username,
            first_name=followed_user.first_name,
            last_name=followed_user.last_name,
            middle_name=followed_user.first_name,
            email=followed_user.email,
            avatar=followed_user.profile.avatar.url if hasattr(followed_user, 'profile') else None
            )
            return Response({"detail": "Mofaqqiyatli follow qilindi."}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            followed_user = User.objects.get(id=id)
            follow_instance = Follow.objects.get(follower=request.user, followee=followed_user)
            follow_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        except Follow.DoesNotExist:
            return Response({"detail": "Siz ushbu foydalanuvchini kuzatmayapsiz."}, status=status.HTTP_404_NOT_FOUND)

class FollowersListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        followers = Follow.objects.filter(followee=user).select_related('follower')
        return User.objects.filter(id__in=followers.values_list('follower_id', flat=True))

class FollowingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        followings = Follow.objects.filter(follower=user).select_related('followee')

        followings_data = [{'id': follow.followee.id, 'username': follow.followee.username} for follow in followings]

        return Response({'results': followings_data})  # DRF Response obyekti bilan qaytish

class UserNotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user, is_active=True)

class UserNotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user, is_active=True)
        return queryset

    def patch(self, request, *args, **kwargs):
        try:
            notification = self.get_object()

        # Check if the request data contains the 'read' field
            if 'read' in request.data:
                if request.data['read']:
                    notification.read_at = timezone.now()  # Mark as read by setting read_at to current time
                else:
                    notification.read_at = None  # Optionally handle marking as unread

            notification.is_active = False  # Optionally mark as inactive
            notification.save()  # Save changes

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)