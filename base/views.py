from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import User, Car, Info, Reservation, Review, Logs
from datetime import date, datetime, timedelta

def dashboard(request):
    pending = Reservation.objects.filter(confirmed=False, end__gte=date.today()).count()
    cars = Car.objects.all().count()
    available_cars = Car.objects.filter(available=True).count()
    confirmed = Reservation.objects.filter(confirmed=True).count()
    clients = User.objects.filter(is_staff=False, is_superuser=False).count()

    context = {
        'pending': pending,
        'cars': cars,
        'available': available_cars,
        'confirmed': confirmed,
        'clients': clients,
    }
    return render(request, 'base/dashboard.html', context=context)

def cars(request):
    cars = Car.objects.all()
    for car in cars:
        car.save()

    context = {
        'cars': cars,
    }
    return render(request, 'base/dash-cars.html', context)

def add_car(request):
    if request.method == 'POST':
        car = Car.objects.create(
            brand = request.POST.get('brand'),
            model = request.POST.get('model'),
            year = request.POST.get('year'),
            km = request.POST.get('km'),
            color = request.POST.get('color'),
            description = request.POST.get('description'),
            price = request.POST.get('price')
        )
        if request.POST.get('photo'):
            car.photo = request.POST.get('photo')
            car.save()
        
        Logs.objects.create(
            user = request.user,
            action = "Ajouter",
            type = 'V',
            name = car.brand + " " + car.model
        )
        return redirect("cars")

    return render(request, 'base/add-car.html')

def edit_car(request, pk):
    car = Car.objects.get(id=pk)

    if request.method == 'POST':
        car.brand = request.POST.get('brand')
        car.model = request.POST.get('model')
        car.year = request.POST.get('year')
        car.km = request.POST.get('km')
        car.color = request.POST.get('color')
        car.description = request.POST.get('description')
        car.price = request.POST.get('price')
        if request.POST.get('photo'):
            car.photo = request.POST.get('photo')
        car.save()

        Logs.objects.create(
            user = request.user,
            action = "Modifier",
            type = 'V',
            name = car.brand + " " + car.model
        )

        return redirect("cars")

    context = {
        'car': car,
    }
    return render(request, 'base/edit-car.html', context=context)

def delete_car(request, pk):
    car = Car.objects.get(id=pk)
    object = "la voiture"
    name = car.brand + " " + car.model

    if request.method == 'POST':
        car.delete()

        Logs.objects.create(
            user = request.user,
            action = "Supprimer",
            type = 'V',
            name = car.brand + " " + car.model
        )
        return redirect('cars')

    context = {
        'object': object,
        'name': name,
    }
    return render(request, 'base/delete.html', context)


def reservation(request):
    non = Reservation.objects.filter(confirmed=False, end__gte=date.today())
    confirmed = Reservation.objects.filter(confirmed=True, end__gte=date.today())

    if request.method == 'POST':
        res = Reservation.objects.get(id=request.POST.get('id'))
        if request.POST.get('button') == 'confirmer':
            res.confirmed = True
            Logs.objects.create(
                user = request.user,
                action = "Confirmer",
                type = 'R',
                name = "Reservation " + str(res.id)
            )
            res.save()
            res.car.save()
        else:
            Logs.objects.create(
                user = request.user,
                action = "Annuler",
                type = 'R',
                name = "Reservation " + str(res.id)
            )
            res.delete()
            
        

        return redirect('reservation')

    context = {
        'non': non,
        'confirmed': confirmed,
    }
    return render(request, 'base/reservation.html', context)

def users(request):
    staff = User.objects.filter(is_staff=True)
    clients = User.objects.filter(is_staff=False)

    context = {
        'staff': staff,
        'clients': clients,
    }
    return render(request, 'base/users.html', context)

