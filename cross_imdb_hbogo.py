import json, re
import requests as r
import pandas as pd

# Input 
API_KEY = "..." # Go to http://www.omdbapi.com/apikey.aspx and generate an API Key

OMDB_REQUEST = "http://www.omdbapi.com/?apikey={}&t={}"

with open('hbo_element.html', 'r') as myfile:
    data=myfile.read()

hbo_movie_names = re.findall( r'itemName">(.*?)</span>', data)

#hbo_movie_names = hbo_movie_names[:10]

imdb_ratings = {}

for title in hbo_movie_names:
    try:
        movie = r.get(OMDB_REQUEST.format(API_KEY, title.replace(' ', '+'))).content
        print(movie)
        movie = json.loads(movie)
        rating = float(movie["Ratings"][0]["Value"].replace("/10",""))
        print(rating)
        imdb_ratings[title] = rating

    except Exception as e:
        print("##### ERROR #####")
        print(e)

print(imdb_ratings)

df = pd.Series(imdb_ratings)
df = df.sort_values(ascending=False)

print(df)

df.to_csv('results.csv')
