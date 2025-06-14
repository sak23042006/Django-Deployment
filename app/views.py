import os
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from . models import *
# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, GroundsSerializer
from datetime import datetime, timedelta

ADMIN_CONFIRMATION_CODE = os.getenv('ADMIN_CONFIRMATION_CODE', 'rcVwwENOS7hEvtj')
class UserDetailView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()  # You can filter or get a specific user if needed
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ParticularUserView(APIView):
    def get(self, request, user_id, format=None):
        # Retrieve the user by ID (or email if needed)
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserDeleteView(APIView):
    
    def delete(self, request, user_id, format=None):
        # Retrieve the user by ID
        user = get_object_or_404(User, id=user_id)
        
        # Serialize the user data before deletion to show it in the response
        serializer = UserSerializer(user)
        
        # Return the serialized user data with a message indicating the deletion is about to occur
        return Response({
            "message": "Are you sure you want to delete this user?",
            "user_to_be_deleted": serializer.data
        }, status=status.HTTP_200_OK)


class UpdateUserDetailView(APIView):
    
    def get(self, request, user_id, format=None):
        # Retrieve a user by ID
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, user_id, format=None):
        # Retrieve a user by ID
        user = get_object_or_404(User, id=user_id)
        
        # Serialize the incoming data and validate it
        serializer = UserSerializer(user, data=request.data, partial=False)
        
        if serializer.is_valid():
            # Update the user instance with the validated data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')

def register(request):
  
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
     
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['email']=email
            request.session['login']='admin'
            return redirect('home') 

        elif User.objects.filter(email=email,password=password).exists():

            request.session['email']=email
            request.session['login']='user'
            return redirect('home')  
        else:

            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

def admin_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        confirmation_code = request.POST.get('confirmation_code')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_register')

        if confirmation_code != ADMIN_CONFIRMATION_CODE:
            messages.error(request, 'Invalid confirmation code.')
            return redirect('admin_register')

        # ✅ Save the admin credentials temporarily in session (local testing only)
        request.session['admin_email'] = email
        request.session['admin_password'] = password

        messages.success(request, 'Admin registered successfully. You can now log in.')
        return redirect('admin_login')

    return render(request, 'admin_register.html')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Retrieve stored admin email and password (from session)
        stored_email = request.session.get('admin_email')
        stored_password = request.session.get('admin_password')

        if stored_email is None or stored_password is None:
            messages.error(request, 'No admin registered yet.')
            return redirect('admin_login')

        if email == stored_email and password == stored_password:
            request.session['email'] = email
            request.session['login'] = 'admin'
            return redirect('home')
        else:
            messages.error(request, 'Invalid admin credentials.')
            return redirect('admin_login')

    return render(request, 'admin_login.html')

def about(request):
    # User.objects.all().delete()
    # UserProfile.objects.all().delete()
    # Grounds.objects.all().delete()
    # groundSlotsModel.objects.all().delete()
    # slotPaymentModel.objects.all().delete()
    # teamModel.objects.all().delete()
    # userRequestModel.objects.all().delete()
    return render(request, 'about.html')



def home(request):
    login = request.session['login']
    return render(request, 'home.html',{'login':login})

def profile(request):
    login =  request.session['login']
    email = request.session['email']
    
    data=UserProfile.objects.filter(user__email=email).exists()
    if data:
        data=UserProfile.objects.filter(user__email=email)
    else:
        return redirect('updateprofile')

    return render(request, 'profile.html',{'login':login, 'data':data})
    

