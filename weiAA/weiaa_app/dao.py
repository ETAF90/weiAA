from weiaa_app.models import *

def insert_user(uid,screen_name,access_token,expire_in):
	try:
		user = WeiaaUser.objects.get(weibo_id = uid)
		#add by woniu17 begin
		user.name = screen_name
		user.access_token = access_token
		user.expire_in = expire_in
		user.save()
		#add by woniu17 end
	except WeiaaUser.DoesNotExist:
		user = WeiaaUser(weibo_id = uid,name = screen_name, access_token=access_token,expire_in=expire_in )
		user.save()
		

