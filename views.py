def view(request):
    if user.request.has_perm('myapp.add_post'):
        # Allow user to create new post
    else:
        # Deny user access or show error message.
