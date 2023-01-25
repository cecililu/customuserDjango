from rest_framework import permissions

class CustomObjectLevelDisasterModel(permissions.BasePermission): 
    edit_methods = ("PUT", "PATCH")
    def has_permission(self, request, view):
        print(request.method)
        if request.method in ['GET']:
            return True
        print('has_permissions')
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        print('has_permissions onject run')
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        # if obj.author== request.user:
        #     return True 
        if request.user.is_staff and request.user.municipality==obj.municipality or request.user.ward==obj.ward:
            return True
        return False
    
    
class CustomObjectLevelActivityModel(permissions.BasePermission): 
    # edit_methods = ("PUT", "PATCH")
    def has_permission(self, request, view):
        print(request.method)
        if request.method in ['GET']:
            return True
        print('has_permissions')
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        print('has_permissions onject run')
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        # if obj.author== request.user:
        #     return True 
        if request.user.is_authenticated :
            return True
        return False
    