#encoding: utf-8
from django.utils import simplejson
from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from weiaa_app import weiboTools
from weiaa_app.models import *
WONIU_DEBUG = False
def test(request):
	# return render(request,'weiAA_app/result.html',{
	# 	'message_title':'test ajax'
	# 	})
	plan_id = request.GET.get('plan_id')
	result = simplejson.dumps({'plan_id': plan_id, 'message':'Hello World'})
	return HttpResponse(result, mimetype='application/javascript')

    # return simplejson.dumps({'message':'Hello World'})
def vote(request):
	
	if not request.session.has_key('weibo_id'):
		return weiboTools.signin()
	weibo_id = request.session['weibo_id']
	if WeiaaUser.objects.filter(weibo_id = weibo_id).count()<=0:
		return weiboTools.signin()
	print 'ajax.vote, weibo_id:%s' % weibo_id
	user = WeiaaUser.objects.get(weibo_id = weibo_id)
	
	plan_id = request.GET.get('plan_id')
	plan = WeiaaActivityPlan.objects.get(apid = plan_id)
	vote_num = plan.vote
	if WONIU_DEBUG:
		print 'user:%s' % user
		print 'plan:%s' % plan
	if WeiaaActivityPlanVote.objects.filter(apid = plan, uid = user).count()>0:
		if WONIU_DEBUG:
			print 'already voted'
		result = simplejson.dumps({'vote_num':vote_num,'message':'您已经投过票了'})
		return HttpResponse(result,mimetype='application/javascript')
	# write db
	plan.vote += 1
	plan.save()
	pv = WeiaaActivityPlanVote(apid = plan, uid = user)
	pv.save()
	vote_num = plan.vote
	result = simplejson.dumps({'vote_num':vote_num,'message':'投票成功'})
	return HttpResponse(result,mimetype='application/javascript')

def remind_join(request):

	aid = int(request.GET.get('act_id'))
	uid = int(request.GET.get('member_id'))
	weibo_id = request.session['weibo_id']
	inviter = WeiaaUser.objects.filter(weibo_id = weibo_id )[0]
	invitee = WeiaaUser.objects.filter(uid = uid)[0]
	act = WeiaaActivity.objects.filter(aid = aid)[0]
	status = u'@%s 您好，您的好友@%s 邀请您加入%s 活动，请登入weiAA系统确认http://weiaa.sinaapp.com' % (invitee.name,inviter.name,act.name)
	
	if WONIU_DEBUG:
		print 'remind_join:%s' % uid
		print 'status:%s' % status
	weiboTools.remind_by_weibo(request,status)
	result = simplejson.dumps({'member_id':uid,'message':'已经提醒！'})
	return HttpResponse(result,mimetype='application/javascript')
def remind_fee(request):
	
	aid = int(request.GET.get('act_id'))
	uid = int(request.GET.get('member_id'))
	weibo_id = request.session['weibo_id']
	inviter = WeiaaUser.objects.filter(weibo_id = weibo_id )[0]
	invitee = WeiaaUser.objects.filter(uid = uid)[0]
	act = WeiaaActivity.objects.filter(aid = aid)[0]
	status = u'@%s 您好，您参加的活动%s 已经开始收费，请登入weiAA系统进行查看http://weiaa.sinaapp.com' % (invitee.name,act.name)
	if WONIU_DEBUG:
		print 'remind_join:%s' % uid
		print 'status:%s' % status
	weiboTools.remind_by_weibo(request,status)
	result = simplejson.dumps({'member_id':uid,'message':'已经提醒！'})
	return HttpResponse(result,mimetype='application/javascript')
def remove_member(request):

	aid = int(request.GET.get('act_id'))
	uid = int(request.GET.get('member_id'))
	member = WeiaaActivityMember.objects.filter(aid__aid = aid, uid__uid = uid)[0]
	member.delete()
	result = simplejson.dumps({'member_id':uid,'message':'已经删除！'})
	return HttpResponse(result,mimetype='application/javascript')

def confirm_fee(request):
	if not request.session.has_key('weibo_id'):
		return render(request,'weiAA_app/weiboLogin.html')
	aid = int(request.GET['act_id'])
	member_id = int(request.GET['member_id'])
	if WeiaaActivityMember.objects.filter(aid__aid = aid, uid__uid = member_id)<=0:
		return render(request,'weiAA_app/result.html',{'message_title': '没有该参与者！！' })
	member = WeiaaActivityMember.objects.filter(aid__aid = aid, uid__uid = member_id)[0]
	member.is_paid = True
	member.save()
	result = simplejson.dumps({'status':'已确认该参与者缴费'})
	return HttpResponse(result,mimetype='application/javascript')