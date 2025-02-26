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

# Extras

Let’s break down the concept of **custom authentication backends**.

---

### What Is a Custom Authentication Backend?

In Django, an **authentication backend** is a system that handles how users are authenticated (logged in). By default, Django uses the `ModelBackend`, which authenticates users based on the username and password stored in the database.

However, sometimes you might want to customize this process. For example:

- Allow users to log in with their **email** instead of a username.
- Integrate **social login** (e.g., Google, Facebook).
- Add **two-factor authentication**.
- Authenticate users against an external system (e.g., LDAP).

To do this, you can create a **custom authentication backend**.

---

### How Does It Work?

A custom authentication backend is a Python class that defines two key methods:

1. **`authenticate()`**: This method checks if the user's credentials (e.g., email and password) are valid and returns the user object if they are.
2. **`get_user()`**: This method retrieves a user object based on a unique identifier (e.g., user ID).

Once you create this backend, you tell Django to use it by adding it to the `AUTHENTICATION_BACKENDS` setting in `settings.py`.

---

### Steps to Create a Custom Authentication Backend

1. **Define the Custom Backend Class**:

   - Create a class that inherits from `BaseBackend`.
   - Implement the `authenticate()` and `get_user()` methods.

2. **Register the Backend**:
   - Add the path to your custom backend in the `AUTHENTICATION_BACKENDS` setting in `settings.py`.

---

### Example: Phone Number Authentication

Let’s create a custom authentication backend where users log in with their **phone number** instead of a username or email.

#### Step 1: Define the Custom Backend Class

Create a file called `backends.py` in your app (e.g., `accounts/backends.py`):

```python
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        # Check if a user with the given phone number exists
        try:
            user = User.objects.get(phone_number=phone_number)
            # Verify the password
            if user.check_password(password):
                return user  # Authentication successful
        except User.DoesNotExist:
            return None  # No user found with this phone number
        return None  # Password is incorrect

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

#### Step 2: Update the User Model

Ensure your custom user model has a `phone_number` field:

```python
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Default login field
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    def __str__(self):
        return self.email
```

#### Step 3: Register the Custom Backend

In `settings.py`, add your custom backend to the `AUTHENTICATION_BACKENDS` list:

```python
AUTHENTICATION_BACKENDS = [
    'accounts.backends.PhoneBackend',  # Your custom backend
    'django.contrib.auth.backends.ModelBackend',  # Default backend (fallback)
]
```

#### Step 4: Update the Login View

In your login view, modify the form to accept a phone number instead of a username:

```python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid phone number or password'})
    return render(request, 'login.html')
```

#### Step 5: Update the Login Form

In your `login.html` template, update the form fields:

```html
<form method="post">
  {% csrf_token %}
  <label for="phone_number">Phone Number:</label>
  <input type="text" name="phone_number" required />
  <br />
  <label for="password">Password:</label>
  <input type="password" name="password" required />
  <br />
  <button type="submit">Login</button>
