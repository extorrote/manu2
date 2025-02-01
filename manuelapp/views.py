from django.shortcuts import render,redirect


from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages

# Create your views here.

def index(request):
     condos = Condo.objects.all()
     return render(request, 'index.html', {'condos': condos})



def property_management(request):
    return render(request,'property_management.html')


def private_chef(request):
    return render(request,'private_chef.html')





def contact(request):
    return render(request,'contact.html')




############################# DESDE AQUI TODO LO QUE TIENE QUE VER CON LAS RESERVACIONES ###########################
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from .models import Condo, Reservation
from .forms import ReservationForm, CondoForm, ContactForm
from datetime import datetime, timedelta
import json
from pydantic import ValidationError




   


def condo_detail(request, condo_id):
    condo = get_object_or_404(Condo, id=condo_id)
    image_urls = [getattr(condo, f'imagen{i}').url for i in range(1, 9) if getattr(condo, f'imagen{i}')]
    return render(request, 'condo_detail.html', {'condo': condo, 'image_urls': image_urls})


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def post_condo(request):
    if request.method == 'POST':
        form = CondoForm(request.POST, request.FILES)
        if form.is_valid():
            condo = form.save(commit=False)  # Save the form data without committing to the database yet

            # Handle image uploads
            for i in range(1, 9):
                image = request.FILES.get(f'imagen{i}')
                if image:
                    # Set the image file to the condo instance
                    setattr(condo, f'imagen{i}', image)

            # Handle video upload
            video = request.FILES.get('video')
            if video:
                condo.video = video

            # Save the condo instance
            condo.save()

            return redirect('index')
    else:
        form = CondoForm()

    return render(request, 'post_condo.html', {'form': form})


def get_reserved_dates(condo):
    reservations = Reservation.objects.filter(condo=condo)
    reserved_dates = []
    for reservation in reservations:
        date = reservation.start_date
        while date <= reservation.end_date:
            reserved_dates.append(date.strftime('%Y-%m-%d'))
            date += timedelta(days=1)
    return reserved_dates


def get_available_dates(condo):
    today = datetime.now().date()
    end_date = today + timedelta(days=180)
    available_dates = [today + timedelta(days=i) for i in range((end_date - today).days + 1)]
    reserved_dates = set(get_reserved_dates(condo))
    return [date.strftime('%Y-%m-%d') for date in available_dates if date.strftime('%Y-%m-%d') not in reserved_dates]


from django.templatetags.static import static
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
import os

from datetime import timedelta# ESTE SE IMPORTA PARA PODER CONTAR LOS DIAS





