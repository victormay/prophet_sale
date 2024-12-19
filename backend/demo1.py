from utils.common import parse_token
from utils.password import gen_password, verify_password


# user = {
#     "username": "admin",
#     "passwd": "123456"
# }

# token = gen_token(user)
# print(token)

# print(parse_token(token))

a = parse_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZW1haWwiOiJ1c2VyQHBkc2YuY29tIiwidXNlcm5hbWUiOiJ1c2VyIiwiaW1nIjoibm9ybWFsLnBuZyIsInR5cGUiOjEsImNyZWF0ZV90aW1lIjoiMjAyNC0xMi0wMyAyMjo1NjowNyIsInVwZGF0ZV90aW1lIjoiMjAyNC0xMi0wMyAyMjo1NjowNyIsImV4cCI6MTczMzI0MjIwOX0.V_aGuScdewgGjUO_ePbnx76qqloEOCGkU25HFBsL9B4")
print(a)
print(type(a))