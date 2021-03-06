# _*_ coding: utf-8 _*_
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, render,redirect
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from apps.space.models import Headquart
from django.contrib.auth.models import User
from apps.space.models import Association, Enterprise, Headquart, Solution
from apps.sad.security import DataAccessToken
from apps.sad.models import *
from django.db.models import Q

#@csrf_exempt
def index(request):
	
	t = {
		'page_module':("Home"),
		'page_title':("Django backend Manager."),
		}
	return render_to_response("home/index.html", t, context_instance = RequestContext(request))

#@csrf_exempt
def choice_headquart(request):
	
	headquart_list_by_user=[]
	print "\n\n\n\n\n"
	headquart_list = []
	if request.user.is_superuser:
		headquart_list = Headquart.objects.filter().distinct() #Trae todo
	else:
		if request.user.id:
			print "--%s" % request.user.id
			headquart_list = Headquart.objects.filter(userprofileheadquart__user__id = request.user.id).distinct() #request.user.id
	
	for headquart in headquart_list:
		#print u"--%s" % (headquart)
		group_list = Group.objects.filter(userprofileheadquart__headquart__id = headquart.id, userprofileheadquart__user__id = request.user.id).distinct()
		#for group in group_list:
		#	print u"-- --%s" % (group)
		module_list = Module.objects.filter(groups__in = group_list).distinct()
		#for module in module_list:
		#	print u"-- -- ---%s" % (module)
		if request.user.is_superuser:
			'''
			permitir ingresar al módulo:Django Backend 
			'''
			if len(module_list)==0:
				module_list = Module.objects.filter(module = Module.DBM).distinct()
			else:
				if Module.objects.get(module = Module.DBM) not in module_list:
					module_list=Module.objects.filter(Q(groups__in = group_list) | Q(module = Module.DBM) ).distinct()

		headquart_list_by_user.append({
			'association': headquart.association,
			'enterprise': headquart.enterprise,
			'headquart': headquart,
			'modules': module_list,
			'groups': group_list,
			})
	
	t = {
		'page_module':("Elegir Módulo"),
		'page_title':("Listado de empresas en los cuales colabora."),
		'headquart_list': headquart_list_by_user,
		}
	return render_to_response("home/choice_headquart.html", t, context_instance = RequestContext(request))