def condo_calendar_and_reserve(request, condo_id):
    condo = get_object_or_404(Condo, id=condo_id)

    # Determine the image path (dynamic or static fallback)
    if hasattr(condo, 'image') and condo.image:
        image_path = condo.image.path  # Path to the image on the server
    else:
        image_path = os.path.join(settings.BASE_DIR, 'manuelapp', 'static', 'images', 'logo_property_management.png')

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data['accept_terms']:
                form.add_error('accept_terms', 'You must accept the terms and conditions to proceed.')
                return render(request, 'condo_calendar_and_reserve.html', {
                    'form': form,
                    'condo': condo,
                    'unavailable_dates': json.dumps(get_reserved_dates(condo)),
                    'available_dates': json.dumps(get_available_dates(condo))
                })

            reservation = form.save(commit=False)
            reservation.condo = condo

            overlapping_reservations = Reservation.objects.filter(
                condo=condo,
                start_date__lte=reservation.end_date,
                end_date__gte=reservation.start_date
            )

            if overlapping_reservations.exists():
                form.add_error(None, 'The selected dates are not available.')
                return render(request, 'condo_calendar_and_reserve.html', {
                    'form': form,
                    'condo': condo,
                    'unavailable_dates': json.dumps(get_reserved_dates(condo)),
                    'available_dates': json.dumps(get_available_dates(condo))
                })

            # Calculate total to pay
            holiday_season_price = float(condo.holiday_season)
            total_days = (reservation.end_date - reservation.start_date).days +1
            total_to_pay = total_days * holiday_season_price 

            reservation.save()

            subject = 'Reservation Confirmation'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = reservation.email
            recipient_list = [to_email, 'proyectodigitalmexico@gmail.com']

            # Updated HTML email to include total to pay
            html_message = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            color: #ffffff;
            background-color: #1f1f1f;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            background-color: #262626;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }}
        h2 {{
            color: #bf8d30;
            font-size: 24px;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #bf8d30;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #bf8d30;
            margin-top: 30px;
            text-transform: uppercase;
            font-size: 18px;
            border-bottom: 1px solid #bf8d30;
            padding-bottom: 5px;
        }}
        strong{{
        text-transform:capitalize;
        }}

        h4{{
        color:#1f1f1f;
        }}

        p {{
            margin: 10px 0;
            font-size: 14px;
            color: #d1d1d1;
        }}
        a {{
            color: #bf8d30;
            text-decoration: none;
            font-weight: bold;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .highlight {{
            color: #bf8d30;
            font-weight: bold;
        }}
        .highlight-red {{
            color: #ff4c4c;
            font-weight: bold;
        }}
        .condo-info {{
            background-color: #333333;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }}
        .condo-info img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-top: 15px;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #999999;
        }}
        .button {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #bf8d30;
            color: #1f1f1f;
            font-weight: bold;
            text-transform: uppercase;
            border-radius: 5px;
            text-decoration: none;
        }}
        .button:hover {{
            background-color: #d1a45a;
        }}
        @media only screen and (max-width: 600px) {{
            .container {{
                padding: 15px;
            }}
            h2 {{
                font-size: 20px;
            }}
            h3 {{
                font-size: 16px;
            }}
            p {{
                font-size: 13px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Reservation Confirmation</h2>
        <p>Dear {reservation.name},</p>
        <p>Your reservation for <strong class="highlight">{condo.development_name}</strong> from <strong class="highlight">{reservation.start_date}</strong> to <strong class="highlight">{reservation.end_date}</strong> has been confirmed.</p>
        <div class="condo-info">
            <p class="highlight-red">Payment in full is due within 7 days of reservation or the reservation will be cancelled.</p>
            <h3>Guest Details</h3>
            <p>Name: <strong>{reservation.name}</strong></p>
            <p>Start Date: <strong>{reservation.start_date}</strong></p>
            <p>End Date: <strong>{reservation.end_date}</strong></p>
            <p>Email: <strong>{reservation.email}</strong></p>
            <p>Num Guests: <strong>{reservation.num_guests}</strong></p>
            <p>Phone Number: <strong>{reservation.phone_number}</strong></p>
            <p>Special Requests: <strong>{reservation.special_requests}</strong></p>

            <h3>Condo Details</h3>
            <p>Neighborhood: <strong>{condo.neighborhood}</strong></p>
            <p>Bedrooms: <strong>{condo.bedrooms}</strong></p>
            <p>Bathrooms: <strong>{condo.bathrooms}</strong></p>
            <p>Checking Time: <strong>{condo.horario_checking}</strong></p>
             <p>Checkout Time: <strong>{condo.horario_checkout}</strong></p>
            <p>Price Per Night: <strong>${holiday_season_price:.2f} USD</strong></p>
            <p>Total Nights: <strong>{total_days} night(s)</strong></p>
            <h3>Total to Pay</h3>
            <p><strong class="highlight">${total_to_pay:.2f} USD</strong></p>
            <p>Refundable Damage Deposit: $<strong>{condo.refundable_damage_deposit}</strong></p>
            <img src="cid:condo_image" alt="Condo Image" />
        </div>
        <div class="footer">
            <p style="text-trasform:capitalize"> Thank You for Choosing Us! </p>
            <p> If You Have Any Question Feel Free to Contact Us:</p>
            <p> <a href="mailto:{from_email}">{from_email}</a></p>

            <a href="{request.build_absolute_uri('/terms_and_conditions/')}" class="button" target="_blank">View Terms and Conditions</a>
        </div>
    </div>
</body>
</html>
"""

            # Create email message
            email = EmailMessage(subject, html_message, from_email, recipient_list)
            email.content_subtype = 'html'

            # Attach the image
            with open(image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<condo_image>')
                email.attach(img)

            email.send()
            messages.success(request, 'Thank You! Please Check Your Email.')
            return redirect('index')
    else:
        form = ReservationForm(initial={'condo': condo})

    return render(request, 'condo_calendar_and_reserve.html', {
        'form': form,
        'condo': condo,
        'unavailable_dates': json.dumps(get_reserved_dates(condo)),
        'available_dates': json.dumps(get_available_dates(condo)),
    })





def check_date_availability(request):
    date_str = request.GET.get('date')
    condo_id = request.GET.get('condo_id')

    if not date_str or not condo_id:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    condo = get_object_or_404(Condo, id=condo_id)
    reservations = Reservation.objects.filter(
        condo=condo,
        start_date__lte=date,
        end_date__gte=date
    )

    available = not reservations.exists()
    return JsonResponse({'available': available})




from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            # Process the form data, e.g., send an email
            send_mail(
                f'Contact Form Submission from {name}',
                f'Message: {message}\nPhone: {phone}\nEmail: {email}',
                'proyectodigitalmexico@gmail.com',  # From email
                ['proyectodigitalmexico@gmail.com'],  # To email
                fail_silently=False,
            )


            messages.success(request, 'Email Sent!  we will Get Back to You Soon')
            return redirect('index')
    else:
        form = ContactForm()

    return render(request, 'send_email_form.html', {'form': form})




def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')



from django.contrib.auth import authenticate,login,logout
def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')#ESTO ES LO QUE LE HE PUESTO EN EL NAME EN EL CAMPO DEL FORMULARIO
        user=authenticate(request,username=username,password=password)#KEYBOL ARGUMENT ES CUANDO VA UN LA PRIMERA ES LA KEIBOLNAME  NOMBRE=NOMBRE LA SEGUNDA ES LA VARIABLE QUE ESTA RECIBIENDO
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.warning (request,'Wrong Psername or Password')


    return render (request,'login.html',{'title':'identificate'})


def logout_user(request):
    logout(request)
    return redirect ('index')



def about_us(request):
    return render(request,'about_us.html')

def terms_and_conditions(request):
    return render (request,'terms_and_conditions.html')


def privacy_policy(request):
    return render (request,'privacy_policy.html')