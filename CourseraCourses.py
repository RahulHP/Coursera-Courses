import json
import requests
import webbrowser


jsonresponse=open('jsonresponse.json','w')
courselist=open('courselist.txt','w')


permissions=json.load(open('Permissions.json'))
client_id=permissions['client_id']
client_secret=permissions['client_secret']
redirect_uri=permissions['redirect_uri']


base_auth_url='https://accounts.coursera.org/oauth2/v1/auth'
base_token_url='https://accounts.coursera.org/oauth2/v1/token'
enrollments_url='https://api.coursera.org/api/users/v1/me/enrollments'


code_request_params={'response_type':'code','client_id':client_id,'redirect_uri':redirect_uri,'scope':'view_profile','state':''}
login_url=requests.get(base_auth_url,params=code_request_params)
webbrowser.open(login_url.url,new=1)
print('Please Enter the URL you are redirected to:')
code_response_url=raw_input('>>')
code=str(code_response_url).split('&code=')[1]


token_request_params={  "client_id": client_id,  "code": code,  "client_secret": client_secret,  "redirect_uri": redirect_uri,  "grant_type": "authorization_code"}
access_token_url=requests.post(base_token_url,data=token_request_params)
access_token=access_token_url.json()[u'access_token']




enrollments_headers= {'Authorization': 'Bearer '+str(access_token)}
enrollents_data_request=requests.get(enrollments_url,headers=enrollments_headers)
enrollment_data= enrollents_data_request.json()
json.dump(enrollment_data,jsonresponse)
for i in enrollment_data['courses']:
	print i['name'].encode('utf-8')
	courselist.write(i['name'].encode('utf-8'))
	courselist.write('\n')