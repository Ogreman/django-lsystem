import re
import math
import pygame
import random

from django.db import models

from .managers import TreeManager

ALPHABET = (
	('X', 'X'), # no movement
	('F', 'F'), # move forward
	('[', '['), # save current state
	(']', ']'), # load state
	('+', '+'), # rotate clockwise
	('-', '-'), # rotate anticlockwise
)
TORADS = 0.01745

class Branch(models.Model):
	"""
	A description of a segment of a tree in
	terms of a line and its corresponding
	child branches.
	"""
	startX = models.FloatField()
	startY = models.FloatField()

	endX = models.FloatField()
	endY = models.FloatField()

	length = models.PositiveIntegerField()
	angle = models.FloatField()

	colour = models.CharField(max_length=12, default="255,255,255")

	children = models.ManyToManyField(
		"self", symmetrical=False, related_name="parent"
	)

	class Meta:
		verbose_name_plural = "branches"

	def __unicode__(self):
		return unicode(
			"({0}, {1}), ({2}, {3})".format(
				self.startX, self.startY,
				self.endX, self.endY
			)
		)

	def delete(self, *args, **kwargs):
		for child in self.children.all():
			child.delete()
		super(Branch, self).delete(*args, **kwargs)

	def draw(self, screen):
		colour = [int(i) for i in self.colour.split(',')]
		pygame.draw.aaline(
			screen, colour,
			(self.startX, self.startY),
			(self.endX, self.endY)
		)
		for child in self.children.all():
			child.draw(screen)


