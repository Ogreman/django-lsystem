import pygame
import sys

from django.contrib import admin
from .models import Axiom, Tree, Rule, TreeRule, Branch

WIDTH = 800
HEIGHT = 640
BLACK = (0,0,0)
BLUE = (10, 80, 150)

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


def reset_tree(modeladmin, request, queryset):
    """
    Resets a tree
    """
    for tree in queryset:
        tree.reset()
    rows_updated = queryset.count()
    if rows_updated == 1:
        count_bit = "1 tree was"
    else:
        count_bit = "%s trees were" % rows_updated
    modeladmin.message_user(request, "%s successfully reset." % count_bit)



def build(modeladmin, request, queryset):
    """
    Builds a tree
    """
    for i, tree in enumerate(queryset):
        w = (WIDTH / (queryset.count() + 1)) * (i + 1)
        tree.build((w, 640.0))
    rows_updated = queryset.count()
    if rows_updated == 1:
        count_bit = "1 tree was"
    else:
        count_bit = "%s trees were" % rows_updated
    modeladmin.message_user(request, "%s successfully built." % count_bit)


def draw(modeladmin, request, queryset):
    """
    Displays a tree using pygame
    """
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    modeladmin.message_user(request, "Successfully drew trees to screen.")
    actors = []
    for tree in queryset:
        actors.append(tree.init())
    while True:
        elapsed = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return;
        screen.fill(BLUE)
        for tree in actors:
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
	actions = [grow,draw,build,reset_tree,]
	inlines = (TreeRuleInline,)
	model = Tree

admin.site.register(Axiom)
admin.site.register(Tree, TreeAdmin)
admin.site.register(Rule)
admin.site.register(Branch)
