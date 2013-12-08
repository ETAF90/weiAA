#encoding: utf-8
# Create your views here.
import math
import time
from django.http import HttpResponse
#from django.template import Context, loader
from django.shortcuts import render,redirect
import weiboTools
from weiaa_app import dao

from weiaa_app.models import *
WONIU_DEBUG = False
def get_access_token(request):

	return weiboTools.signin()

def index(request):
#	template = loader.get_template('weiAA_app/index.html');
#	context = Context()
#	return HttpResponse(template.render(context));

	if request.session.has_key('weibo_id'):
		if WONIU_DEBUG:
			print "!!!direct "
		weibo_id = request.session['weibo_id']
		if WONIU_DEBUG:
			print "views.index: weibo_id %s" % weibo_id
		current_user = WeiaaUser.objects.get(weibo_id = weibo_id)
		
		#activity_list = WeiaaActivity.objects.all()
		#unchecked_activity_list = activity_list.filter(state = 0,creator_id__weibo_id = weibo_id)
		
		unchecked_activity_list = WeiaaActivityMember.objects.filter(aid__state = 0,uid__weibo_id=weibo_id,aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		checked_activity_list = WeiaaActivityMember.objects.filter(aid__state = 1,uid__weibo_id=weibo_id,aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		feeing_activity_list = WeiaaActivityMember.objects.filter(aid__state = 2,uid__weibo_id=weibo_id,aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		finished_activity_list = WeiaaActivityMember.objects.filter(aid__state = 3,uid__weibo_id=weibo_id,aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		#act_confirm_list
		# act_confirm_list = {}
		# for a in unchecked_activity_list:
			# act_confirm_list[a] = True
			# member_list = WeiaaActivityMember.objects.filter(aid = a).exclude(confirm_state = 0)
			# if member_list.count()>0:
				# act_confirm_list[a] = False
		#invited activity
		#参与或者创建的活动
		# member_list = WeiaaActivityMember.objects.filter(uid = WeiaaUser.objects.get(weibo_id = weibo_id)).exclude(aid__creator_id = WeiaaUser.objects.get(weibo_id = weibo_id))
		# unchecked_activity_list2 = []
		# checked_activity_list2 = []
		# feeing_activity_list2 = []
		# finished_activity_list2 = []
		# for m in member_list:
			# a = m.aid;
			# if a.state == 0:
				# unchecked_activity_list2.extend(a)
			# if a.state == 1:
				# checked_activity_list2.extend(a)
			# if a.state == 2:
				# feeing_activity_list2.extend(a)
			# if a.state == 3:
				# finished_activity_list2.extend(a)weiaaactivitymember
		# unchecked_activity_list2 = WeiaaActivity.objects.filter(state = 0).exclude(creator_id__weibo_id = weibo_id).filter(weiaaactivitymember__uid__weibo_id = weibo_id)
		# checked_activity_list2 = WeiaaActivity.objects.filter(state = 1).exclude(creator_id__weibo_id = weibo_id).filter(weiaaactivitymember__uid__weibo_id = weibo_id)
		# feeing_activity_list2 = WeiaaActivity.objects.filter(state = 2).exclude(creator_id__weibo_id = weibo_id).filter(weiaaactivitymember__uid__weibo_id = weibo_id)
		# finished_activity_list2 = WeiaaActivity.objects.filter(state = 3).exclude(creator_id__weibo_id = weibo_id).filter(weiaaactivitymember__uid__weibo_id = weibo_id)
		
		unchecked_activity_list2 = WeiaaActivityMember.objects.filter(aid__state = 0, uid__weibo_id = weibo_id).exclude(aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		checked_activity_list2 = WeiaaActivityMember.objects.filter(aid__state = 1, uid__weibo_id = weibo_id).exclude(aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		feeing_activity_list2 = WeiaaActivityMember.objects.filter(aid__state = 2, uid__weibo_id = weibo_id).exclude(aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		finished_activity_list2 = WeiaaActivityMember.objects.filter(aid__state = 3, uid__weibo_id = weibo_id).exclude(aid__creator_id__weibo_id = weibo_id).order_by('aid__date')
		#confirm_state_list
		confirm_state_list = {}
		# for a in unchecked_activity_list2:
			# confirm_state_list[a.aid] = True
			# confirm_state = WeiaaActivityMember.objects.get(uid__weibo_id = weibo_id,aid = a).confirm_state
			# if confirm_state > 0:
				# confirm_state_list[a.aid] = False
			# print 'confirm_state: %s' % confirm_state_list[a.aid]
		#待确认活动 uid__weibo_id = weibo_id：该登录者参加的活动；comfirm_state = 0：待确认
		unconfirm_activity_count = WeiaaActivityMember.objects.filter(uid__weibo_id = weibo_id,confirm_state = 0).count()
		if WONIU_DEBUG:
			print "unconfirm_activity_count:%d" % unconfirm_activity_count
		#待缴费活动  uid.weibo_id=weibo_id：该登录者参加的活动；state=2:活动收费中；is_paid = False：未交费
		topay_activity_count = WeiaaActivityMember.objects.filter(uid__weibo_id = weibo_id, aid__state = 2, is_paid = False).count()
		if WONIU_DEBUG:
			print "topay_activity_count:%d" % topay_activity_count
		#收费中活动
		feeing_activity_count = feeing_activity_list.count()
		if WONIU_DEBUG:
			print "feeing_activity_count: %d" % feeing_activity_count
		
		#p = WeiaaActivityPlan.objects.filter(aid__name__exact='activity01')[1]
		#p = unchecked_activity_list[0].weiaaactivityplan_set.all()[0];
		profile_img = weiboTools.get_profile_img(request);
		if WONIU_DEBUG:
			print "fffffuck %s" % profile_img; 
		activity_lists = {}
		activity_lists['unchecked_activity_list'] = unchecked_activity_list
		activity_lists['checked_activity_list'] = checked_activity_list
		activity_lists['feeing_activity_list'] = feeing_activity_list
		activity_lists['finished_activity_list'] = finished_activity_list
		#invited activity
		activity_lists['unchecked_activity_list2'] = unchecked_activity_list2
		activity_lists['checked_activity_list2'] = checked_activity_list2
		activity_lists['feeing_activity_list2'] = feeing_activity_list2
		activity_lists['finished_activity_list2'] = finished_activity_list2
		#'name':value
		return render(request,'weiAA_app/index.html',{'activity_lists':activity_lists,'unconfirm_activity_count':unconfirm_activity_count,'topay_activity_count':topay_activity_count,'feeing_activity_count':feeing_activity_count,'current_user':current_user,
		'profile_img':profile_img})
	else:
		return render(request,'weiAA_app/weiboLogin.html')



def test(request):
	
	return render(request,'weiAA_app/test.html',
		{'message_title':'投票成功','message_content':'投票结果'})
	
def weiboLogin(request):

	#return weiboTools.signin()
	return render(request,'weiAA_app/weiboLogin.html')



def callback(request):

	if weiboTools.callback(request)==True:
		return redirect('/')
	else:
		return render(request,'weiAA_app/weiboLogin.html')

def create_act(request):

	if request.session.has_key('weibo_id'):
		user = WeiaaUser.objects.get(weibo_id = request.session['weibo_id'])
		screen_name = user.name
		create_time = time.localtime(time.time())
		create_time = "%04d-%02d-%02d %02d:%02d" % (create_time.tm_year,create_time.tm_mon, create_time.tm_mday, create_time.tm_hour,create_time.tm_min)
		if WONIU_DEBUG:
			print 'views.create_act, create time:' % create_time
		
		return render (request,'weiAA_app/create_act.html',{'screen_name': screen_name,'create_time':create_time})
	else:
		return render(request,'weiAA_app/weiboLogin.html')

	# print "!!! here"
	# return redirect(request,'weiAA_app/test.html',
	# 	{'message_title':'投票成功','message_content':'投票结果'})
def create_act_form(request):
	if request.session.has_key('weibo_id'):

		weibo_id = request.session['weibo_id']
		current_user = WeiaaUser.objects.get(weibo_id = weibo_id)
		if WONIU_DEBUG:
			print 'create_act_form, weibo_id: %s' % weibo_id
		
		#create new activity: name, date, creator_id
		act_name = 'activity%02d' % (WeiaaActivity.objects.all().count()+1)
		date = request.POST['create_time']
		if WONIU_DEBUG:
			print 'create time: %s' % date
		new_act = WeiaaActivity(name=act_name,date=date, creator_id=WeiaaUser.objects.get(weibo_id=weibo_id))
		new_act.save();
		
		#create new activity plan: aid, creator_id, estimate_per_cost
		new_plan = WeiaaActivityPlan(aid = new_act, creator_id = WeiaaUser.objects.get(weibo_id = weibo_id))
		#new_plan.save();
		#plan item table begin
		#item_time
		#item_address
		#item_content
		#item_estimate_per_cost
		#plan item table end
		flag = True
		for i in range(1,50):
			key = 'item_time_%d' % i
			if request.POST.has_key(key):
				item_time = request.POST['item_time_%d' % i]
				item_address = request.POST['item_address_%d' % i]
				item_content = request.POST['item_content_%d' % i]
				item_estimate_per_cost = request.POST['item_estimate_per_cost_%d' % i]
				#set plan.esitmate_per_cost
				new_plan.estimate_per_cost += float(item_estimate_per_cost)
				new_plan.save();
				#create plan item: start_time, place, content, estimate_per_cost 
				item = WeiaaActivityPlanItem(apid = new_plan, start_time = item_time,place = item_address, content = item_content, estimate_per_cost = item_estimate_per_cost)
				item.save();
				if WONIU_DEBUG:
					#plan item info
					print 'plan item info'
					print 'apiid:%s' % item.apiid
					print 'apid:%s' % item.apid
					print 'start_time:%s' % item.start_time
					print 'place:%s' % item.place
					print 'content:%s' % item.content
					print 'estimate_per_cost %s' % item.estimate_per_cost
		
		if WONIU_DEBUG:
			#activity plan info
			print 'activity plan info'
			print 'apid:%s' % new_plan.apid
			print 'aid:%s' % new_plan.aid
			print 'is_selected:%s' % new_plan.is_selected
			print 'vote:%s' % new_plan.vote
			print 'estimate_per_cost:%s' % new_plan.estimate_per_cost
			print 'real_cost:%s' % new_plan.real_cost
			print 'creator_id:%s' % new_plan.creator_id
			#activity info
			print 'activity info'
			print 'id:%s' % new_act.aid
			print 'name:%s' % new_act.name
			print 'date:%s' % new_act.date
			print 'state:%s' % new_act.state
			print 'creator_id:%s' % new_act.creator_id;
		if WONIU_DEBUG:
			for key in request.POST:
				print 'POST: key=%s,value=%s' % (key,request.POST[key])
		#add current user to the WeiaaActivityMember table
		member = WeiaaActivityMember(aid = new_act,uid = current_user,confirm_state = 1)
		member.save()
		#add the other members
		for i in range(1,100):

			key = 'member_%d' % i			
			if request.POST.has_key(key):
				screen_name = request.POST[key]
				weibo_id = weiboTools.find_weibo_id(request, screen_name)
				if WONIU_DEBUG:
					print 'screen_name:%s' % screen_name
					print 'weibo_id:%s' % weibo_id
				users = WeiaaUser.objects.filter(weibo_id = weibo_id)
				if users.count()==0:
					dao.insert_user(weibo_id,screen_name,'null',0)
					#user = WeiaaUser(name = screen_name, weibo_id = weibo_id,access_token='null',expire_in = 0 )
					#user.save()
				member = WeiaaActivityMember(aid = new_act,uid = WeiaaUser.objects.get(weibo_id = weibo_id))
				member.save()
		return render(request,'weiAA_app/result.html',{'message_title':'您已成功创建一个活动!'})
	else:
		return render(request,'weiAA_app/weiboLogin.html')
def create_act_plan(request):
	if request.session.has_key('weibo_id'):
		if request.GET.has_key('act_id'):
			act_id = request.GET['act_id']
			return render(request,'weiAA_app/create_act_plan.html',{'act_id':act_id})
		else:
			redirect('/')
	else:
		return render(request,'weiAA_app/weiboLogin.html')
def create_act_plan_form(request):
	if request.session.has_key('weibo_id'):

		weibo_id = request.session['weibo_id']
		if WONIU_DEBUG:
			for key in request.POST:
				print 'POST:key=%s,value=%s' % (key,request.POST[key])
			for key in request.GET:
				print 'GET:key=%s,value=%s' % (key,request.GET[key])
		
		if WONIU_DEBUG:
			print 'get creating activity form from %s' % weibo_id
		if not (request.POST.has_key('act_id')):
			if WONIU_DEBUG:
				print 'not act_id'
			return redirect('/')
		if WONIU_DEBUG:
			print 'act_id=%s' % request.POST['act_id']
		act = WeiaaActivity.objects.get(aid = int(request.POST['act_id']))
		#create new activity plan: aid, creator_id, estimate_per_cost
		new_plan = WeiaaActivityPlan(aid = act, creator_id = WeiaaUser.objects.get(weibo_id = weibo_id))
		#new_plan.save();
		#plan item table begin
		#item_time
		#item_address
		#item_content
		#item_estimate_per_cost
		#plan item table end
		flag = True
		for i in range(1,50):
			key = 'item_time_%d' % i
			if request.POST.has_key(key):
				item_time = request.POST['item_time_%d' % i]
				if flag:
					new_plan.save();
					flag = False
				item_address = request.POST['item_address_%d' % i]
				item_content = request.POST['item_content_%d' % i]
				item_estimate_per_cost = request.POST['item_estimate_per_cost_%d' % i]
				#set plan.esitmate_per_cost
				new_plan.estimate_per_cost += float(item_estimate_per_cost)
				new_plan.save();
				#create plan item: start_time, place, content, estimate_per_cost 
				item = WeiaaActivityPlanItem(apid = new_plan, start_time = item_time,place = item_address, content = item_content, estimate_per_cost = item_estimate_per_cost)
				item.save();
				if WONIU_DEBUG:
					#plan item info
					print 'plan item info'
					print 'apiid:%s' % item.apiid
					print 'apid:%s' % item.apid
					print 'start_time:%s' % item.start_time
					print 'place:%s' % item.place
					print 'content:%s' % item.content
					print 'estimate_per_cost %s' % item.estimate_per_cost
		
		if WONIU_DEBUG:
			#activity plan info
			print 'activity plan info'
			print 'apid:%s' % new_plan.apid
			print 'aid:%s' % new_plan.aid
			print 'is_selected:%s' % new_plan.is_selected
			print 'vote:%s' % new_plan.vote
			print 'estimate_per_cost:%s' % new_plan.estimate_per_cost
			print 'real_cost:%s' % new_plan.real_cost
			print 'creator_id:%s' % new_plan.creator_id
		if WONIU_DEBUG:
			for key in request.POST:
				print 'key=%s,value=%s' % (key,request.POST[key])
		return render(request,'weiAA_app/result.html',{'message_title':'您已成功为该活动创建了一个活动方案！'})
	else:
		return weiboTools.signin()
def confirm_act(request):

	if request.session.has_key('weibo_id'):
		if request.GET.has_key('act_id'):
			aid = request.GET['act_id']
			#change activity state to checked state
			act = WeiaaActivity.objects.get(aid = aid)
			act.state = 1
			act.save()
			#remove unjoined members
			member_list = WeiaaActivityMember.objects.filter(aid = act)
			for m in member_list:
				if m.confirm_state!=1:
					m.delete()
			#select the acitivity plan
			plan_list = WeiaaActivityPlan.objects.filter(aid = act).order_by('-vote')
			plan = plan_list[0]
			plan.is_selected = True
			plan.save()
			if WONIU_DEBUG:
				print 'plan = %s' % plan
				print 'plan.vote = %s' % plan.vote
				print 'plan.is_selected = %s' % plan.is_selected
		else:
			redirect('/')
		return render(request,'weiAA_app/result.html',
			{ 'message_title': '已成功确认该活动','message_content':'已确认的活动'})
	else:
		return render(request,'weiAA_app/weiboLogin.html')
def confirm_join(request):
	if request.session.has_key('weibo_id'):
		weibo_id = request.session['weibo_id']
		if request.GET.has_key('act_id'):
			aid = request.GET['act_id']
			member = WeiaaActivityMember.objects.get(aid__aid = aid, uid__weibo_id = weibo_id)
			member.confirm_state = 1
			member.save()
		else:
			redirect('/')
		return render(request,'weiAA_app/result.html',
			{ 'message_title':'您已加入该活动','message_content':'已加入的活动'})
	else:
		return render(request,'weiAA_app/weiboLogin.html')
def reject_join(request):
	if request.session.has_key('weibo_id'):
		weibo_id = request.session['weibo_id']
		if request.GET.has_key('act_id'):
			aid = request.GET['act_id']
			member = WeiaaActivityMember.objects.get(aid__aid = aid, uid__weibo_id = weibo_id)
			member.confirm_state = 2
			member.save()
		else:
			redirect('/')
		return render(request,'weiAA_app/result.html',
			{ 'message_title':'您已拒绝加入该活动','message_content':''})
	else:
		return render(request,'weiAA_app/weiboLogin.html')

def introduce(request):
	
	return render(request,'weiAA_app/introduce.html')

def logout(request):
	if request.session.has_key('weibo_id'):
		request.session.delete()
		request.session.clear()
		# if request.session.has_key('weibo_id'):
		# 	print("!!! logout failed")
		# else:
		# 	print("----logout success")
		return redirect('/login')
	else:
		return redirect('/login')
def contact_us(request):
	return render(request,'weiAA_app/contact_us.html')
def charge(request):

	if request.session.has_key('weibo_id'):
		act_id = int(request.GET['act_id'])
		if WONIU_DEBUG:
			print "act_id=%s" % act_id
		
		member_list = WeiaaActivityMember.objects.filter(aid__aid = act_id,confirm_state = 1)
		if member_list.count()<=0:
			if WONIU_DEBUG:
				print 'view.charge, act_id error'
			redirect('/')
		plan = WeiaaActivityPlan.objects.filter(aid__aid = act_id, is_selected = True)[0]
		return render(request,"weiAA_app/charge.html",{'member_list':member_list,'plan':plan,})
	else:
		return render(request,'weiAA_app/weiboLogin.html')
def charge_form(request):

	if not request.session.has_key('weibo_id'):
		return render(request,'weiAA_app/weiboLogin.html')
	if not request.POST.has_key('apid'):
		redirect('/')
	weibo_id = request.session['weibo_id']
	current_user = WeiaaUser.objects.filter(weibo_id = weibo_id)[0]
	#活动方案总支出
	apid = int(request.POST['apid'])
	plan = WeiaaActivityPlan.objects.filter(apid = apid)[0]
	plan.real_cost = float(request.POST['%d_real_cost' % apid])
	plan.save()
	#生成收费表
	member_list = WeiaaActivityMember.objects.filter(aid = plan.aid, confirm_state = 1)
	
	for m in member_list:
		key = '%d_%d_real_per_cost' % (apid,m.uid.uid)
		if WONIU_DEBUG:
			print 'key:%s' % key
		real_per_cost = request.POST[key]
		if WONIU_DEBUG:
			print 'real_per_cost:%s' % real_per_cost
		m.real_per_cost = float(real_per_cost)
		m.save()
	#
	current_member = WeiaaActivityMember.objects.filter(aid = plan.aid, uid = current_user)[0]
	current_member.is_paid = True
	current_member.save()
	#修改该活动状态
	act = plan.aid
	act.state = 2
	act.save()
	return render(request,'weiAA_app/result.html',{'message_title':'weiAA已开始帮你提醒收费！'})
def pay(request):
	if not request.session.has_key('weibo_id'):
		return weiboTools.signin()
	aid = int(request.GET['act_id'])
	member_id = int(request.GET['member_id'])
	member = WeiaaActivityMember.objects.filter(aid__aid = aid, uid__uid = member_id)[0]
	real_per_cost = '%.2f' % member.real_per_cost

	return render(request,'weiAA_app/pay.html',{'real_per_cost':real_per_cost})


def finish_act(request):
	if not request.session.has_key('weibo_id'):
		return render(request,'weiAA_app/weiboLogin.html')

	aid = int(request.GET['act_id'])
	if(WeiaaActivity.objects.filter(aid = aid).count()<=0):
		return render(request,'weiAA_app/result.html',{'message_title':'无该收费活动'})
	if(WeiaaActivityMember.objects.filter(aid__aid = aid, is_paid = False).count()>0):
		return render(request,'weiAA_app/result.html',{'message_title':'活动参与者未全部缴费，结束活动失败'})
	act = WeiaaActivity.objects.filter(aid = aid)[0]
	act.state = 3
	act.save()

	return render(request,'weiAA_app/result.html',{'message_title':'该活动已收费成功，您已结束该活动'})


