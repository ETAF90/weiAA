#encoding: utf-8
from django.db import models
from django.contrib import admin
# Create your models here.

class WeiaaUser(models.Model):
	uid = models.AutoField(primary_key=True)
	passwd = models.CharField(max_length=30,blank=False)
	name = models.CharField(max_length=45,blank=False)
	email = models.EmailField()
	phone_num = models.CharField(max_length=20,blank=True)
	permission = models.IntegerField(blank=False,default=0)
	weibo_id = models.CharField(max_length=45,blank=True)
	access_token = models.CharField(max_length=40,blank=True)
	expire_in = models.IntegerField(blank=True,default=0)
	def __unicode__(self):
		return self.name

class WeiaaActivity(models.Model):
	aid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30,blank=False)
	date = models.DateTimeField()
	state = models.IntegerField(blank=False,default=0)
	#state, 0：待确认；1：已确认；2：收费中；3：已结束
	creator_id = models.ForeignKey(WeiaaUser)
	def __unicode__(self):
		return self.name

class WeiaaActivityPlan(models.Model):
	apid = models.AutoField(primary_key=True)
	aid = models.ForeignKey(WeiaaActivity)
	is_selected = models.BooleanField(blank = False,default = False)
	vote = models.IntegerField(blank=False,default=0)
	estimate_per_cost = models.FloatField(blank=False,default=0)
	real_cost = models.FloatField(blank=False,default=0)
	creator_id = models.ForeignKey(WeiaaUser)
	def __unicode__(self):
		return 'activity plan %s for %s' % (self.apid, self.aid)

class WeiaaActivityPlanItem(models.Model):
	apiid = models.AutoField(primary_key=True)
	apid = models.ForeignKey(WeiaaActivityPlan)
	start_time = models.DateTimeField()
	place = models.CharField(max_length=45,blank=False)
	content = models.CharField(max_length=45,blank=False)
	estimate_per_cost = models.FloatField(blank=False,default=0)
	real_cost = models.FloatField(blank=False,default=0)
	def __unicode__(self):
		return 'plan item %d belongs to activity plan %s' % (self.apiid, self.apid)

class WeiaaActivityMember(models.Model):
	aid = models.ForeignKey(WeiaaActivity)
	uid = models.ForeignKey(WeiaaUser)
	confirm_state = models.IntegerField(default=0)# 0:waiting; 1:yes; 2:no;
	real_per_cost = models.FloatField(blank = False, default = 0)
	is_paid = models.BooleanField()
	def __unicode__(self):
		return 'user %s in activity %s share:%f' % (self.uid, self.aid, self.real_per_cost)

class WeiaaActivityPlanVote(models.Model):
	apid = models.ForeignKey(WeiaaActivityPlan)
	uid = models.ForeignKey(WeiaaUser)
	def __unicode__(self):
		return 'user %s vote activity plan %s' % (self.uid, self.apid)

admin.site.register(WeiaaUser)
admin.site.register(WeiaaActivity)
admin.site.register(WeiaaActivityPlan)
admin.site.register(WeiaaActivityPlanItem)
admin.site.register(WeiaaActivityMember)
admin.site.register(WeiaaActivityPlanVote)