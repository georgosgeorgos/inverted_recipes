# 5bis
from lib3 import *
from lib5bis import *
import numpy as np
import re
import time
import pandas as pd
import string
import json
import csv
import webbrowser


# external index for recipes
# keys ----> number (str)
# values ----> recipes identifier (str)
with open("dictRecipes.json", "r") as fp:

    dictRecipes = json.load(fp)

data = []

# all data order using dictRecipes

with open("data.csv") as tsv:

    fieldnames = ["title", "author", "serves", "prepTime", "cookTime", "dietary", "ingredients", "methods"]
    reader = csv.DictReader(tsv, fieldnames=fieldnames, delimiter="\t")
    for row in reader:
        temp = []
        temp.append(
            [
                row["title"],
                row["author"],
                row["serves"],
                row["prepTime"],
                row["cookTime"],
                row["dietary"],
                row["ingredients"],
                row["methods"],
            ]
        )
        data.extend(temp)

# all data normalized (same relative order dictRecipes)

with open("d_normalized.json", "r") as fp:

    d_normalizedDict = json.load(fp)

# fast recipes (same relative order dictRecipes)
# keys ----> number (str)
# values ----> number [0,1]

with open("d8_dict.json", "r") as fp:

    d8_dict = json.load(fp)

# no lactose recipes
# keys ----> number (str)
# values ----> number [0,1]

with open("d9_dict.json", "r") as fp:

    d9_dict = json.load(fp)

# external index for words
# keys ----> numbers (str)
# values ---> words (str)
with open("indexImproved.json", "r") as fp:

    indices = json.load(fp)

# all necessary information is stored here(same order indexes)
# keys ----> words
# values ----> dictionaries where keys ----> numbers related wiht recipes and values ----> (tf*id)*weight
with open("wordsDictImproved.json", "r") as fp:

    wordsDict = json.load(fp)


# inverted index(same order indexes)
# keys ----> words
# values ----> list with all sorted recipes that contain this word
with open("invertedPostImproved.json", "r") as fp:

    invertedPost = json.load(fp)


print("Ok")


# X contains the tf*id frequency for words in every recipe

p = len(wordsDict)
q = len(d_normalizedDict)

X = np.zeros((p, q))

f = open("XcompressImproved.csv", "r")

i = 0
for row in f:
    x = row.split(",")
    for j in range(0, len(x) - 1, 2):

        X[i, int(x[j])] = float(x[j + 1])

    i += 1

f.close()
print("Ok")

# Xweight contains the (tf*id)*weight frequency for words in every recipe

Xweight = np.zeros((p, q))

f = open("XweightCompressImproved.csv", "r")

i = 0
for row in f:
    x = row.split(",")
    for j in range(0, len(x) - 1, 2):

        Xweight[i, int(x[j])] = float(x[j + 1])

    i += 1

f.close()
print("Ok")


# PREPROCESSING ------> improve and save in a file .dat
data_normalized = []

c = 0
for row in data[1:]:

    temp = []
    c = c + 1

    if c % 100 == 0:

        time.sleep(5)
        print(c)
    for i in range(len(row)):

        if i == 0:

            temp.append(preprocessTitle(row[i]))
        else:
            temp.append(preprocess(row[i]))

    data_normalized.append(temp)


data_normalized = []

for i in range(len(d_normalizedDict)):

    data_normalized.append(d_normalizedDict[str(i)])


# create a set of preprocessed words and initialize wordsDict

set_normalized = set()

for recipe in data_normalized[1:]:
    for category in recipe:
        for word in category:
            set_normalized.add(word)

words = list(set_normalized)

wordsDict = {}
wordsDict = {str(key): {} for key in words}


# build inverted index

for recipe in range(1, len(data_normalized)):
    # for argument in d_normalized[recipe+1]:
    for category in data_normalized[recipe]:  # conserve the original order
        for string in category:

            wordsDict[str(string)][str(recipe)] = wordsDict[str(string)].get(str(recipe), 0) + 1


# frequency normalization + id

tot = len(wordsDict)

for key in wordsDict:
    c = 0
    ix = np.log(tot / len(wordsDict[key]))
    for key2 in wordsDict[key]:

        c += wordsDict[key][key2]

    for key2 in wordsDict[key]:

        wordsDict[key][key2] = (wordsDict[key][key2] / c) * ix


X = BuildMatrix(wordsDict, indices, data_normalized)


X_compress = []

p, q = X.shape
for i in range(p):
    temp = []
    for j in range(q):
        if X[i][j] != 0:
            temp.append([j, X[i][j]])
    X_compress.append(temp)


# weighted inverted index
# weighted  title +100  ingredient +25 method +10

for key in wordsDictWeight:
    for key2 in wordsDictWeight[key]:

        title = d_normalizedDict[key2][0]
        ingredients = d_normalizedDict[key2][6]
        method = d_normalizedDict[key2][7]
        if key in title:

            wordsDictWeight[key][key2] = wordsDictWeight[key][key2] * 100

        if key in ingredients:

            wordsDictWeight[key][key2] = wordsDictWeight[key][key2] * 25

        if key in method:

            wordsDictWeight[key][key2] = wordsDictWeight[key][key2] * 10