</form>
```

---

### How It Works

1. When a user submits the login form, the `phone_number` and `password` are sent to the `login_view`.
2. The `authenticate()` method in the `PhoneBackend` is called.
   - It looks for a user with the given `phone_number`.
   - If the user exists and the password is correct, it returns the user object.
3. If authentication is successful, the user is logged in using Django's `login()` function.

---

### Why Is This Useful?

- **Flexibility**: You can authenticate users in any way you want (e.g., phone number, social login, etc.).
- **Fallback**: You can keep the default `ModelBackend` as a fallback for other authentication methods.
- **Custom Logic**: You can add additional checks (e.g., two-factor authentication) in the `authenticate()` method.

---

### Key Takeaways

- A **custom authentication backend** allows you to define your own rules for logging in users.
- You need to implement two methods: `authenticate()` and `get_user()`.
- Register your backend in `AUTHENTICATION_BACKENDS` to make it active.

````markdown
# Permissions and Authorization

This concept page aims to discuss the implementation and management of permissions and authorization mechanisms within Django to enforce fine-grained access control and enhance the security of your web applications.

## Concept Overview

Permissions and authorization are fundamental aspects of web application security. They allow you to control which users can access specific resources or perform certain actions within your Django application. This concept explores Django’s built-in permission system and how to effectively manage access control.

## Topics

- Understanding Permissions and Groups
- Assigning Permissions
- Permission Checks in Views and Templates
- Custom Permissions

## Learning Objectives

- Grasp the core concepts of permissions and groups in Django.
- Learn how to create and assign permissions to users and groups.
- Implement permission checks within views and templates to restrict access.
- Define and utilize custom permissions for granular access control.

## Understanding Permissions and Groups

### Permissions

Permissions are fine-grained access controls that define specific actions a user can perform, such as “can add post,” “can change user,” or “can delete comment.” Django provides a set of built-in permissions for common actions related to models.

### Groups

Groups allow you to categorize users and assign permissions to the entire group at once. This simplifies permission management, especially when dealing with many users.

## Assigning Permissions

### 1. Django Admin

The Django admin interface provides a user-friendly way to manage permissions. You can assign permissions to individual users or groups directly from the admin panel.

### 2. Programmatically

You can also assign permissions programmatically using the `user.user_permissions.add()` and `group.permissions.add()` methods. This is useful for automating permission assignments or integrating with custom user registration processes.

```python
from django.contrib.auth.models import Permission

# Get the permission
permission = Permission.objects.get(codename='add_post')

# Assign permission to a user
user.user_permissions.add(permission)

# Assign permission to a group
group.permissions.add(permission)
```
````

## Permission Checks in Views and Templates

### Views

In your views, you can check if a user has a specific permission using the `user.has_perm()` method. This allows you to control which parts of the view logic are executed based on the user’s permissions.

```python
def my_view(request):
    if request.user.has_perm('app_name.add_post'):
        # Allow user to create a new post
        ...
    else:
        # Deny access or show an error message
        ...
```

### Templates

Django’s template system provides the `{% if perms %}` tag to conditionally render content based on the user’s permissions.

```django
{% if perms.app_name.add_post %}
    <a href="{% url 'create_post' %}">Create New Post</a>
{% endif %}
```

## Custom Permissions

While Django’s built-in permissions cover many common use cases, you may need more granular control for specific applications. You can create custom permissions by defining them in your models:

```python
class Post(models.Model):
    # ... other fields ...

    class Meta:
        permissions = [
            ("can_publish_post", "Can publish post"),
        ]
```

This creates a new permission called “can_publish_post” which you can then assign to users or groups just like any other permission.

## Practice Exercise

1. Explore the Django admin interface and practice assigning permissions to users and groups.
2. Implement permission checks in a view to restrict access to a specific section of your application based on user permissions.
3. Define a custom permission for a model in your project and use it to control access to a particular action.

## Additional Resources

- [Django Permissions Documentation](https://intranet.alxswe.com/rltoken/VkBgLyvjvUVC2fByg9ECYw)
- [Django Groups Documentation](https://intranet.alxswe.com/rltoken/8CUFiOq155V8qysRZxRiLQ)

```

```

Here’s the text formatted as Markdown for better readability when uploaded to GitHub:

```markdown
# Security Practices in Django

This concept page aims to explore essential knowledge and best practices to fortify the security of your Django applications and safeguard against common web vulnerabilities.

## Concept Overview

Building secure web applications is paramount for protecting sensitive data and maintaining user trust. Django, renowned for its robust security features, provides developers with tools and guidance to create resilient applications. This concept delves deeper into key security considerations and practices that are essential when developing with Django.

## Topics

- Common Web Vulnerabilities and their Impact
- Leveraging Django’s Built-in Security Features
- Implementing Secure Development Practices

## Learning Objectives