def updateprofile(request):
   
    login = request.session.get('login', None)
    email = request.session.get('email', None)
    
   
    user = User.objects.get(email=email)
    
   
    data = UserProfile.objects.filter(user=user.id)
    
    if request.method == 'POST':
       
        profile_image = request.FILES.get('profileImage') 
        
       
        game_type = request.POST.get('game_type')
        indoor_game = request.POST.get('indoor_game')
        outdoor_game = request.POST.get('outdoor_game')
        
       
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        if game_type == 'indoor':
            game = indoor_game 
        elif game_type == 'outdoor':
            game = outdoor_game 
        else:
            game = None 
       
        if data:
            profile = data[0]
           
            profile.address = address
            profile.bio = bio
            profile.game_type = game_type
            if game_type == 'indoor':
                profile.game = indoor_game
               
            elif game_type == 'outdoor':
                profile.game = outdoor_game
               
            if profile_image:
                profile.profile = profile_image 
            profile.save()
        else:
            profile = UserProfile.objects.create(
                user=user,
               
                address=address,
                bio=bio,
                game_type=game_type,
                game=game,
                profile_image=profile_image
            )
        
       
        return render(request, 'updateprofile.html', {'data': [profile], 'login': login})
    
    else:
       
        if data:
            userdata = data
        else:
           
            UserProfile.objects.create(user=user)
            userdata = UserProfile.objects.filter(user=user.id)

        return render(request, 'updateprofile.html', {'data': userdata, 'login': login})


def logout(request):
    del request.session['email']
    del request.session['login']
    return redirect('index')



class AddGroundAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Create a serializer instance with the incoming data
        serializer = GroundsSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new Ground to the database
            serializer.save()
            return Response({"message": "Ground added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def addground(request):
    login =  request.session['login']
   

    return render(request, 'addgrounds.html',{'login':login})


class ViewGroundsAPIView(APIView):
    """
    API View to get all grounds or a specific ground by ground name or ID.
    """
    
    def get(self, request, *args, **kwargs):
        ground_name = request.query_params.get('groundname', None)  # optional query param for filtering by name
        ground_id = request.query_params.get('id', None)  # optional query param for filtering by ID
        
        # Fetching a specific ground by groundname or ID if provided
        if ground_name:
            try:
                ground = Grounds.objects.get(groundname=ground_name)
                serializer = GroundsSerializer(ground)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Grounds.DoesNotExist:
                return Response({"detail": "Ground not found"}, status=status.HTTP_404_NOT_FOUND)
        
        elif ground_id:
            try:
                ground = Grounds.objects.get(id=ground_id)
                serializer = GroundsSerializer(ground)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Grounds.DoesNotExist:
                return Response({"detail": "Ground not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # If no query parameter is provided, return all grounds
        grounds = Grounds.objects.all()
        serializer = GroundsSerializer(grounds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def viewgrounds(request):
    login = request.session.get('login', 'user')
    data = Grounds.objects.all()

    # Fetch weather forecast ONCE for the city you're displaying (Vijayawada)
    weather_data = run_weather_forecast_pipeline(city="Vijayawada")

    # Prepare grounds data with weather for display
    grounds_with_weather = []
    for ground in data:
        if 'error' not in weather_data:
            ground.weather = weather_data.get('forecasted_weather')
            ground.temp_min = weather_data.get('approx_temp_min')
            ground.temp_max = weather_data.get('approx_temp_max')
        else:
            ground.weather = "Unavailable"
            ground.temp_min = "0"
            ground.temp_max = "0"

        grounds_with_weather.append(ground)

    return render(request, 'viewgrounds.html', {
        'login': login,
        'data': grounds_with_weather,
        'weather_datetime': weather_data.get('datetime') if 'error' not in weather_data else "Unavailable",
        'weather_city': weather_data.get('city') if 'error' not in weather_data else "Unavailable"
    })

def updategrounds(request, id):
    login = request.session['login']
    data = Grounds.objects.filter(id=id)
    if request.method == 'POST':
        groudname = request.POST['groundname']
        gamename = request.POST['gamename']
        price = request.POST['price']
        location = request.POST['location']
        slots = request.POST['slots']
        image = request.FILES.get('image')  # Using .get() to avoid KeyError
        up = Grounds.objects.get(id=id)
        up.groundname = groudname
        up.gamename =gamename
        up.price = price
        up.location = location
        up.slots = slots
        if image:
            up.image = image
        up.save()
        messages.success(request, 'Updated Successfully!')
        return redirect('updategrounds', id)


    return render(request, 'updateground.html',{'login':login,'id':id, 'data':data})


def deleteground(request, id):
    data = Grounds.objects.filter(id=id)
    data.delete()

    return redirect('viewgrounds')

def viewSlots(request):
    login = request.session.get('login', 'user')
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    # Get slots for today and tomorrow
    allSlots = groundSlotsModel.objects.filter(date__in=[today, tomorrow]).order_by('date', 'start_time')

    if not allSlots.exists():
        messages.info(request, "No slots available for today or tomorrow. Please add slots first.")
        return redirect('addSlots')  # Ensure 'addSlots' is the name used in your urls.py

    return render(request, 'viewSlots.html', {
        'login': login,
        'allSlots': allSlots
    })

def addSlots(request):
    login = request.session.get('login')

    if request.method == 'POST':
        groundName = request.POST.get('groundName')
        date_str = request.POST.get('date')
        is_available = request.POST.get('is_available_value') == '1'
        time_range = request.POST.get('end_time')

        if not groundName or not date_str:
            messages.error(request, 'Ground name and date are required.')
            return redirect('addSlots')

        try:
            formatted_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('addSlots')

        try:
            ground = Grounds.objects.get(groundname__iexact=groundName)
        except Grounds.DoesNotExist:
            messages.error(request, 'Ground not found.')
            return redirect('addSlots')

        # Weather API call
        result = run_weather_forecast_pipeline(date_str)
        print('Weather Result:', result)

        if 'forecasted_weather' in result:
            weather_report = result['forecasted_weather']
            slot_price = ground.price * 0.5 if weather_report.lower() == 'rain' else ground.price
        else:
            weather_report = "Unavailable"
            slot_price = ground.price

        # Parse start and end time
        start_time_str, end_time_str = None, None
        if time_range:
            try:
                start_time_str, end_time_str = [t.strip() for t in time_range.split('-')]
            except ValueError:
                messages.warning(request, 'Invalid time range format. Expected: "HH:MM - HH:MM".')

        # Create slot
        groundSlotsModel.objects.create(
            groundName=groundName,
            start_time=start_time_str,
            end_time=end_time_str,
            is_available=is_available,
            location=ground.location,
            gameName=ground.gamename,
            slotPrice=slot_price,
            date=formatted_date,
            weatherReport=weather_report,
        )

        messages.success(request, 'Slot added successfully.')
        return redirect('addSlots')

    return render(request, 'addSlots.html', {'login': login})



def getBookedSlots(request, groundname):
    login = request.session.get('login')
    getSlots = groundSlotsModel.objects.filter(groundName=groundname)
    return render(request, 'viewSlots.html', {'login': login, 'allSlots':getSlots})

def slotPayment(request, slotId):
    print('3333333333333', slotId)
    userEmail = request.session['email']
    print('mmmmmmmmmmm', userEmail)
    getSlotDetails = groundSlotsModel.objects.get(slotId=slotId)
    amount = getSlotDetails.slotPrice
    if request.method == 'POST':
        getCardNumber = request.POST.get('cardNumber')
        getHolderName = request.POST.get('cardHolder')

        payment = slotPaymentModel(
            cardNumber=getCardNumber,
            cardHolderName=getHolderName,
            groundName=getSlotDetails.groundName,
            gameName=getSlotDetails.gameName,
            userEmail=userEmail,
            paid=amount,
            location=getSlotDetails.location,
            start_time=getSlotDetails.start_time,
            end_time=getSlotDetails.end_time
        )
        payment.save()
        getSlotDetails.is_available = False
        getSlotDetails.save()

        messages.success(request, 'payment successfull')
        return redirect('slotPayment', slotId=slotId) 
    return render(request, 'slotPayment.html', {'slotId':slotId, 'amount':amount})

### Weather Prediction Function
import requests
from decouple import config
from datetime import datetime

def run_weather_forecast_pipeline(city="Vijayawada"):
    try:
        API_KEY = config('OPENWEATHER_API_KEY')  # Your API key in .env
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return {"error": data.get("message", "Failed to fetch weather data")}

        # Extract forecast for the *next available day (first item)*
        first_forecast = data['list'][0]

        forecasted_weather = first_forecast['weather'][0]['main']
        temp_min = first_forecast['main']['temp_min']
        temp_max = first_forecast['main']['temp_max']
        wind = first_forecast['wind']['speed']

        return {
            "city": city,
            "forecasted_weather": forecasted_weather,
            "approx_temp_min": round(temp_min, 1),
            "approx_temp_max": round(temp_max, 1),
            "approx_wind": round(wind, 1),
            "datetime": first_forecast['dt_txt']
        }

    except Exception as e:
        return {"error": str(e)}
#---------------------------------------------------------------------------------------------

def viewUserBookings(request):
    userEmail = request.session['email']
    login = request.session.get('login')
    getUserBookings = slotPaymentModel.objects.filter(userEmail=userEmail)
    return render(request, 'viewUserBookings.html', {'getUserBookings':getUserBookings, 'login':login})

def addTeam(request, paymentID):
    userEmail = request.session['email']
    login = request.session.get('login')
    getDetails = slotPaymentModel.objects.get(paymentID=paymentID)
    getUserDetails = User.objects.get(email=userEmail)
    if request.method == 'POST':
        team_members = request.POST.getlist('teamMembers')  # Get all team member inputs as a list

        # Save to the database
        teamModel.objects.create(
            teamLeaderName=getUserDetails.firstname, 
            team=team_members,
            teamLeaderMail=userEmail,
            groundName=getDetails.groundName,
            gameName=getDetails.gameName,
            location=getDetails.location
            )
        messages.success(request, 'Team added successfully')
        return redirect('addTeam', paymentID=paymentID)
    return render(request, 'addTeam.html', {'login':login, 'paymentID':paymentID, 'leaderName':getUserDetails.firstname})


def viewTeam(request):
    userEmail = request.session['email']
    login = request.session.get('login')
    getUserTeam = teamModel.objects.filter(teamLeaderMail=userEmail)
    return render(request, 'viewTeam.html', {'login':login, 'getUserTeam':getUserTeam})

def otherUsersBookingSlots(request):
    userEmail = request.session['email']
    login = request.session.get('login')
    getOtherUserSLots = teamModel.objects.exclude(teamLeaderMail=userEmail)
    return render(request, 'otherUsersBookingSlots.html', {'getOtherUserSLots':getOtherUserSLots, 'login':login})

def sendRequest(request, teamID):
    userEmail = request.session['email']
    getTeamDetails = teamModel.objects.get(teamID=teamID)
    userRequestModel.objects.create(
        requestReciever=getTeamDetails.teamLeaderMail,
        requestSender=userEmail,
        recieverTeamId=teamID,
        groundName=getTeamDetails.groundName,
        gameName=getTeamDetails.gameName,
        location=getTeamDetails.location
    )
    messages.success(request, 'Requset send successfully')
    return redirect('otherUsersBookingSlots')

def teamRequests(request):
    userEmail = request.session['email']
    login = request.session.get('login')
    getUserRequsts = userRequestModel.objects.filter(requestReciever=userEmail, requestStatus='not accepted')
    return render(request, 'teamRequests.html', {'getUserRequsts':getUserRequsts, 'login':login})

def acceptUserRequest(request, requestID):
    getRequestDetails = userRequestModel.objects.get(requestID=requestID)
    getTeamDetails = teamModel.objects.get(teamID=int(getRequestDetails.recieverTeamId))
    getUserDetails = User.objects.get(email=getRequestDetails.requestSender)
    addPlayer = getTeamDetails.team
    addPlayer.append(getUserDetails.firstname)
    getTeamDetails.team=addPlayer
    getTeamDetails.save()
    getRequestDetails.requestStatus='accepted'
    getRequestDetails.save()
    messages.success(request, 'Request accepted successfully')
    return redirect('teamRequests')


def deleteSlot(request, slotId):
    getSlot = groundSlotsModel.objects.get(slotId=slotId)
    getSlot.delete()
    return redirect('viewSlots')

def removeUserFromTeam(request, teamID, userName):
    getTeam = teamModel.objects.get(teamID=teamID)
    updated_list = [item for item in getTeam.team if item != userName]
    getTeam.team = updated_list
    getTeam.save()
    return redirect(viewTeam)