time = ["10 to 30 mins", "less than 10 mins", "no cooking required"]

d8 = []
d8.append("time")
for row in data[1:]:
    if row[4] in time:

        d8.append(1)
    else:
        d8.append(0)
return d8


milk = [
    "lactose",
    "milk",
    "yogurt",
    "cheese",
    "Buttermilk",
    "CreamSome",
    "Cottage",
    "ricotta",
    "Cream",
    "chocolate",
    "ice cream",
    "Butter",
    "Margarines",
    "butter",
    "Cookies",
    "cakes",
    "pies",
    "pastries",
    "Toffee",
    "butterscotch",
    "caramels",
    "muffins",
    "biscuits",
    "Pancakes",
    "waffles",
    "mascarpone",
    "double-cream",
    "whipped",
    "yoghurt",
    "parmigiano",
]

milk = preprocess(milk)
d9 = []
d9.append("Milk")

for row in d_normalizedImproved[1:]:
    v = False
    c = 0
    for category in row:
        for word in category:
            if word in milk:

                d9.append(1)
                print(word)
                c = 1
                v = True
                break
            if v:
                break
        if v:
            break
    if c == 0:
        d9.append(0)


# simple inverted index

for key in wordsDict:

    invertedPost[key] = sorted(map(int, wordsDict[key].keys()))


decision = ""


while True:

    while decision not in ["r", "x"]:

        print("what do you want to do?\n")
        print("r", "new search")
        print("x", "exit")
        decision = input()

    print("\n")
    if decision == "x":
        print("bye")
        break

    else:

        try:
            b = False
            print("Please search something: \n")
            s = input()
            s = preprocess(s)
            f = "y"
            if len(s) > 1:
                print("Do you want only results containing all your request?")
                print("y")
                print("n")
                f = -1
                while f not in ["y", "n"]:
                    try:
                        f = input()
                    except:
                        continue
            print("\nSomething you don't like: (Enter if none.) \n")
            n = preprocess(input())
            print("please wait a second...")

            answer = queryPointers(X, s, n, invertedPost, indices, f)
            print("we are searching the best fit for your request...\n")
            answerWeighted = queryPointers(Xweight, s, n, invertedPost, indices, f)
            time.sleep(1)

            if answer == []:
                print("sorry nothing to search :(")
                print("\nplease try again you could be lucky :)")
                print("\n")
                decision = "n"

        except:

            try:
                print("No match...we are trying a partial match...")

                answer = partialQueryPointers(X, s, n, invertedPost, indices)
                answerWeighted = partialQueryPointers(Xweight, s, n, invertedPost, indices)
                b = True
                time.sleep(1)
                if answer == []:
                    print("sorry nothing in our database :(")
                    print("\nplease try again you could be lucky :)")
                    print("\n")
                    decision = "n"

            except:
                print("sorry n in our database :(")
                print("\nplease try again you could be lucky :)")
                print("\n")
                decision = "n"

    while decision != "n":

        print("Do you prefer to see the result ordered by higher cosine similarity or by category?")
        print("(the weighted similarity gives different importance to words contained in different part of the text)\n")
        if b:
            print("Attention: you could not obtain a good category result because you obtained only a partial match.")

        while decision not in ["0", "1", "2", "3"]:

            answer2 = answer[:]
            answer2Weighted = answerWeighted[:]
            print("0", "similarity ranking")
            print("1", "similarity ranking weighted")
            print("2", "category ranking")
            print("3", "category ranking weighted")

            decision = input()

        if decision == "2" or decision == "3":
            if decision == "3":
                answer2 = answer2Weighted

            n = ByCategory(data[0])
            # answer2 = answer[:]
            if n in [8, 9]:
                answer2 = OrderByOther(n, answer2, d8_dict, d9_dict, 51)
            else:
                if b:
                    answer2 = OrderByCategoryPartialMatch(n, answer2, d_normalizedDict, s, 51)
                else:
                    answer2 = OrderByCategory(n, answer2, d_normalizedDict, s, 51)

        if answer2 == []:
            print("\nNo result for this category.")
            print("Please try something else:\n")
            decision = -1
        else:
            if decision in ["0", "2", "3"]:
                ans = answer2
            elif decision == "1":
                ans = answer2Weighted

            print("\n")
            print("The requested result is:\n")
            c = 0

            num = {k: v for v, k in enumerate(ans)}
            if n != 8:
                for k in ans:
                    if c > 50:
                        break
                    print(num[k], re.sub("BBC Food - Recipes - ", "", data[k][0]))
                    c += 1
            else:
                for k in ans:
                    if c > 50:
                        break
                    print(num[k], re.sub("BBC Food - Recipes - ", "", data[k][0]), "\t\tCookingTime:", data[k][4])
                    c += 1

            d = -1

            while d not in list(num.values()):
                print("\nPlease choose a recipe:\n")
                try:
                    d = int(input())
                except:
                    continue

            chooseRec(d, num, data, dictRecipes)

            print("\nDo you want to do something else with this documents?")
            print("y")
            print("n")

            while decision not in ["y", "n"]:

                decision = input()
