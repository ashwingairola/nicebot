import requests
import urllib.request

IG_ACCESS_TOKEN = "6234398719.e5a224b.cc11ddfad02d40bf878902768a8e9492"
BASE_URL = "https://api.instagram.com/v1/"


def self_info():
    request_url = BASE_URL + "users/self/?access_token=" + IG_ACCESS_TOKEN
    print('GET request url :\n%s' % request_url)
    user_request = requests.get(request_url).json()
    print(user_request)

    if user_request['meta']['code'] == 200:
        if len(user_request['data']):
            print("Username: %s" % user_request['data']['username'])
            print("Full Name: %s" % user_request['data']['full_name'])
            print("Followers: %s" % user_request['data']['counts']['followed_by'])
            print("Follows: %s" % user_request['data']['counts']['follows'])
            print("Posts: %s" % user_request['data']['counts']['media'])
        else:
            print("User does not exist!")
    else:
        print("Error! Status code: " + str(user_request['meta']['code']))


def get_user_info():
    user = input("Enter the username to be searched: ")
    request_url = BASE_URL + "users/search?q=" + user + "&access_token=" + IG_ACCESS_TOKEN
    user_request = requests.get(request_url).json()
    print(user_request)


def get_user_id(username):
    request_url = BASE_URL + "users/search?q=" + username + "&access_token=" + IG_ACCESS_TOKEN
    user_data = requests.get(request_url).json()

    if user_data['meta']['code'] == 200:
        return user_data['data'][0]['id']
    else:
        print("Error fetching user data for " + username + "! Status code: " + user_data['meta']['code'])

    return None


def get_recent_media_object(user_id):
    request_url = BASE_URL + "users/" + user_id + "/media/recent/?access_token=" + IG_ACCESS_TOKEN
    media = requests.get(request_url).json()

    if media['meta']['code'] == 200:
        return media

    print("Error fetching latest media for user: " + user_id + ". Status code: " + media['meta']['code'])
    return None


def get_media(media):
    media_name = None

    if media['data'][0]['type'] == 'image':
        media_name = media['data'][0]['id'] + ".jpg"
    elif media['data'][0]['type'] == 'video':
        media_name = media['data'][0]['id'] + ".mp4"

    media_url = media['data'][0]['images']['standard_resolution']['url']

    try:
        urllib.request.urlretrieve(media_url, media_name)
        print("Media successfully downloaded! Media ID:" + media['data'][0]['id'])
    except OSError:
        print("Network Error! Network is currently unreachable.")


def get_self_media():
    self_media = get_recent_media_object('self')

    if self_media is not None:
        if self_media['data']:
            get_media(self_media)
        else:
            print("You have made no posts.")


def get_user_media():
    username = input("Enter the user name for which you wish to see the most recent posts: ")
    user_id = get_user_id(username)

    if user_id is None:
        return

    user_media = get_recent_media_object(user_id)

    if user_media is not None:
        if user_media['data']:
            get_media(user_media)
        else:
            print("User has made no posts.")


def set_like():
    # Get the latest post that the user made.
    user_media = get_recent_media_object('self')

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/likes"
            payload = {"access_token": IG_ACCESS_TOKEN}
            requests.post(request_url, payload)
            print("You liked this post!")
        else:
            print("User has no media to like.")


def remove_like():
    user_media = get_recent_media_object('self')

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/likes/?access_token=" + IG_ACCESS_TOKEN
            requests.delete(request_url)
            print("You unliked this post.")
        else:
            print("User has no media to unlike.")


def get_likes():
    user_media = get_recent_media_object('self')

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/likes/?access_token=" + IG_ACCESS_TOKEN
            liked_users = requests.get(request_url).json()
            print("Following users liked this latest media: ")
            for user in liked_users['data']:
                print(user)


def post_comment():
    user_media = get_recent_media_object('self')

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/comments"

            comment = input("Enter your comment below:\n")

            payload = {
                'access_token': IG_ACCESS_TOKEN,
                'text': comment
            }
            requests.post(request_url, payload)
            print("Comment posted!")
        else:
            print("User has no media to comment on.")

#
# def remove_comment():
#     user_media = get_recent_media_object('self')
#
#     if user_media is not None:
#         if user_media['data']:
#             request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/comments"


self_info()
# get_self_media()
# get_user_info()
# get_user_media()
# set_like()
# remove_like()
# get_likes()
post_comment()
