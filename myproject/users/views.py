from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User, UploadedFile
from .forms import SignupForm, LoginForm, FileUploadForm
import random
import string
from django.db import connection
import csv

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.generate_otp()
            user.save()
            return render(request, 'users/success.html', {'message': 'Signup successful! Please login.'})
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            otp = form.cleaned_data.get('otp')
            try:
                user = User.objects.get(mobile=mobile, otp=otp)
                return render(request, 'users/success.html', {'message': 'Login successful!'})
            except User.DoesNotExist:
                return render(request, 'users/error.html', {'message': 'Invalid OTP or mobile number.'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# File Upload View
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            table_name = uploaded_file.table_name

            # Parse the uploaded CSV file
            file_path = uploaded_file.file.path
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Get the header row
                rows = list(reader)  # Get the data rows

            # Dynamically create the table with headers as columns
            with connection.cursor() as cursor:
                # Construct the SQL for table creation
                create_table_query = f"""
                    CREATE TABLE `{table_name}` (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        {", ".join([f"`{col}` TEXT" for col in headers])}
                    )
                """
                cursor.execute(create_table_query)

                # Insert the rows into the table
                for row in rows:
                    placeholders = ", ".join(["%s"] * len(headers))
                    insert_query = f"""
                        INSERT INTO `{table_name}` ({", ".join([f"`{col}`" for col in headers])})
                        VALUES ({placeholders})
                    """
                    cursor.execute(insert_query, row)

            return render(request, 'users/success.html', {
                'message': f'File uploaded successfully. Data stored in table: {table_name}'
            })
    else:
        form = FileUploadForm()
    return render(request, 'users/file_upload.html', {'form': form})
