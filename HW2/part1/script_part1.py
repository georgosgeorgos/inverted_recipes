from lib1 import *

#
import requests
import re
import time
from bs4 import BeautifulSoup
import string
import json
import nltk

# create a dictionary where we store as key letters of alphabet and value
# the whole set of ingredients starting with this letter

foodsDict = {i: [] for i in string.ascii_lowercase}


# create a dictionary where

# keys ----> lower alphabet letters
# values ----> foods starting with this letter

# start = time.time()

for key in string.ascii_lowercase:

    foodsDict[key] = foodsLetter("ingredients", key)


with open("foodsDict.json", "r") as fp:

    foodsDict = json.load(fp)


recipes = set()


# input: v vector of foods, set recipes, page where we start
# output: a set of recipes

for alphabet in foodsDict:

    vector = foodsDict[alphabet]
    recipesLink("keyword", vector, recipes, 2)


recipesDict = {k: v for k, v in enumerate(recipes)}


with open("dictRecipes.json", "r") as fp:

    recipesDict = json.load(fp)


# now download the HTML for all recipes available

dHTML = {}


for key in recipesDict:

    url = "http://www.bbc.co.uk/food/recipes/" + recipesDict[str(key)]
    soup = CheckRequest(url)
    print(key)
    dHTML[key] = soup


# alternative

for i in range(len(recipesDict)):

    url = "http://www.bbc.co.uk/food/recipes/" + recipesDict[str(i)]
    soup = CheckRequest(url)
    print(i)
    dHTML[i] = soup


with open("dictHTML.json", "r") as fp:

    dHTML = json.load(fp)  # DON'T PRINT THIS!!!!!
