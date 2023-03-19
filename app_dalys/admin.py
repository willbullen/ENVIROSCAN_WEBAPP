from django.contrib import admin
from .models import Node_Category, Node_Region, Node_Type, Node_List, Node_Water, Node_Power, Node_Temperature

admin.site.register(Node_Category)
admin.site.register(Node_Region)
admin.site.register(Node_Type)
admin.site.register(Node_List)
admin.site.register(Node_Water)
admin.site.register(Node_Power)
admin.site.register(Node_Temperature)