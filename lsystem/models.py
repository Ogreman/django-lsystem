import re
import math
import pygame
import random
from datetime import datetime

from django.db import models
from django.db import transaction

from .managers import TreeManager

ALPHABET = (
	('X', 'X'), # no movement
	('Y', 'Y'),
	('F', 'F'), # move forward
	('[', '['), # save current state
	(']', ']'), # load state
	('+', '+'), # rotate clockwise
	('-', '-'), # rotate anticlockwise
)
TORADS = 0.01745
GREEN = "80,200,80"
BROWN = "150,120,120"


class TreeError(Exception):
	pass


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
	thickness = models.PositiveIntegerField()
	angle = models.FloatField()

	colour = models.CharField(max_length=12, default=GREEN)

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

	def init(self):
		self._children = []
		self._children = list(self.children.all())
		return self

	def draw(self, screen, position, colour=None):
		colour = [int(i) for i in self.colour.split(',')]
		pygame.draw.line(
			screen, colour,
			(self.startX + position[0], self.startY + position[1]),
			(self.endX + position[0], self.endY + position[1]),
			self.thickness
		)

	def rotate(self, angle):
		self.angle += angle
		rads = self.angle * TORADS
		self.endX = self.startX + math.cos(rads) * self.length
		self.endY = self.startY	+ math.sin(rads) * -1.0 * self.length
		if hasattr(self, '_children'):
			for child in self._children:
				child.startX = self.endX
				child.startY = self.endY
				child.rotate(angle)



