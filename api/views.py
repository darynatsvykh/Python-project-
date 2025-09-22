from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from .models import Hobbies
from .models import Hobbies, User, FriendRequest
from django.core.paginator import Paginator
import json

@login_required
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', {})


@ensure_csrf_cookie
def csrf_token_view(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        print("CSRF obtained: ", csrf_token)
        return JsonResponse({'csrfToken': csrf_token})
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_protect 
def login_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return JsonResponse({
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "dob": user.dob
                    },
                    "message": "Login successful"
                }, status=200)             
            else:
                # Authentication failed
                messages.error(request, "Invalid username or password")
                return JsonResponse({'error': 'Invalid username or password'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # If not a POST request, return method not allowed
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@login_required
@csrf_protect
def logout_view(request):
    if request.method == "POST":
        logout(request)
        print("logged out")
        return JsonResponse({"message": "Logged out successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data['email']
            name = data['name']
            last_name = data['surname']
            dob = data['dob']

            User = get_user_model()

            if User.objects.filter(username=username).exists():
                return JsonResponse({"detail": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password, name=name, last_name=last_name, email=email, dob=dob)
            user.save()
            return JsonResponse({"detail": "User registered successfully"}, status=201)

        except ValidationError as e:
            return JsonResponse({"detail": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=400)

    return JsonResponse({"detail": "Invalid request method"}, status=405)
 

def display_hobbies(request):
    """View to get all hobbies from DB"""

    if request.method == 'GET':
        hobbies = Hobbies.objects.all()
        return JsonResponse({'Hobbies': [hobby.as_dict() for hobby in hobbies]})

@csrf_exempt
def add_hobby(request):
    """View to add a new hobby to DB"""

    if request.method == "POST":
        body = json.loads(request.body)
        name = body.get("name")
        description = body.get("description")

        if not name:
            return JsonResponse({'error': 'Name of hobby required'})

        if Hobbies.objects.filter(name=name).exists():
            return JsonResponse({'error': 'That hobby already exists'})

        hobby = Hobbies.objects.create(name=name, description=description)

        return JsonResponse({'hobby': hobby.as_dict()})

@csrf_exempt
def delete_hobby(request, hobby_id):
    """View to delete hobby from DB"""

    if request.method == "DELETE":
        hobby = Hobbies.objects.get(id=hobby_id)
        hobby.delete()
        return JsonResponse({'message': 'Hobby deleted successfully'})

def get_all_users(request):
    """View to get all users and their details"""

    if request.method == 'GET':
        User = get_user_model()
        users = User.objects.all()

        page_number = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(users, page_size)
        page_obj = paginator.get_page(page_number)

        users_data = [user.as_dict() for user in page_obj.object_list]

        response = {
            'users': users_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        }
        return JsonResponse(response, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_similar_users(request, user_id):
    """View to get a list of users with the most similar set of hobbies"""

    if request.method == 'GET':
        User = get_user_model()

        try:
            current_user = User.objects.prefetch_related('hobbies').get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': f'User with id {user_id} does not exist'}, status=404)

        other_users = User.objects.prefetch_related('hobbies').exclude(id=user_id)

        user_similarity = []
        current_user_hobbies = set(hobby.id for hobby in current_user.hobbies.all())

        for user in other_users:
            other_user_hobbies = set(hobby.id for hobby in user.hobbies.all())
            common_hobbies = current_user_hobbies.intersection(other_user_hobbies)
            user_similarity.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'dob': user.dob,
                'hobbies': [hobby.name for hobby in user.hobbies.all()],
                'common_hobby_count': len(common_hobbies),  # Number of common hobbies
            })

        sorted_users = sorted(user_similarity, key=lambda x: x['common_hobby_count'], reverse=True)

        return JsonResponse({'similar_users': sorted_users}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def profile_page(request, username):
    """View to display and update user profile"""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        try:
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'dob': user.dob,
            }
            user_hobbies = [{'id': hobby.id, 'name': hobby.name} for hobby in user.hobbies.all()]
            return JsonResponse({'user': user_data, 'hobbies': user_hobbies})
        except Exception as e:
            print(f"Error in GET /profile_page: {e}")
            return JsonResponse({'error': 'Failed to retrieve user data'}, status=500)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            name = body.get('name')
            email = body.get('email')
            dob = body.get('dob')
            hobby_ids = body.get('hobbies', [])

            if name:
                user.name = name
            if email:
                user.email = email
            if dob:
                user.dob = dob

            if hobby_ids:
                hobbies = Hobbies.objects.filter(id__in=hobby_ids)
                user.hobbies.set(hobbies)

            user.save()
            
            hobbies_data = [{'id': hobby.id, 'name': hobby.name} for hobby in user.hobbies.all()]
            return JsonResponse({
                'success': 'Profile updated successfully',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'dob': user.dob,
                    'hobbies': hobbies_data,
                }
            })
        except Exception as e:
            print(f"Error in POST /profile_page: {e}")
            return JsonResponse({'error': 'Failed to update profile'}, status=500)



@csrf_exempt
def update_password(request, username):
    """View to update user password"""
    if request.method == 'POST':
        try:
            # Fetch the user based on the username
            user = User.objects.get(username=username)
            
            # Parse the new password from the request body
            body = json.loads(request.body)
            new_password = body.get('password')

            if not new_password:
                return JsonResponse({'error': 'Password not provided'}, status=400)

            # Hash and update the user's password
            user.password = make_password(new_password)
            user.save()

            return JsonResponse({'success': 'Password updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            print(f"Error in POST /profile/{username}/password/: {e}")
            return JsonResponse({'error': 'Failed to update password'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def send_friend_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            sender_id = data.get('sender_id')
            recipient_id = data.get('recipient_id')

            if not sender_id or not recipient_id:
                return JsonResponse({"error": "Both sender_id and recipient_id are required."}, status=400)
            
            sender = User.objects.get(id=sender_id)
            recipient = User.objects.get(id=recipient_id)

            # Check if a friend request already exists
            if FriendRequest.objects.filter(sender=sender, recipient=recipient).exists():
                return JsonResponse({"error": "Friend request already sent."}, status=400)

            # Create a new friend request
            friend_request = FriendRequest.objects.create(sender=sender, recipient=recipient)
            return JsonResponse({
                "message": "Friend request sent successfully!",
                "status": "pending",  # Include a status field
                "friend_request_id": friend_request.id,
                "send_id": sender_id,
                "receiver_id": recipient_id,
            }, status=200)
        
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Sender or Recipient not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON provided."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

       

    return JsonResponse({"error": "Method not allowed."}, status=405)

@login_required
def get_pending_friend_requests(request):
    user = request.user
    pending_requests = FriendRequest.objects.filter(recipient=user, status="pending").select_related("sender")
    result = [
        {
            "id": fr.id,
            "sender_id": fr.sender.id,
            "sender_name": fr.sender.username,  # Retrieve sender's username
        }
        for fr in pending_requests
    ]

    return JsonResponse({"pending_requests": result}, safe=False)

@login_required
def manage_friend_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            friend_request_id = data.get("friend_request_id")
            action = data.get("action")  # "accept" or "reject"

            # Validate action and friend request
            if action not in ["accept", "reject"]:
                return JsonResponse({"error": "Invalid action."}, status=400)

            friend_request = FriendRequest.objects.filter(id=friend_request_id, recipient=request.user).first()
            if not friend_request:
                return JsonResponse({"error": "Friend request not found or not authorized."}, status=404)

            # Update the friend request status based on action
            if action == "accept":
                friend_request.status = "accepted"
                # You can add logic to create a "friendship" relationship here
            elif action == "reject":
                friend_request.status = "rejected"

            friend_request.save()
            return JsonResponse({"message": f"Friend request {action}ed successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)