from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from leads.models import UserProfile, Lead, Agent, Category, FollowUp
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Adds sample data to the database'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        FollowUp.objects.all().delete()
        Lead.objects.all().delete()
        Agent.objects.all().delete()
        Category.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()

        # Create Users
        self.stdout.write('Creating users...')
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True,
            is_organisor=True
        )

        agent_user = User.objects.create_user(
            username='agent1',
            email='agent1@example.com',
            password='agent123',
            is_agent=True
        )

        # Create User Profiles
        self.stdout.write('Creating user profiles...')
        admin_profile = UserProfile.objects.create(user=admin_user)
        agent_profile = UserProfile.objects.create(user=agent_user)

        # Create Categories
        self.stdout.write('Creating categories...')
        categories = [
            Category.objects.create(name='New', organisation=admin_profile),
            Category.objects.create(name='Contacted', organisation=admin_profile),
            Category.objects.create(name='Converted', organisation=admin_profile),
            Category.objects.create(name='Unconverted', organisation=admin_profile),
        ]

        # Create Agent
        self.stdout.write('Creating agent...')
        agent = Agent.objects.create(
            user=agent_user,
            organisation=admin_profile
        )

        # Create Leads
        self.stdout.write('Creating leads...')
        leads = [
            Lead.objects.create(
                first_name='John',
                last_name='Doe',
                age=30,
                organisation=admin_profile,
                agent=agent,
                category=categories[0],
                description='Interested in our premium package',
                phone_number='1234567890',
                email='john@example.com'
            ),
            Lead.objects.create(
                first_name='Jane',
                last_name='Smith',
                age=25,
                organisation=admin_profile,
                agent=agent,
                category=categories[1],
                description='Looking for basic services',
                phone_number='0987654321',
                email='jane@example.com'
            ),
            Lead.objects.create(
                first_name='Bob',
                last_name='Johnson',
                age=40,
                organisation=admin_profile,
                agent=agent,
                category=categories[2],
                description='Converted customer',
                phone_number='5555555555',
                email='bob@example.com',
                converted_date=timezone.now()
            ),
        ]

        # Create Follow-ups
        self.stdout.write('Creating follow-ups...')
        for lead in leads:
            FollowUp.objects.create(
                lead=lead,
                notes=f'Initial contact made with {lead.first_name}',
                date_added=timezone.now()
            )
            FollowUp.objects.create(
                lead=lead,
                notes=f'Follow-up call scheduled with {lead.first_name}',
                date_added=timezone.now()
            )

        self.stdout.write(self.style.SUCCESS('Successfully added sample data')) 