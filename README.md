# Custom User Models and Authentication

This concept page aims to introduce a comprehensive guide on customizing user models and extending authentication mechanisms in Django to cater to specific application requirements.

## Concept Overview

Django comes equipped with a built-in user model that serves basic authentication needs. However, as your applications grow and evolve, you might require additional user information or alternative login methods. This concept delves into the methods of tailoring the user model and extending Django’s authentication system to align with your unique project specifications.

## Topics

- Enhancing the Default User Model
- Crafting Custom Authentication Backends

## Learning Objectives

- Recognize the limitations of the default Django user model.
- Master the creation of custom user models with supplementary fields.
- Implement custom authentication backends to enable diverse login methods (e.g., social login).
- Seamlessly integrate social login functionalities with Django authentication.

## Enhancing the Default User Model

The standard Django user model offers fundamental fields like username, email, and password. However, applications often demand additional data points such as phone numbers, addresses, or profile pictures. Custom user models empower you to incorporate these extra fields.

### Approaches to Customization

1. **AbstractBaseUser**: Inheriting from `AbstractBaseUser` provides extensive flexibility but necessitates implementing core methods like `get_username()` and `get_full_name()`. This approach grants granular control over user attributes and behavior.

   ```python
   from django.contrib.auth.models import AbstractBaseUser

   class CustomUser(AbstractBaseUser):
       email = models.EmailField(unique=True)
       phone_number = models.CharField(max_length=20)
       # ... additional fields and methods as required ...
   ```

2. **AbstractUser**: This method extends the existing user model while preserving default fields and functionality. It’s suitable for scenarios where you need to add a few extra fields without altering the core user model structure.

   ```python
   from django.contrib.auth.models import AbstractUser

   class CustomUser(AbstractUser):
       bio = models.TextField(blank=True)
       # ... additional fields as needed ...
   ```

### Essential Considerations

- **AUTH_USER_MODEL Configuration**: In your `settings.py` file, ensure you set the `AUTH_USER_MODEL` variable to point to your newly created custom user model. This informs Django about the model to utilize for user management.
- **Method Implementation**: Based on your chosen approach (`AbstractBaseUser` or `AbstractUser`), implement the necessary methods and manager classes to ensure proper user management functionality.

## Crafting Custom Authentication Backends

Django empowers you to extend or override the default authentication backend to accommodate diverse login methods. This flexibility allows you to integrate social login options, two-factor authentication, or any custom authentication flow you desire.

### Steps to Implementation

1. **Define a Custom Backend Class**: Create a class that inherits from `BaseBackend` and implement the `authenticate()` and `get_user()` methods. These methods define how user authentication and retrieval are handled.

   ```python
   from django.contrib.auth.backends import BaseBackend

   class EmailBackend(BaseBackend):
       def authenticate(self, request, username=None, password=None):
           # Implement logic to authenticate user using email and password
           # ...

       def get_user(self, user_id):
           # Implement logic to retrieve user based on user ID
           # ...
   ```

2. **Register the Custom Backend**: In your `settings.py` file, add the path to your custom backend class within the `AUTHENTICATION_BACKENDS` setting. This informs Django about the available authentication methods.

   ```python
   AUTHENTICATION_BACKENDS = [
       'path.to.EmailBackend',  # Your custom backend
       'django.contrib.auth.backends.ModelBackend',  # Keep the default backend as a fallback
   ]
   ```

## Practice Exercises

- Enhance your learning by creating a custom user model enriched with fields like date of birth and profile picture.
- Implement an authentication backend that enables users to log in using their email address instead of a username.

## Additional Resources

- [Django Custom User Model Documentation](https://intranet.alxswe.com/rltoken/ett-FApY6-NN0yXwZ0qnWw)
- [Django Authentication Backends](https://intranet.alxswe.com/rltoken/jrlgYEoefTeld6cDZKqbIQ)
