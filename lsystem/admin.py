import pygame
import sys

from django.contrib import admin
from .models import Axiom, Tree, Rule, TreeRule, Branch

WIDTH = 800
HEIGHT = 640

def grow(modeladmin, request, queryset):
    """
    Grows a tree
	"""
    for tree in queryset:
    	tree.grow()
	rows_updated = queryset.count()
    if rows_updated == 1:
        count_bit = "1 tree was"
    else:
        count_bit = "%s trees were" % rows_updated
    modeladmin.message_user(request, "%s successfully grown." % count_bit)


def draw(modeladmin, request, queryset):
    """
    Displays a tree using pygame
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    modeladmin.message_user(request, "Successfully drew trees to screen.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return;
        for tree in queryset:
            if tree.root is not None:
                tree.draw(screen)
        pygame.display.update()


class TreeRuleInline(admin.StackedInline):

    model = TreeRule
    fieldsets = (
        (None,
            { 'fields': (
                "rule",
                "order",
                )
            }
        ),
    )

class TreeAdmin(admin.ModelAdmin):
	actions = [grow,draw,]
	inlines = (TreeRuleInline,)
	model = Tree

admin.site.register(Axiom)
admin.site.register(Tree, TreeAdmin)
admin.site.register(Rule)
admin.site.register(Branch)
