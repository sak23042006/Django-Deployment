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
    login = request.session['login']
    data = Grounds.objects.all()
    return render(request, 'viewgrounds.html',{'login':login,'data':data})

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
    login = request.session.get('login')
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    allSlots = groundSlotsModel.objects.filter(date__in=[today, tomorrow])
    return render(request, 'viewSlots.html', {'login':login, 'allSlots':allSlots})

def addSlots(request):
    login = request.session.get('login')

    if request.method == 'POST':
        groundName = request.POST.get('groundName')
        getDate = request.POST.get('date')
        is_available = True if request.POST.get('is_available_value') == '1' else False  # Fix: Compare string

        end_time = request.POST.get('end_time')
        formatted_date1 = datetime.strptime(getDate, '%Y-%m-%d').date()
        formatted_date = datetime.strptime(getDate, '%Y-%m-%d').strftime('%Y-%m-%d')
        print('DDDDDDDDDDDDD', formatted_date)
        if Grounds.objects.filter(groundname__iexact=groundName).exists():
            getGround = Grounds.objects.get(groundname__iexact=groundName)  # Fix: use .get() instead of .filter() when fetching one
            getGroundLocation = getGround.location
            getGameName = getGround.gamename
            getPrice = getGround.price
            result = run_weather_forecast_pipeline(formatted_date)
            print('PPPPPPPPPPPPPPPPPPPPPPP', result)
            print('weather Report', result['forecasted_weather'])

            if result['forecasted_weather'] == 'rain':
                getPrice = getPrice*0.5

            if end_time:
                try:
                    start_time_str, end_time_str = end_time.split('-')
                    start_time_str = start_time_str.strip()
                    end_time_str = end_time_str.strip()
                except ValueError:
                    start_time_str, end_time_str = None, None
            else:
                start_time_str, end_time_str = None, None

            # Create and save slot
            groundS = groundSlotsModel(
                groundName=groundName,
                start_time=start_time_str,
                end_time=end_time_str,
                is_available=is_available,
                location=getGroundLocation,
                gameName = getGameName,
                slotPrice = getPrice,
                date = formatted_date1,
                weatherReport=result['forecasted_weather']
            )
            groundS.save()
            messages.success(request, 'Slot added sucessfully')
            return redirect('addSlots')  # Redirect after successful creation
        else:
            messages.success(request, 'Ground name exits')
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
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_weather_forecast_pipeline(date_str):
    try:
        # Load dataset
        df = pd.read_csv("seattle-weather.csv")

        # Convert 'date' column to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Extract features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['dayofweek'] = df['date'].dt.dayofweek

        # Simplify weather types
        df['weather'] = df['weather'].replace({
            'rain': 'rain',
            'sun': 'sun',
            'fog': 'sun',
            'drizzle': 'sun',
            'snow': 'sun'
        })

        # Encode target
        label_encoder = LabelEncoder()
        df['weather_encoded'] = label_encoder.fit_transform(df['weather'])

        # Features and target
        X = df[['year', 'month', 'day', 'dayofweek']]
        y = df['weather_encoded']

        # Train/test split and model training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Convert input date
        input_date = pd.to_datetime(date_str)
        year, month, day, dayofweek = input_date.year, input_date.month, input_date.day, input_date.weekday()

        # Predict
        input_features = pd.DataFrame([[year, month, day, dayofweek]], columns=['year', 'month', 'day', 'dayofweek'])
        pred_encoded = model.predict(input_features)[0]
        predicted_weather = label_encoder.inverse_transform([pred_encoded])[0]

        # Simulate temperature and wind
        subset = df[(df['month'] == month) & (df['day'] == day)]
        if subset.empty:
            subset = df[df['month'] == month]

        temp_max = subset['temp_max'].mean()
        temp_min = subset['temp_min'].mean()
        wind = subset['wind'].mean()

        return {
            "date": date_str,
            "forecasted_weather": predicted_weather,
            "approx_temp_max": round(temp_max, 1),
            "approx_temp_min": round(temp_min, 1),
            "approx_wind": round(wind, 1)
        }

    except Exception as e:
        return {"error": str(e)}
result = run_weather_forecast_pipeline("2025-04-15")

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




