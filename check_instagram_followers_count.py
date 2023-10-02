import requests
import json

def check_instagram_followers_count(username):
  """Checks how many Instagram followers the given user has.

  Args:
    username: The username of the Instagram user to check.

  Returns:
    The number of followers the user has, or None if the request was unsuccessful.
  """

  # Make a request to the Instagram API to get the user's information.
  response = requests.get(f"https://www.instagram.com/{username}/?__a=1")

  # Check if the request was successful.
  if response.status_code == 200:
    # Try to extract the user's information from the response. If the JSON
    # response is not valid, the json.loads() function will raise an exception.
    try:
      user_info = json.loads(response.content)
    except json.decoder.JSONDecodeError:
      return None

    # Get the number of followers the user has.
    follower_count = user_info["graphql"]["user"]["edge_followed_by"]["count"]

    # Return the number of followers the user has.
    return follower_count
  else:
    # Return None if the request was not successful.
    return None

def main():
  """The main function."""

  # Get the Instagram username from the user.
  username = input("Enter an Instagram username: ")

  # Check how many followers the user has.
  follower_count = check_instagram_followers_count(username)

  # If the follower count is None, then the request was unsuccessful.
  if follower_count is None:
    print("Error: Could not get the number of followers for the given user.")
  else:
    print(f"The user {username} has {follower_count} followers.")

if __name__ == "__main__":
  main()
