# -*- coding: utf-8 -*-

from functools import wraps
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str

from django.shortcuts import resolve_url
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, get_object_or_404, render,redirect, Http404
from apps.helpers.message import Message
from django.views.generic import TemplateView
from django.template.context import RequestContext

def is_admin(view_func):
    '''
    Verifica si es admin o no
    '''
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse("<h3>Necesitas privilegios de aministrador para realizar esta acción</h3>")
        return view_func(request, *args, **kwargs) 
        
    return _wrapped_view_func

def permission_resource_required(function=None, template_denied_name="denied_mod_backend.html"):
    """
    
    """
    actual_decorator = permission_resource_required_decorator(
        template_denied_name=template_denied_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def permission_resource_required_decorator(template_denied_name="denied_mod_backend.html"):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs) :
            permiso=""
            recurso="/"
            response = HttpResponse()
            response.write('<script type="text/javascript">')
            response.write('alert("Hola")')
            response.write('</script>')
            try:
                path = request.path.strip("/") #request.get_full_path().strip("/") #"/apps/controller/action/" to "apps/controller/action"
                print "path=%s" % path
                print "request path=%s" % request.path
            except Exception, e:
                raise Exception("%s. Asigne adecuadamente el parámetro template_denied_name " % e)
            
            #if path.startswith("/"):
            #    path = path[1:] #quitando / del extremo izq
            #if path.endswith("/"):
            #    path = path[:-1] #quitando / del extremo der
            #print "path=%s" % path
            #permiso=path.replace('/','.') #permiso='params.locality_listx'
            #print "permiso=%s" % permiso
            if "/" in path:
                path_list = path.split('/')
        	    #print ".".join(path_list)
                permiso="%s" % (path_list[0])
                recurso="/%s/" % (path_list[0])
                if len(path_list) > 1:
                    permiso = "%s.%s" % (path_list[0], path_list[1])
                    recurso = "/%s/%s/" % (path_list[0], path_list[1])
                
                if not isinstance(permiso, (list, tuple)):
                    perms = (permiso, )
                else:
                    perms = permiso
                if not request.user.has_perms(perms):
                    if len(path_list) > 2:
                        permiso = "%s.%s_%s" % (path_list[0], path_list[1], path_list[2])
                        recurso = "/%s/%s/%s/" % (path_list[0], path_list[1], path_list[2])
            print "permiso=%s" % permiso
            print "recurso=%s" % recurso
            if not isinstance(permiso, (list, tuple)):
	            perms = (permiso, )
            else:
	            perms = permiso
            if request.user.has_perms(perms):
	            return view_func(request, *args, **kwargs)
            else:
                #if login_url:
                #    Message.warning(request, ("Tu no posees permisos para acceder a <b>%(route)s</b>") % {'route':recurso} )
                #    return redirect(login_url)
                #else:
                Message.warning(request, ("Tu no posees permisos para acceder a <b>%(route)s</b>") % {'route':recurso} )
                return render_to_response(template_denied_name, {'': ''}, context_instance=RequestContext(request))
        return _wrapped_view
    return decorator


#Metodos decorators en testing

def permission_codename_required(perm, login_url='mod_backend_dashboard', raise_exception=False):
	"""
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
	"""
	def decorator(func):
	    def inner_decorator(request, *args, **kwargs):
        	path = request.get_full_path() #="/apps/controller/"
        	path = path[1:-1] #quitando los / de ambos extremos
        	permiso=path.replace('/','.')
        	permiso='params.locality_list'
        	print permiso
        	#old_privilegios_r = path.split('/')
        	#print ".".join(old_privilegios_r)

        	if not isinstance(permiso, (list, tuple)):
	            perms = (permiso, )
	        else:
	            perms = permiso
	        if request.user.has_perms(perms):
	            return func(request, *args, **kwargs)
	        else:
	            Message.warning(request, ("Tu no posees privilegios para acceder a <b>%(route)s</b>") % {'route':permiso} )
	            return HttpResponseRedirect(reverse(login_url))
	            #return HttpResponse("<h3>Tu no posees privilegios para realizar esta acción</h3>")
	        
	    return wraps(func)(inner_decorator)
	return decorator





def xlogin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    print redirect_field_name
    actual_decorator = eeee(
        login_url=login_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def eeee(login_url=None):
	def decorator(view_func):
	    @wraps(view_func, assigned=available_attrs(view_func))
	    def _wrapped_view(request, *args, **kwargs):
	        path = request.get_full_path()
	        
	        resolved_login_url = force_str(resolve_url(login_url or settings.LOGIN_URL))
	        print path
	        if request.user.is_superuser:
	            return view_func(request, *args, **kwargs) 
	        else:
	            return HttpResponseRedirect(reverse('mod_backend_dashboard')) 
	        
	    return _wrapped_view
	return decorator



# eliminar estos decorators


def user_passes_testx(test_func=None, login_url=None):
	def decorator(view_func):
	    @wraps(view_func, assigned=available_attrs(view_func))
	    def _wrapped_view(request, *args, **kwargs):
	        print login_url
	        if request.user.is_superuser:
	            return view_func(request, *args, **kwargs) 
	        else:
	            return HttpResponseRedirect(reverse('mod_backend_dashboard')) 
	        
	    return _wrapped_view
	return decorator





def user_passes_testy(test_func=None, login_url=None):
	actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url
    )
	return actual_decorator


def access_required(permission=None):
	def decorator(func):
	    def inner_decorator(request, *args, **kwargs):
	        #if permission == 'admin':
	        if request.user.is_superuser:
	            return func(request, *args, **kwargs)
	        else:
	            Message.warning(request, ("Tu no posees privilegios para acceder a <b>%(route)s</b>") % {'route':'locality_list'} )
	            return HttpResponseRedirect(reverse('mod_backend_dashboard'))
	            #return HttpResponse("<h3>Tu no posees privilegios para acceder a esta pagina</h3>")
	        
	    return wraps(func)(inner_decorator)
	return decorator


def access_requiredx(view_func): 
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs) 
        else:
            return HttpResponseRedirect(reverse('mod_backend_dashboard')) 
        
    return _wrapped_view_func

def xpermission_requiredx(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)