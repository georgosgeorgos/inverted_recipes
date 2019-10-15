import requests
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
import string
import json
import nltk
import csv


def extractTitle(soup):

    title = "NA"

    try:
        title = soup.title.contents[0]
    except:

        title = "NA"

    return title


def extractAuthor(soup):

    author = "NA"

    for link in soup.find_all("a"):

        try:
            if link.get("class") == ["chef__link"] and link.get("itemprop") == "author":

                author = link.contents[0]
        except:

            author = "NA"

    return author


def extractPrepTime(soup):

    prep = "NA"

    for link in soup.find_all("p"):

        try:

            if link.get("class") == ["recipe-metadata__prep-time"]:

                prep = link.contents[0]
        except:

            prep = "NA"

    return prep


def extractCookTime(soup):

    cook = "NA"

    for link in soup.find_all("p"):

        try:

            if link.get("class") == ["recipe-metadata__cook-time"]:

                cook = link.contents[0]
        except:

            cook = "NA"

    return cook


def extractServes(soup):

    serves = "NA"

    for link in soup.find_all("p"):

        try:
            if link.get("class") == ["recipe-metadata__serving"] and link.get("itemprop") == "recipeYield":

                serves = link.contents[0]
        except:

            serves = "NA"

    return serves


def extractDietary(soup):

    diet = "NA"

    for link in soup.find_all("p"):

        try:
            if link.get("class") == ["recipe-metadata__dietary-vegetarian-text"]:

                diet = link.contents[0]
        except:

            diet = "NA"

    return diet


def extractIngredients(soup):

    ingredients = []

    for link in soup.find_all(itemprop="ingredients"):
        try:
            if link.a != None:

                ingredients.extend(link.a.contents)
        except:
            ingredients = "NA"

    return ingredients


def extractMethods(soup):

    methods = []

    for link in soup.find_all(itemprop="recipeInstructions"):
        try:
            methods.extend(link.p.contents)
        except:
            methods = "NA"

    return methods


def extract(soup):

    title = extractTitle(soup)
    author = extractAuthor(soup)
    serves = extractServes(soup)
    prepTime = extractPrepTime(soup)
    cookTime = extractCookTime(soup)
    dietary = extractDietary(soup)
    ingredients = extractIngredients(soup)
    methods = extractMethods(soup)

    return title, author, serves, prepTime, cookTime, dietary, ingredients, methods
