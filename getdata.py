#import spotipy
import numpy as np
import matplotlib.pyplot as plt
import base64
import requests
import datetime
import json
import operator
from urllib.parse import urlencode

client_id = '7275a99aae1a47c2a4d883f1ad5da61f'
client_secret = '90fd995e85024add8246e84dd1027fca'
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

class SpotifyAPI(object):
    access_token = None
    access_token_expires = None
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        
    
    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("Must set client id & secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {"Authorization": f"Basic {client_creds_b64}"}

    def get_token_data(self):
        return {"grant_type": "client_credentials"}
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token


def track_name(trackid):
    if type(trackid) == str:
            headers = {"Authorization": f"Bearer {access_token}"}
            endpoint = f"https://api.spotify.com/v1/tracks/{trackid}"
            data = urlencode({"trackid": trackid, "market": "GB"})
            lookup_url = f"{endpoint}?{data}"
            r = requests.get(lookup_url, headers = headers)
    else:
        raise Exception("Please enter a string track id")

    if r.status_code == 200:
        data = r.json()
    else:
        raise Exception("API track request has gone wrong")

    trackname = data['name']

    return trackname

genre_dict = {}

def track_genres(trackid):

    if type(trackid) == str:
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = f"https://api.spotify.com/v1/tracks/{trackid}"
        data = urlencode({"trackid": trackid, "market": "GB"})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers = headers)
    else:
        raise Exception("Please enter a string track id")

    if r.status_code == 200:
        data = r.json()
    else:
        raise Exception("API track request has gone wrong")

    artistid = data['artists'][0]['external_urls']['spotify'][-22:]

    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = f"https://api.spotify.com/v1/artists/{artistid}"
    data = urlencode({"artistid": artistid, "market": "GB"})
    lookup_url = f"{endpoint}?{data}"
    r = requests.get(lookup_url, headers = headers)

    if r.status_code == 200:
        data = r.json()
    else:
        raise Exception("API artist request has gone wrong")

    genres_list = data['genres']

    for genre in genres_list:
        if genre not in genre_dict.keys():
            genre_dict[genre] = [trackid]
        else:
            if trackid not in genre_dict[genre]:
                genre_dict[genre].append(trackid)
            else:
                pass
##########################################################################

def playlist_to_trackidlist(playlist_id):
    
    if type(playlist_id) == str:
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        data = urlencode({"playlist_id": playlist_id, "market": "GB"})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers = headers)
    else:
        raise Exception("Please enter a string playlist id")
    
    if r.status_code == 200:
        results = r.json()
    else:
        raise Exception("API request has gone wrong")
    
    track_id_list = []
    for i in range(len(results['items'])):
        song_id = results['items'][i]['track']['id']
        track_id_list.append(song_id) 

    return track_id_list

#####################################################

#getting recent tracks
def recent():
    headers = {"Authorization": f"Bearer {access_token}"}
    endpoint = "https://api.spotify.com/v1/me/player/recently-played"
    data = urlencode({"limit":50})
    lookup_url = f"{endpoint}?{data}"
    r = requests.get(lookup_url, headers = headers)

    if r.status_code == 200:
        data = r.json()
        print(data)
    else:
        print(r.status_code)
        raise Exception("API recent activity request has gone wrong")
    
recent()