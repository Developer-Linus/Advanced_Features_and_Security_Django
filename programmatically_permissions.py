from django.contrib.auth.models import Permission

# Get the permission
permission = Permission.objects.get(codename='add_post')

# Assign permission to a user
user.user_permissions.add(permission)

#Assign permission to a group
group.permissions.add(permission)