class TimeStampedModel(models.Model):
    """
	An abstract base class model that provides self-
	updating ''created'' and ''modified'' fields.
	"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rule(TimeStampedModel):
	"""
	A rule defines the replacements that may
	occur within an L-System.

	Rules generally take the form:
	    a -> b
	Where a, b are characters in a string
	belonging to the alphabet in the system.

	Rules may be context-sensitive or context-free.

	Context-sensitive rules take the form:
		(x) a (y) -> b
	Where a, b, x, y are characters in a string
	belonging to the alphabet in the system and where
	a is in context of x and/or y.
	"""

	start = models.CharField(max_length=1, choices=ALPHABET)
	result = models.CharField(max_length=255)

	# Context sensitive fields
	left_of_start = models.CharField(
		max_length=1, blank=True, choices=ALPHABET
	)
	right_of_start = models.CharField(
		max_length=1, blank=True, choices=ALPHABET
	)

	"""
	Extends the Rule model by adding a probability of
	occurence that the start will be replaced.
	"""
	probability = models.PositiveIntegerField(blank=True, null=True)

	def __unicode__(self):
		left = self.left_of_start + ':' if self.left_of_start else ''
		right = ':' + self.right_of_start if self.right_of_start else ''
		front = '{0}% '.format(self.probability) if self.probability else ''
		return unicode (
			front + left + self.start + right + ' -> ' + self.result
		)

	def __find_all(self, string):
		start = self.left_of_start + self.start + self.right_of_start
		return [ m.start() + 1 if self.left_of_start else m.start()
		 	for m in re.finditer(start, string) ]

	def do_replace(self, string):
		slist = list(string)
		for i in self.__find_all(string):
			if self.probability:
				if (random.random() * 100) <= self.probability:
					slist[i] = self.result
			else:
			 	slist[i] = self.result
		return ''.join(slist)



class Axiom(TimeStampedModel):
	"""
	An axiom defines the seed or starting point
	of an L-System, from which a tree is grown.

	An axiom is defined as a single character.

	Each axiom has a unique id field.
	"""
	seed = models.CharField(max_length=1, choices=ALPHABET)

	def __unicode__(self):
		return unicode(str(self.id) + ' - ' + self.seed)


class Tree(TimeStampedModel):
	"""
	A tree defines a string of characters
	that are a product of the effects of
	multiple rules being applied and iterated
	over an initial axiom, modelling the effects
	forces have over form.

	A tree is defined by its axiom and the
	generation from the axiom as well as its
	resulting string.
	"""
	label = models.CharField(blank=True, max_length=255)
	start = models.ForeignKey('Axiom')
	root = models.ForeignKey(
		'Branch', blank=True, null=True, on_delete=models.SET_NULL
	)
	generation = models.PositiveIntegerField(default=0)
	form = models.TextField(blank=True)
	tree_rules = models.ManyToManyField('Rule', through='TreeRule')
	theta = models.FloatField()
	move = models.FloatField()

	objects = TreeManager()


	def __unicode__(self):
		if self.label:
			return unicode(self.label)
		return unicode(self.id)

	def grow(self):
		if self.generation is 0:
			self.form = self.start.seed
		for tr in self.rules.all().select_related():
			self.form = tr.rule.do_replace(str(self.form))
		self.generation = self.generation + 1
		self.save()
		return self.form

	def build(self, start):
		angle = -1.0 * self.theta
		if self.root:
			self.root.delete()
		builder = TreeBuilder(self.form, angle, self.move, start)
		self.root = builder.build()
		self.save()

	def draw(self, screen):
		self.root.draw(screen)


class TreeRule(models.Model):
	"""
	Through table for trees >-< rules relationship.
	"""

	tree = models.ForeignKey('Tree', related_name='rules')
	rule = models.ForeignKey('Rule')

	# order of application of rules
	order = models.PositiveIntegerField()

	def __unicode__(self):
		return unicode(self.rule)

	class Meta:
		ordering = ['order',]



class TreeBuilder(object):
	"""
	Python class for building branches from L-System
	string, angle, distance and start position.

	Used to create all branches in tree and return root.
	"""

	def __init__(self, string, angle, length, start):
		self.string = string    # string to convert
		self.stack = [] 		# push / pop (b, angle)
		self.current = None 	# current branch
		self.angle = 90.0		# vector angle
		self.x = start[0] 		# current x pos
		self.y = start[1]		# current y pos
		self.startX = self.x 	# starting x pos
		self.startY = self.y 	# starting y pos
		self.theta = angle 		# global angle
		self.root = None		# root branch of tree
		self.lines = []			# collection of branches
		self.distance = length 	# global length of branches

	def build(self):
		for i, c in enumerate(self.string):
			self.__action(c)
		return self.root

	def __action(self, char):
		return {
			'X': self.__nothing,
			'F': self.__move,
			'[': self.__push,
			']': self.__pop,
			'+': self.__cturn,
			'-': self.__aturn,
		}[char]()

	def __nothing(self):
		return 0

	def __cturn(self):
		return self.__turn(self.theta)

	def __aturn(self):
		return self.__turn(-1.0 * self.theta)

	def __move(self):
		print "Moving..."
		componentX = math.cos(self.angle * TORADS) * self.distance
		componentY = math.sin(self.angle * TORADS) * -1.0 * self.distance
		newX = componentX + self.x
		newY = componentY + self.y
		branch = Branch(
			startX=self.x, startY=self.y,
			endX=newX, endY=newY,
			length=self.distance, angle=self.angle
		)
		branch.save()
		print "{0}".format(branch)
		self.lines.append(branch)
		if self.root == None:
			self.root = branch
		else:
			self.current.children.add(branch)
		self.current = branch
		self.x = newX
		self.y = newY
		return 1

	def __push(self):
		print "Pushing..."
		self.stack.append((
			self.current,
			self.angle
		))
		return 1

	def __pop(self):
		print "Popping..."
		data = self.stack.pop()
		self.current = data[0]
		self.x = self.current.endX
		self.y = self.current.endY
		self.angle = data[1]
		return 1

	def __turn(self, theta):
		print "Turning by {0}...".format(theta)
		self.angle += theta
		print "Angle now: {0}".format(self.angle)
		return 1
