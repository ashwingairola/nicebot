import requests
import urllib.request
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Your unique Instagram Access Token
IG_ACCESS_TOKEN = "<Put your unique Instagram Access Token here>"
# The base URL for accessing the Instagram API
BASE_URL = "https://api.instagram.com/v1/"


# Function to get the information of the user (self)
def self_info():
    request_url = BASE_URL + "users/self/?access_token=" + IG_ACCESS_TOKEN
    user_request = requests.get(request_url).json()

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


# Function to get the information of another user
def get_user_info():
    user = input("Enter the username to be searched: ")
    request_url = BASE_URL + "users/search?q=" + user + "&access_token=" + IG_ACCESS_TOKEN
    user_request = requests.get(request_url).json()

    if user_request['meta']['code'] == 200:
        if len(user_request['data']):
            print("Username: %s" % user_request['data'][0]['username'])
            print("Full Name: %s" % user_request['data'][0]['full_name'])
        else:
            print("User does not exist!")
    else:
        print("Error! Status code: " + str(user_request['meta']['code']))


# Utility function for retrieving the user ID of a user based on the username
def get_user_id(username):
    request_url = BASE_URL + "users/search?q=" + username + "&access_token=" + IG_ACCESS_TOKEN
    user_data = requests.get(request_url).json()

    if user_data['meta']['code'] == 200:
        return user_data['data'][0]['id']
    else:
        print("Error fetching user data for " + username + "! Status code: " + user_data['meta']['code'])

    return None


# Utility function for returning the latest media object
def get_recent_media_object(user_id):
    request_url = BASE_URL + "users/" + user_id + "/media/recent/?access_token=" + IG_ACCESS_TOKEN
    media = requests.get(request_url).json()

    if media['meta']['code'] == 200:
        return media

    print("Error fetching latest media for user: " + user_id + ". Status code: " + media['meta']['code'])
    return None


# Utility function for downloading media based on a media object's URL
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


# Function for downloading the user's (self) latest post
def get_self_media():
    self_media = get_recent_media_object('self')

    if self_media is not None:
        if self_media['data']:
            get_media(self_media)
        else:
            print("You have made no posts.")


# Function for downloading another user's latest post
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


# Function for liking the latest post based on a username
def set_like():
    # Get the latest post that the user made.
    username = input("Enter the user name for which you wish to like the latest post: ")
    user_id = get_user_id(username)

    user_media = get_recent_media_object(user_id)

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/likes"
            payload = {"access_token": IG_ACCESS_TOKEN}
            requests.post(request_url, payload)
            print("You liked this post!")
        else:
            print("User has no media to like.")


# Function for unliking the latest post of another user
def remove_like():
    username = input("Enter the user name for which you wish to unlike the latest post: ")
    user_id = get_user_id(username)

    user_media = get_recent_media_object(user_id)

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/likes/?access_token=" + IG_ACCESS_TOKEN
            requests.delete(request_url)
            print("You unliked this post.")
        else:
            print("User has no media to unlike.")


# Function for getting the number of likes on the latest post of a user
def get_likes():
    username = input("Enter the user name for which you wish to see the likes on the latest post: ")
    user_id = get_user_id(username)

    user_media = get_recent_media_object(user_id)

    if user_media is not None:
        if user_media['data']:
            request_url = BASE_URL + "media/" + user_media['data'][0]['id'] + "/likes/?access_token=" + IG_ACCESS_TOKEN
            liked_users = requests.get(request_url).json()
            print("Following users liked this latest media: ")
            for user in liked_users['data']:
                print(user)


# Function to post a comment on the latest post of a user
def post_comment():
    username = input("Enter the user name for which you wish to post a comment on the latest post: ")
    user_id = get_user_id(username)

    user_media = get_recent_media_object(user_id)

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


# Function to remove all negative comments on the latest post of a user
def delete_negative_comments():
    username = input("Enter the user name for which you wish to delete negative comments on the latest post: ")
    user_id = get_user_id(username)

    media = get_recent_media_object(user_id)
    media_id = media['data'][0]['id']
    request_url = BASE_URL + "media/" + media_id + "/comments/?access_token=" + IG_ACCESS_TOKEN

    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            comment_count = 0

            for comment in comment_info['data']:
                print(comment['text'])
                blob = TextBlob(comment['text'], analyzer=NaiveBayesAnalyzer())
                print(blob.sentiment)
                if blob.sentiment.p_neg > 0.5:
                    print("Verdict: This comment has negative vibes!")

                    request_url = BASE_URL + "media/" + media_id + "/comments/" + comment['id'] + "?access_token=" + \
                                  IG_ACCESS_TOKEN
                    del_response = requests.delete(request_url).json()

                    if del_response['meta']['code'] == 200:
                        print("Comment has been deleted!")
                    else:
                        print("Sorry, comment could not be deleted. Error:" + del_response['meta']['code'])

                comment_count += 1
        else:
            print("There are no comments on this post!")
    else:
        print("Error fetching comment data for media ID: " + media_id)


# The driver function
def driver():
    show_menu = True
    while show_menu:
        menu_choices = '''What do you wish to do?\n1. Get you own info\n2. Get a user's info\n3. See your latest post
4. See a user's latest post\n5. Like a post\n6. Unlike a post\n7. See the number of likes on a post
8. Post a comment\n9. Delete all negative comments on a post\n0. Exit Nicebot\n'''
        choice = eval(input(menu_choices))

        if choice == 1:
            self_info()
        elif choice == 2:
            get_user_info()
        elif choice == 3:
            get_self_media()
        elif choice == 4:
            get_user_media()
        elif choice == 5:
            set_like()
        elif choice == 6:
            remove_like()
        elif choice == 7:
            get_likes()
        elif choice == 8:
            post_comment()
        elif choice == 9:
            delete_negative_comments()
        elif choice == 0:
            print("Bye-bye! Closing Nicebot.")
            show_menu = False


# Start the application
driver()