def edit_user(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.info.phone = request.POST.get('phone')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        user.info.save()
        
        Logs.objects.create(
            user = request.user,
            action = "Modifier",
            type = 'C',
            name = user.username
        )

        return redirect('users')

    context = {
        'user': user,
    }
    return render(request, 'base/edit-user.html', context)

def delete_user(request, pk):
    user = User.objects.get(id=pk)
    object = "l'utilisateur"
    name = user.username

    if request.method == 'POST':
        user.delete()
        return redirect('users')

    context = {
        'object': object,
        'name': name,
    }
    return render(request, 'base/delete.html', context)


def reviews(request):
    shown = Review.objects.filter(show=True)
    not_shown = Review.objects.filter(show=False)

    if request.method == 'POST':
        review = Review.objects.get(id=request.POST.get('id'))
        if request.POST.get('action') == 'show':
            review.show = True
        else:
            review.show = False
        review.save()
        return redirect('reviews')

    context = {
        'shown': shown,
        'not_shown': not_shown
    }
    return render(request, 'base/reviews.html', context)


def logs(request):
    logs = Logs.objects.all().order_by('-created')

    context = {
        'logs': logs
    }
    return render(request, 'base/logs.html', context)


@login_required()
def logout_user(request):
    logout(request)
    return redirect('landing')


def login_user(request):
    if request.user.is_authenticated:  
        if request.user.is_staff:
            return redirect("dashboard")
        else: 
            return redirect("landing")

    if request.method == 'POST':
        user = None
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('dashboard')
                return redirect('landing')
            else:
                messages.error(request, "Mot de passe incorrecte")
        except:
            messages.error(request, 'Adresse email invalide')

    return render(request, 'base/login.html')


def landing(request):
    cars = Car.objects.filter(available=True)[0:3]
    reviews = Review.objects.filter(show=True)[0:3]

    context = {
        'cars': cars,
        'reviews': reviews,
    }
    return render(request, 'base/landing.html', context)


def register_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        Info.objects.create(
            user=user,
            phone=request.POST.get('phone'),
        )

        login(request, user)
        return redirect('login')

    context = {}
    return render(request, 'base/sign-up.html', context)


def car_page(request):
    cars = Car.objects.filter(available=True)

    context = {
        'cars': cars,
    }
    return render(request, 'base/carsPage.html', context)


start=None
end=None
def reserver(request, pk):
    global start, end
    car = Car.objects.get(id=pk)

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')

        return redirect('confirmer', car.id)

    context = {
        'car': car
    }
    
    if request.user.is_authenticated: 
        return render(request, 'base/reserver1.html', context)
    else:
        return redirect('res-login', pk)


def confirmer(request, pk):
    global start, end
    start = datetime.strptime(str(start), '%Y-%m-%d').date()
    end = datetime.strptime(str(end), '%Y-%m-%d').date()
    car = Car.objects.get(id=pk)
    total = (end - start).days * car.price

    if request.method == 'POST':
        Reservation.objects.create(
            car=car,
            client=request.user,
            start=start,
            end=end,
        )
        return redirect('landing')

    context = {
        'car': car,
        'total': total,
        'start': start,
        'end': end,
    }
    return render(request, 'base/reservation2.html', context)


def res_register(request, pk):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        Info.objects.create(
            user=user,
            phone=request.POST.get('phone'),
        )

        login(request, user)
        return redirect('reserver', pk)

    context = {
        'pk': pk
    }
    return render(request, 'base/sign-up2.html', context)


def res_login(request, pk):
    if request.method == 'POST':
        user = None
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('reserver', pk)
            else:
                messages.error(request, "Mot de passe incorrecte")
        except:
            messages.error(request, 'Adresse email invalide')
    
    context = {
        'pk': pk,
    }
    return render(request, 'base/login2.html', context)


def car_info(request, pk):
    car = Car.objects.get(id=pk)
    cars = Car.objects.filter(available=True)[0:3]
    
    context = {
        'car': car,
        'cars': cars,
    }
    return render(request, 'base/carInfo.html', context)


def profil(request):
    res = Reservation.objects.filter(client=request.user)
    user = request.user

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.info.phone = request.POST.get('phone')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        user.info.save()
        return redirect('profil')

    context = {
        'reservations': res
    }
    return render(request, 'base/profil.html', context)


def add_review(request):
    if request.method == 'POST':
        Review.objects.create(
            client=request.user,
            message=request.POST.get('message')
        )
        return redirect('landing')

    if request.user.is_authenticated: 
        return render(request, 'base/avisPage.html')
    else:
        return redirect('rev-login')


def rev_register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        Info.objects.create(
            user=user,
            phone=request.POST.get('phone'),
        )

        login(request, user)
        return redirect('avis')

    return render(request, 'base/sign-up3.html')


def rev_login(request):
    if request.method == 'POST':
        user = None
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('avis')
            else:
                messages.error(request, "Mot de passe incorrecte")
        except:
            messages.error(request, 'Adresse email invalide')
    
    return render(request, 'base/login3.html')