class TimeStampedModel(models.Model):
    """
	An abstract base class model that provides self-
	updating ''created'' and ''modified'' fields.
	"""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rule(models.Model):
	"""
	A rule defines the replacements that may
	occur within an L-System.

	Handles all the string replacement functionality.

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

	"""
	Extension adding context sensitive fields
	"""
	left_of_start = models.CharField(
		max_length=1, blank=True, choices=ALPHABET
	)
	right_of_start = models.CharField(
		max_length=1, blank=True, choices=ALPHABET
	)
	# ignore = models.CharField(
	#	max_length=10, blank=True
	#)

	"""
	Extends the Rule model by adding a probability of
	occurence that the start will be replaced.
	"""
	probability_start = models.PositiveIntegerField(
		default=0
	)
	probability_end = models.PositiveIntegerField(
		default=100
	)


	def __unicode__(self):
		left = self.left_of_start + ':' if self.left_of_start else ''
		right = ':' + self.right_of_start if self.right_of_start else ''
		front = '{0}% '.format(
			self.probability_end - self.probability_start
		) if self.probability_end else ''
		return unicode (
			front + left + self.start + right + ' -> ' + self.result
		)

	def __find_all(self, string, thing):
		"""
		Generator function that returns a list
		of string positions of occurences
		of substring start.

		TODO: match #ignore
		example: (X...X...X)
		"""
		for match in re.finditer(thing, string):
			if self.left_of_start:
				yield match.start() + 1
			else:
				yield match.start()

	def do_replace_all(self, string, rand):
		"""
		Primary rewriting function.

		Takes the current form of the string and 
		iterates over finding all occurences of 
		the required start element and  replaces with 
		the production result.

		Handles stochastic implementation with random 
		number generation (sequentially).
		"""
		
		start = self.left_of_start + self.start + self.right_of_start		
		if self.probability_end:			
			if (self.probability_start <= rand <= self.probability_end):
				slist = list(string)			
				for i in self.__find_all(string, start):
					slist[i] = self.result
				return ''.join(slist)
			return string
		return string.replace(start, self.result)



class Axiom(TimeStampedModel):
	"""
	An axiom defines the seed or starting point
	of an L-System, from which a tree is grown.

	An axiom is defined as a single character.
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
	branches = models.TextField(blank=True)

	objects = TreeManager()


	def __unicode__(self):
		if self.label:
			return unicode(self.label)
		return unicode(self.id)

	def _rules(self):
		for rule in self.rules.all().select_related():
			yield rule.rule

	def init(self):
		"""
		Loads branches from database into memory.
		This readies the tree for simulation.
		"""
		if self.branches == '':
			raise TreeError, "Tree {0} has no branches".format(self.label)

		# loads branch data from db
		tstart = datetime.now()
		branch_ids = self.branches.split(',')
		self._branches = [
			branch.init()
			for branch in Branch.objects.filter(id__in=branch_ids)
		]
		time = datetime.now() - tstart

		print "Tree {0} initialised with {1} branches in {2} seconds.".format(
			str(self), len(self._branches),
			time.total_seconds()
		)
		return self

	def grow_sequential(self):
		"""
		Growth function that checks each character
		sequentially. For comparison purposes.
		"""
		old_form = self.form

		if self.generation is 0:
			self.form = self.start.seed
		
		# sequential character rewriting algorithm
		tstart = datetime.now()
		form = list(self.form)
		rules = { r.start: r for r in self.tree_rules.all() }
		for i, char in enumerate(form):
			try:
				rule = rules[char]
				rand = random.random() * 100
				if rule.probability_start <= rand <= rule.probability_end:
					form[i] = rule.result
			except KeyError:
				pass
		self.form = ''.join(form)
		time = datetime.now() - tstart

		# DEBUG / grow time
		print "Sequential Grow took {0} seconds" .format(
			time.total_seconds()
		)

		if self.form == old_form:
			raise TreeError, "Tree {0} did not grow.".format(self.label)

		self.generation = self.generation + 1
		self.save()
		return self.form


	def grow(self):
		old_form = self.form

		if self.generation is 0:
			self.form = self.start.seed
		rand = random.random() * 100
		
		# pass initial form to each rule to handle replacing
		tstart = datetime.now()
		for rule in self._rules():
			self.form = rule.do_replace_all(str(self.form), rand)
		time = datetime.now() - tstart

		# DEBUG / grow time
		print "Grow took {0} seconds" .format(
			time.total_seconds()
		)

		if self.form == old_form:
			raise TreeError, "Tree {0} did not grow.".format(self.label)

		self.generation = self.generation + 1
		self.save()
		return self.form

	@transaction.commit_on_success
	def build(self):
		# delete all previously generated branches
		if self.root:
			self.root.delete()

		tstart = datetime.now()

		# create and delegate build to a helper class
		builder = TreeBuilder(self.form, self.theta, self.move)

		# stores branches as a comma-separated string of ids
		data = builder.build()
		self.root = data['root']
		self.branches = ','.join([str(b.id) for b in data['branches']])
		self.save()

		time = datetime.now() - tstart

		# DEBUG / grow time
		print "Build took {0} seconds" .format(
			time.total_seconds()
		)

		return 1

	def draw(self, screen, position):

		if not hasattr(self, '_branches'):
			raise TreeError, "Requires initialisation - self.init()"

		# each branch draws itself given a surface
		tstart = datetime.now()
		for branch in self._branches:
			branch.draw(screen, position)
		time = datetime.now() - tstart

		# DEBUG / render time
		print "Draw took {0} seconds" .format(
			time.total_seconds()
		)

	def reset(self):
		if self.root:
			branch_ids = self.branches.split(',')
			print "Deleting {0} branches".format(len(branch_ids))
			Branch.objects.filter(id__in=branch_ids).delete()
		self.root = None
		self.branches = ''
		self.form = ''
		self.generation = 0
		self.save()

	def rotate(self, angle):
		self.root.rotate(angle)
		return self



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

	def __init__(self, string, angle, length, start=(0.0, 0.0)):
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
		self.thickness = 1 		# starting thickness

	def build(self):
		print "Building from {0} characters.".format(len(self.string))
		for c in self.string:
			self.__action(c)
		print "Created {0} branches.".format(len(self.lines))
		return {
			'root': self.root,
			'branches': self.lines,
		}

	def __action(self, char):
		"""
		python hack to associate character
		to turtle command.
		Raises KeyError on not found.
		Acts like a switch statement.
		"""
		return {
			'X': self.__nothing,
			'Y': self.__nothing,
			'F': self.__move,
			'[': self.__push,
			']': self.__pop,
			'+': self.__aturn,
			'-': self.__cturn,
		}[char]()

	def __nothing(self):
		return 0

	def __cturn(self):
		return self.__turn(-1.0 * self.theta)

	def __aturn(self):
		return self.__turn(self.theta)

	def __move(self):
		"""
		NB: |-> 0 degrees; ^ 90 degrees, etc.
		"""
		componentX = math.cos(self.angle * TORADS) * self.distance
		componentY = math.sin(self.angle * TORADS) * -1.0 * self.distance
		newX = componentX + self.x
		newY = componentY + self.y
		branch = Branch(
			startX=self.x, startY=self.y,
			endX=newX, endY=newY,
			length=self.distance, angle=self.angle,
			colour=(BROWN if self.angle == 90.0 else GREEN),
			thickness=self.thickness
		)
		branch.save()
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
		self.stack.append((
			self.current,
			self.angle,
			self.thickness
		))
		return 1

	def __pop(self):
		data = self.stack.pop()
		self.current = data[0]
		self.x = self.current.endX
		self.y = self.current.endY
		self.angle = data[1]
		self.thickness =data[2]
		return 1

	def __turn(self, theta):
		self.thickness -= 2
		if self.thickness < 0:
			self.thickness = 1
		self.angle += theta
		return 1
