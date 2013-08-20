from django.db import models

class TreeQuerySet(models.query.QuerySet):
	pass

class TreeManager(models.Manager):

	def get_query_set(self):
		return TreeQuerySet(self.model, using=self._db)
