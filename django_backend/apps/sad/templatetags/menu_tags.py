# -*- coding: utf-8 -*-
# método para mostrar en los template
from django import template
from django.template import resolve_variable, Context
import datetime
from django.template.loader import render_to_string
from django.contrib.sessions.models import Session
from django.conf import settings
from apps.sad.security import DataAccessToken
from apps.space.models import Enterprise, Headquart

from django.template.defaultfilters import stringfilter

from apps.helpers.message import Message
from apps.sad.security import Security, Menus

register = template.Library()

@register.simple_tag
def load(module):
	"""
	Interfáz del Método para cargar en variables los menús
	"""
	
	return Menus.load(module)

@register.simple_tag
def desktop(request):
	"""
	Interfáz del Método para renderizar el menú de escritorio
	"""
	
	return Menus.desktop(request)

@register.simple_tag
def desktop_items(request):
	"""
	Interfáz del Método para listar los items en el backend
	"""
	
	return Menus.desktop_items(request)


@register.simple_tag
def phone(request):
	"""
	Interfáz del Método para renderizar el menú de dispositivos móviles
	"""
	
	return Menus.phone(request)