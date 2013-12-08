from weibo import APIError, APIClient
from django.shortcuts import redirect
from weiaa_app.models import *
from weiaa_app import dao
_APP_ID = "3007283299"
_APP_SECRET = "36d64c3b378852ce604e6123dcc4cc0e"
robot_name = "_woniu_"
def _create_client():
    return APIClient(_APP_ID, _APP_SECRET, 'http://weiaa.sinaapp.com/callback')

def signin():
	client = _create_client()
	return redirect(client.get_authorize_url())
def callback(request):
	client = _create_client()
	access_code = request.GET.get('code')
	#print ("!!!!code = %s" % access_code)
	r = client.request_access_token(access_code)
	access_token = r.access_token
	expires_in = r.expires_in
	weibo_id = r.uid;
	client.set_access_token(access_token, expires_in)
	u = client.users.show.get(uid=weibo_id)
	#print "debug!!!!!!!!! screen_name: %s\n" %u.screen_name
	dao.insert_user(weibo_id,u.screen_name,access_token,expires_in)
	request.session['weibo_id'] = weibo_id
	request.session['access_token'] = access_token
	request.session['expires_in'] =  expires_in
	return True
def find_weibo_id(request,screen_name):
	client = _create_client()
	access_token = request.session['access_token']
	expires_in = request.session['expires_in']
	client.set_access_token(access_token, expires_in)
	u = client.users.show.get(screen_name = screen_name)
	return u.id
def remind_by_weibo(request,status):
	weiaa = WeiaaUser.objects.get(name=robot_name)
	access_token = weiaa.access_token
	expires_in = weiaa.expire_in
	client = _create_client()
	client.set_access_token(access_token, expires_in)
	client.statuses.update.post(status=status)
	#,pic=open('weiAA_app/img/profile.png')
def get_profile_img(request):
	client = _create_client()
	client.set_access_token(request.session['access_token'],request.session['expires_in'])
	u = client.users.show.get(uid = request.session['weibo_id'])
	return u.avatar_large