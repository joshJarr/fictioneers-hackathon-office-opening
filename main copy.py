import requests
my_headers = {'Authorization' : 's_84adbe13806cfc63.Rwq7EJWRymjtd_WOIHznF6Q8ZUZ2XQ_ETsPecK4MpJs'}
response = requests.get("http://api.open-notify.org/astros.json", headers=my_headers)
/api/v1/users/me
print(response.json())
# s_84adbe13806cfc63.Rwq7EJWRymjtd_WOIHznF6Q8ZUZ2XQ_ETsPecK4MpJs

# response = requests.post('https://httpbin.org/post', data = {'key':'value'})
curl -X POST https://fictioneers.appspot.com/api/v1/auth/anonymous-token \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer s_84adbe13806cfc63.Rwq7EJWRymjtd_WOIHznF6Q8ZUZ2XQ_ETsPecK4MpJs'

  # https://fictioneers.appspot.com/api/v1/