import re
import random

from django.db import models

from .managers import TreeManager

ALPHABET = (
	('f', 'f'),
	('F', 'F'),
)

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
	left_of_start = models.CharField(max_length=1, blank=True, choices=ALPHABET)
	right_of_start = models.CharField(max_length=1, blank=True, choices=ALPHABET)

	"""
	Extends the Rule model by adding a probability of
	occurence that the start will be replaced.
	"""
	probability = models.PositiveIntegerField(blank=True, null=True)

	def __unicode__(self):
		left = self.left_of_start + ':' if self.left_of_start else ''
		right = ':' + self.right_of_start if self.right_of_start else ''
		front = '{0}% '.format(self.probability) if self.probability else ''
		return unicode(front + left + self.start + right + ' -> ' + self.result)

	def __find_all(self, string):
		start = self.left_of_start + self.start + self.right_of_start
		return [m.start() + 1 if self.left_of_start else m.start() for m in re.finditer(start, string)]

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
	root = models.ForeignKey('Axiom')
	generation = models.PositiveIntegerField(default=0)
	form = models.TextField(blank=True)
	tree_rules = models.ManyToManyField('Rule', through='TreeRule')

	objects = TreeManager()

	def __unicode__(self):
		return unicode(self.form) if self.form else unicode(self.root)

	def grow(self):
		if self.generation is 0:
			self.form = self.root.seed
		for tr in self.rules.all().select_related():
			self.form = tr.rule.do_replace(str(self.form))
		self.generation = self.generation + 1
		self.save()
		return self.form


class TreeRule(models.Model):

	tree = models.ForeignKey('Tree', related_name='rules')
	rule = models.ForeignKey('Rule')

	# order of application of rules
	order = models.PositiveIntegerField()

	def __unicode__(self):
		return unicode(self.rule)

	class Meta:
		ordering = ['order',]