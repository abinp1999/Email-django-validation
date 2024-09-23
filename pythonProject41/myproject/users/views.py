from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .forms import UserRegistrationForm
from .utils import generate_password
from django.conf import settings

def register(request):
    # Check if user is already logged in
    if request.user.is_authenticated:
        return redirect('Register')  # Redirect to home page if logged in

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Check if the email is already registered
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('register')

            # Generate a password and save the user
            password = generate_password()
            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            # Send email with the password
            try:
                send_mail(
                    'Your New Account',
                    f'Welcome! Your password is: {password}',
                    settings.EMAIL_HOST_USER,  # Your email from settings.py
                    [user.email],  # Send email to the newly registered user
                    fail_silently=False,
                )
            except BadHeaderError:
                messages.error(request, 'Invalid header found in the email.')
            except Exception as e:
                messages.error(request, f'An error occurred while sending the email: {e}')

            messages.success(request, 'Registration successful! Check your email for your password.')
            return redirect('Register')  # Redirect to Register page
    else:
        form = UserRegistrationForm()

    return render(request, 'Register.html', {'form': form})
