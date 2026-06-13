from django.core.management.base import BaseCommand
from api.models import KBEntry


class Command(BaseCommand):
    help = 'Seed the knowledge base with sample KBEntry records.'

    def handle(self, *args, **options):
        entries = [
            {
                'question': 'What is select_related in Django ORM?',
                'answer': 'select_related performs a SQL JOIN and fetches related objects in one query.',
                'category': 'database',
            },
            {
                'question': 'How does transaction.atomic() work?',
                'answer': 'transaction.atomic creates a database transaction block that can be rolled back on error.',
                'category': 'database',
            },
            {
                'question': 'What is JWT authentication?',
                'answer': 'JWT is a JSON Web Token used for secure, stateless authentication between client and server.',
                'category': 'api',
            },
            {
                'question': 'When should I use Q objects in Django?',
                'answer': 'Use Q objects to build complex OR queries and conditional logic in Django ORM filters.',
                'category': 'framework',
            },
            {
                'question': 'What is the difference between API and SDK?',
                'answer': 'An API defines a contract for interaction while an SDK provides tools and libraries to consume that API.',
                'category': 'api',
            },
            {
                'question': 'How do I scale PostgreSQL for a growing application?',
                'answer': 'Scale PostgreSQL using read replicas, connection pooling, and schema optimization.',
                'category': 'cloud',
            },
            {
                'question': 'What is the best way to secure an API key?',
                'answer': 'Store API keys securely on the server and never expose them to client-side code.',
                'category': 'general',
            },
            {
                'question': 'How can I monitor database performance?',
                'answer': 'Use query analysis, indexes, and monitoring tools like pg_stat_statements or managed service dashboards.',
                'category': 'database',
            },
            {
                'question': 'What is the purpose of a request logger?',
                'answer': 'A request logger records incoming API requests for auditing, debugging, and usage tracking.',
                'category': 'general',
            },
            {
                'question': 'How do I add JWT support to Django REST Framework?',
                'answer': 'Install djangorestframework-simplejwt and configure JWTAuthentication in REST_FRAMEWORK settings.',
                'category': 'framework',
            },
        ]

        created = 0
        for entry_data in entries:
            obj, created_flag = KBEntry.objects.get_or_create(
                question=entry_data['question'],
                defaults={
                    'answer': entry_data['answer'],
                    'category': entry_data['category'],
                },
            )
            if created_flag:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created} KBEntry records.'))
