from django.contrib import admin
from .models import User, Hobbies, FriendRequest
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


# Register your models here.
class SentFriendRequestInline(admin.TabularInline):
    """Inline view of sent friend requests in the User admin."""
    model = FriendRequest
    fk_name = 'sender'  # Define the foreign key for relationship
    extra = 0  # No extra empty rows
    fields = ('recipient', 'status', 'timestamp')  # Define displayed fields
    readonly_fields = ('timestamp',)


class ReceivedFriendRequestInline(admin.TabularInline):
    """Inline view of received friend requests in the User admin."""
    model = FriendRequest
    fk_name = 'recipient'  # Define the foreign key for relationship
    extra = 0  # No extra empty rows
    fields = ('sender', 'status', 'timestamp')
    readonly_fields = ('timestamp',)


class UserHobbiesInline(admin.TabularInline):
    """Inline class for managing the User-Hobbies relationship in the models"""
    model = User.hobbies.through
    extra = 3

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configurations for User model."""
    inlines = [SentFriendRequestInline, ReceivedFriendRequestInline]
    list_display = ('name', 'email', 'dob')
    list_filter = ('hobbies',)
    search_fields = ('name', 'email',)
    inlines = [UserHobbiesInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Hobbies)
class HobbiesAdmin(admin.ModelAdmin):
    """Admin configurations for Hobbies model."""
    list_display = ('name', 'description')
    search_fields = ('name',)


class UserCreationForm(forms.ModelForm):
    
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'status', 'timestamp')  # Columns to display in the admin list view
    list_filter = ('status', 'timestamp')  # Filters for the right sidebar
    search_fields = ('sender__name', 'recipient__name')  # Search bar for sender and recipient names
    ordering = ('-timestamp',)  # Order by most recent requests
    readonly_fields = ('timestamp',)  # Make timestamp read-only in the admin interface

admin.site.register(FriendRequest, FriendRequestAdmin)
