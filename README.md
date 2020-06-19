# Twitter Bounty
## Mass DM your followers on Twitter, An App Deployed on Heroku

### Web App Landing Page

<img src="https://github.com/npgeorge/twitter-bounty/blob/master/images_github/homepage1.png" alt="drawing" width="800"/>

<img src="https://github.com/npgeorge/twitter-bounty/blob/master/images_github/homepage2.png" alt="drawing" width="600"/>

<img src="https://github.com/npgeorge/twitter-bounty/blob/master/images_github/automated_message.PNG" alt="drawing" width="400"/>

# App Version

Flask App

In progress. Add link to heroku app here. 

## How it Works

This app allows anyone to load a dataframe of their followers and DM them within the limits of the Twitter API. All you need are a Twitter account and developer keys and tokens.

## Developer Version - Google Colab

If you are a developer, use this link for a templated guide to gathering followers and sending DM's after sorting. Developers need to ensure they have "Read, write, and Direct Messages" enabled on their app tokens.
![twitter_permissions](https://github.com/npgeorge/twitter-bounty/blob/master/images_github/twitter_permissions.png)

#### Google Colab Link
[Colab Twitter Mass DM Framework in Python](https://colab.research.google.com/drive/1VSkcCeObI8kd7rmkqKOZCZlkNdirW26K?usp=sharing "Colab Twitter Mass DM Framework in Python")

## Command Line

Clone the repo. Open a python command line in the repo. Load python. Then run "import followers" to load the script.

To see your data frame of followers, run "followers.df()"

![followers_dataframe](https://github.com/npgeorge/twitter-bounty/blob/master/images_github/get_df_of_followers.png)

To send an automated message to your list of followers at a cadence of 87.6 seconds (1000 followers a day), run "followers.dm()".

![direct_message](https://github.com/npgeorge/twitter-bounty/blob/master/images_github/send_a_dm.png)

### Proof
Sit back and let the app work for you.

<img src="https://github.com/npgeorge/twitter-bounty/blob/master/images_github/automated_message.PNG" alt="drawing" width="400"/>
