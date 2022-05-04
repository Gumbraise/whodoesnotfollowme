import instagrapi
import json
import sys
from getpass import getpass

config = []
following_list = []
followers_list = []
cl = instagrapi.Client()


def login():
    while True:
        if openJson()['sessionId'] == "":
            while True:
                username = input("Login | Username: ")
                try:
                    password = getpass(prompt="Login | Password: ")
                except Exception as error:
                    print("Login | Error:", error)
                try:
                    verificationcode = input("Login | 2FA: ")
                except Exception as error:
                    print("Login | Error:", error)
                try:
                    cl.login(username, password, verification_code=verificationcode)
                    print('Login | Logged in as {}'.format(cl.username))
                    break
                except:
                    print('Login | Bad password')
            writeJson('sessionId', cl.sessionid)
            print('Login | sessionId saved')
            break
        else:
            try:
                cl.login_by_sessionid(openJson()['sessionId'])
                print('Login | Logged in by sessionId')
                break
            except:
                while True:
                    username = input("Login | Username: ")
                    try:
                        password = getpass(prompt="Login | Password: ")
                    except Exception as error:
                        print("Login | Error:", error)
                    try:
                        cl.login(username, password)
                        print('Login | Logged in as {}'.format(cl.username))
                        break
                    except:
                        print('Login | Bad password')
                writeJson('sessionId', cl.sessionid)
                print('Login | sessionId saved')
                break


def writeJson(key, value):
    with open('config.json', 'r+') as jsonFile:
        data = json.load(jsonFile)
        data[key] = value
        jsonFile.seek(0)
        json.dump(data, jsonFile, indent=4)
        jsonFile.truncate()
        jsonFile.close()


def openJson():
    with open('config.json', 'r') as jsonFile:
        config = json.load(jsonFile)
        jsonFile.close()
        return config


login()
user_id = cl.user_id

grabFollowers = cl.user_followers(user_id)
listFollowers = list(grabFollowers)
intFollowers = list(map(int, listFollowers))

grabFollowing = cl.user_following(user_id)
listFollowing = list(grabFollowing)
intFollowing = list(map(int, listFollowing))


# for following in intFollowing:
#     following_list.append(following["username"])
# for follower in intFollowers:
#     followers_list.append(follower["username"])

# print ((set(followers_list) - set(following_list))) #Personnes abonnées à moi mais moi non
someBitches = (set(intFollowing) - set(intFollowers))  # Personnes à qui je suis abonné

# print (someBitches)
writeJson('theyDontFollowMe', list(someBitches))

for item in someBitches:
    print(cl.username_from_user_id(int(item)))