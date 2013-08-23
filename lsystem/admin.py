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

    TODO: build in world space around (0,0)
    """
    for tree in queryset:
        tree.build()
    rows_updated = queryset.count()
    if rows_updated == 1:
        count_bit = "1 tree was"
    else:
        count_bit = "%s trees were" % rows_updated
    modeladmin.message_user(request, "%s successfully built." % count_bit)


def draw(modeladmin, request, queryset):
    """
    Displays a tree using pygame

    TODO: transpose from model to view space.
    """
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    modeladmin.message_user(request, "Successfully drew trees to screen.")

    actors = [tree.init() for tree in queryset]
    num_actors = len(actors)
    tree_spacing = (WIDTH / (num_actors + 1))
    tree_base = 635.0

    while True:
        elapsed = clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return;
        screen.fill(BLUE)
        pygame.draw.line(screen, [0, 100, 0], [0, 630], [800, 630], 20)
        for i, tree in enumerate(actors):
            position = (tree_spacing * (i + 1), tree_base)
            tree.draw(screen, position)
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
    readonly_fields = (
        "created",
        "modified",
        "root",
        "generation",
        "form",
        "branch_count"
    )

    def branch_count(self, obj):
        return len(obj.branches)
    branch_count.short_description = "Branches"
    branch_count.allow_tags = True

    fieldsets = (
        (None,
            { 'fields': (
                "label",
                "start",
                "generation",
                )
            }
        ),
        ("Details",
            { 'fields': (
                "move",
                "theta",
                "created",
                "modified",
                )
            }
        ),
        ("Form",
            { 'fields': (
                "form",
                "branch_count",
                )
            }
        ),
    )

admin.site.register(Axiom)
admin.site.register(Tree, TreeAdmin)
admin.site.register(Rule)
admin.site.register(Branch)
