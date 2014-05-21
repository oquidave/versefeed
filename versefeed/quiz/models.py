from django.db import models
#from django.contrib.auth.models import User

# Create your models here.
#Questions model
class Qns(models.Model):
	""" Model that holds all the quiz questions"""
	qn = models.TextField()
	ref = models.TextField(null=True)
	 
	class Meta:
	 	verbose_name_plural="qns"
	def __unicode__(self):
	 	return self.qn
#objectives
class Choices(models.Model):
	"""Model holds objectives of each question"""
	qn = models.ForeignKey(Qns)
	choice = models.CharField(max_length=255)
	is_ans = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural="choices"
	def __unicode__(self):
		return self.choice
#themes
class Themes(models.Model):
	"""Model for quiz themes or categories. Each qn should belong to a theme"""
	theme = models.TextField()
	description = models.TextField(null=True)
	author = models.CharField(max_length=255, null=True)

	class Meta:
		verbose_name_plural="themes"
	def __unicode__(self):
		return self.theme


#themes-questions map
class QnsThemes(models.Model):
	"""Models many-to-many relationship between theme and Questions"""
	qn = models.ForeignKey(Qns)
	theme = models.ForeignKey(Themes)

	class Meta:
		verbose_name_plural="qns_themes"
	def __unicode__(self):
		return '%s' % self.theme

#tags
class Tags(models.Model):
	"""Model for quiz question tags. Each qn should belong to a one or two tags"""
	tag = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural="tags"
	def __unicode__(self):
		return self.tag


#tags-questions map
class QnsTags(models.Model):
	"""Models many-to-many relationship between tags and Questions"""
	qn = models.ForeignKey(Qns)
	tag = models.ForeignKey(Tags)

	class Meta:
		verbose_name_plural="qns_tags"
	def __unicode__(self):
		return '%s' % self.tag
#persist users' sessions
class UserSession(models.Model):
	"""persist user's session so that next time they login, they start from where they left off"""
	user_id = models.IntegerField(null=True)
	theme_id = models.IntegerField(null=True)
	quiz_round = models.IntegerField(null=True)
	no_rounds  = models.IntegerField(null=True)
	round_pg = models.IntegerField(null=True)
	round_pts = models.IntegerField(null=True)
	quiz_pts = models.IntegerField(null=True)


	class Meta:
		verbose_name_plural="user_session"
	def __unicode__(self):
		return '%s' % self.theme_id