- Gain a comprehensive understanding of common web vulnerabilities and their potential consequences.
- Effectively utilize Django’s built-in security features to mitigate risks.
- Implement secure development practices to prevent vulnerabilities from creeping into your applications.
- Maintain the security of your Django applications by staying updated with the latest security patches.

## Common Web Vulnerabilities and their Impact

Recognizing and understanding common web vulnerabilities is the first step towards building secure applications. Here are some prevalent threats and their potential impact:

- **Cross-Site Scripting (XSS):** Attackers inject malicious scripts into web pages viewed by users. These scripts can steal sensitive data like cookies or login credentials, deface websites, or redirect users to phishing sites.
- **Cross-Site Request Forgery (CSRF):** Malicious actors trick users into performing actions on a trusted website without their knowledge or consent. This can lead to unauthorized fund transfers, data modification, or account takeover.
- **SQL Injection:** Attackers manipulate database queries to gain unauthorized access to sensitive data, modify data, or even delete entire databases. This can have severe consequences, including data breaches and financial losses.
- **Clickjacking:** Users are deceived into clicking seemingly innocuous elements on a web page, while hidden elements perform unintended actions in the background. This can lead to the installation of malware, unauthorized purchases, or social media hijacking.

## Leveraging Django’s Built-in Security Features

Django comes equipped with several built-in security features designed to mitigate these vulnerabilities:

- **CSRF Protection:** Django’s CSRF middleware automatically generates and validates tokens for forms. This ensures that only forms originating from your own website can submit data, preventing CSRF attacks.
- **XSS Protection:** Django templates automatically escape user-provided data by default. This process converts special characters into harmless entities, preventing malicious scripts from being executed in the browser.
- **SQL Injection Protection:** Django’s querysets and ORM (Object-Relational Mapper) provide a secure way to interact with databases. They use parameterization to ensure that user input is treated as data, not executable code, preventing SQL injection attacks.
- **Password Hashing:** Django stores passwords securely using robust hashing algorithms like PBKDF2 or Argon2. This makes it extremely difficult for attackers to crack passwords even if they gain access to the hashed password data.

## Implementing Secure Development Practices

While Django provides a strong foundation for security, adopting secure development practices is essential to build truly resilient applications:

- **Validate User Input:** Always validate and sanitize user input to prevent malicious data from entering your application. This involves checking for data type, length, format, and allowed characters.
- **Use Parameterized Queries:** Avoid using raw SQL queries that concatenate user input directly into the query string. Instead, use Django’s ORM or parameterized queries, which separate data from code and prevent SQL injection.
- **Keep Dependencies Updated:** Regularly update Django, its dependencies, and any third-party libraries you use in your application. This ensures you benefit from the latest security patches and bug fixes.
- **Implement Strong Authentication:** Enforce strong password policies that require users to create complex passwords with a mix of characters. Consider implementing multi-factor authentication for an extra layer of security.
- **Use HTTPS:** Implement HTTPS to encrypt communication between the client and server. This protects sensitive data transmitted over the network, such as login credentials and financial information, from eavesdropping and man-in-the-middle attacks.
- **Principle of Least Privilege:** Grant users the minimum level of access necessary to perform their tasks. This limits the potential damage in case of a compromised account.

## Practice Exercise

1. Review a recent Django project and identify areas where you can enhance security practices. Consider input validation, authentication mechanisms, and data handling procedures.
2. Implement input validation for a form in your application. Use Django’s form validation features or custom validation logic to ensure data integrity.
3. Research and configure HTTPS for your Django application. Obtain an SSL/TLS certificate and set up your web server to enforce HTTPS connections.

## Additional Resources

- [Django Security Documentation](https://intranet.alxswe.com/rltoken/putNWUiu4vGYdM3A4GQIPw)
- [OWASP Top 10 Web Application Security Risks](https://intranet.alxswe.com/rltoken/UPzX60dl1a6kTfdKIdIb0g)
```
