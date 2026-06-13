import secrets
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import Company, KBEntry, QueryLog
from .permissions import IsAdminUser
from .serializers import LoginSerializer, QuerySerializer, RegisterSerializer


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if User.objects.filter(username=data['username']).exists():
            return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
        )

        company, _ = Company.objects.get_or_create(
            user=user,
            defaults={
                'company_name': data['company_name'],
                'api_key': secrets.token_urlsafe(32),
            },
        )
        company.company_name = data['company_name']
        company.save()

        access_token = str(AccessToken.for_user(user))

        return Response(
            {
                'username': user.username,
                'company_name': company.company_name,
                'api_key': company.api_key,
                'access': access_token,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = str(AccessToken.for_user(user))

        try:
            company = user.company
        except Exception:
            company = Company.objects.create(
                user=user,
                company_name=user.email or user.username,
                api_key=secrets.token_urlsafe(32),
            )

        return Response(
            {
                'access': access_token,
                'company_name': company.company_name,
                'api_key': company.api_key,
            }
        )


class KBQueryView(APIView):
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        search_term = serializer.validated_data['search'].strip()

        if not search_term:
            return Response({'detail': 'Search term may not be blank.'}, status=status.HTTP_400_BAD_REQUEST)

        company = request.user.company

        with transaction.atomic():
            queryset = KBEntry.objects.filter(
                Q(question__icontains=search_term) | Q(answer__icontains=search_term)
            )
            count = queryset.count()
            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=count,
            )

        results = [
            {
                'id': str(entry.id),
                'question': entry.question,
                'answer': entry.answer,
                'category': entry.category,
            }
            for entry in queryset
        ]

        return Response({
            'search': search_term,
            'count': count,
            'results': results,
        })


class UsageSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_queries = QueryLog.objects.aggregate(total=Count('id'))['total'] or 0
        active_companies = QueryLog.objects.values('company').distinct().count()
        top_search_terms_qs = (
            QueryLog.objects
            .values('search_term')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )

        top_search_terms = [
            {'search_term': item['search_term'], 'count': item['count']}
            for item in top_search_terms_qs
        ]

        return Response({
            'total_queries': total_queries,
            'active_companies': active_companies,
            'top_search_terms': top_search_terms,
        })
