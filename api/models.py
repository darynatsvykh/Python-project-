from django.db import models
from django.contrib.auth.models import AbstractUser


class Hobbies(models.Model):
    """Defines the attributes for Hobbies"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        """Returns a string representation showing """
        return f"{self.name} : {self.description}"
    
    def as_dict(self):
        """Returns a dictionary representation showing hobbies id, name and description"""
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description
        }
    
    
class UserHobbies(models.Model):
    """Through table for Users and Hobbies"""
    users = models.ForeignKey('User', on_delete=models.CASCADE)
    hobbies = models.ForeignKey('Hobbies', on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation showing users name, dob and hobbies"""
        return f"{self.users.name} , {self.users.dob} , {self.hobbies.name}"
    
    def as_dict(self):
        """Returns a dictionary representation of the UsersHobbies object"""
        return{
            'id' : self.id,
            'users' : {
                'id' : self.users.id,
                'name' : self.users.name,
                'dob' : self.users.dob
            },
            'hobbies' : {
                'id' : self.hobbies.id,
                'name' : self.hobbies.name,
                'description' : self.hobbies.description
            },
        }


class User(AbstractUser):
    """Defines the attributes for Users"""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique = True)
    dob = models.DateField(null=True, blank = True)
    hobbies = models.ManyToManyField(Hobbies, through="UserHobbies", blank=True)
    friends = models.ManyToManyField(to='self', through="FriendRequest", blank=True)


    def __str__(self):
        """Returns a string representation showing User name adn date of birth"""
        return f"{self.name} , {self.dob}"

    def as_dict(self):
        """Returns a dictionary representation showing User id, name, email and date of birth"""
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'dob' : self.dob,
            'hobbies': [hobby.name for hobby in self.hobbies.all()],
        }
    

class FriendRequest(models.Model):
    """Model to represent friend requests."""
    sender = models.ForeignKey('User', related_name='sent_friend_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey('User', related_name='received_friend_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")],
                              default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friend request from {self.sender.name} to {self.recipient.name}"



class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"
    

# class Profile(models.Model):
#     user = models.ForeignKey('api.User', on_delete=models.CASCADE)  # Reference the custom User model directly
#     bio = models.TextField()

#     def __str__(self):
#         return self.user.username