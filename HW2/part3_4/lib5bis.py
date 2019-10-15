import numpy as np
import time
import webbrowser
import re
import string
import json
import csv


def intersection(L1, L2):  # pointers method to obtain intersection between two lists in linear time

    """
    input: two internally sorted list of int
    output: one sorted list of int obtained by the intersection of elements in the two lists
    """

    if L1 == [] or L2 == []:

        return []

    l1 = len(L1)
    l2 = len(L2)

    if len(L1) > len(L2):
        l = l1
        v = True

    else:
        l = l2
        v = False

    ans = []
    i = 0
    j = 0
    k = 0

    while k < l:

        if L1[i] == L2[j]:

            ans.append(L1[i])
            k += 1
            i += 1
            j += 1
            if i == l1:
                break
            if j == l2:
                break

        elif L1[i] < L2[j]:

            i += 1
            if i == l1:
                break
            if v:
                k += 1
        else:

            j += 1
            if j == l2:
                break
            if not v:
                k += 1

    return ans


def union(L1, L2):

    """
    input: two internally sorted list of int
    output: one sorted list of int obtained by union of all elements 
    """

    if L1 == [] or L2 == []:

        return L1 + L2

    l1 = len(L1)
    l2 = len(L2)

    if len(L1) > len(L2):
        l = l1
        v = True

    else:
        l = l2
        v = False

    ans = []
    i = 0
    j = 0
    k = 0

    while k < l:

        if L1[i] == L2[j]:
            ans.append(L1[i])
            i += 1
            j += 1
            k += 1
            if i == l1:
                ans.extend(L2[j:])
                break
            if j == l2:
                ans.extend(L1[i:])
                break

        elif L1[i] < L2[j]:
            ans.append(L1[i])
            i += 1
            if i == l1:
                ans.extend(L2[j:])
                break
            if v:
                k += 1
        else:
            ans.append(L2[j])
            j += 1
            if j == l2:
                ans.extend(L1[i:])
                break
            if not v:
                k += 1
    # if v:
    #    ans.append(L2[-1])
    # else:
    #    ans.append(L1[-1])

    return ans


def negation(L1, L2):

    """
    input: two internally sorted list of int
    output: one sorted list of int obtained removing element of L2 from L1
    """

    if L2 == []:

        return L1
    if L1 == []:
        return []

    l1 = len(L1)
    l2 = len(L2)

    if len(L1) > len(L2):
        l = l1
        v = True
    else:
        l = l2
        v = False

    ans = L1[:]
    i = 0
    j = 0
    k = 0

    while k < l:

        if ans == []:
            return ans

        if L1[i] == L2[j]:

            ans.remove(L2[j])
            k += 1
            i += 1
            j += 1
            if i == l1:
                break
            if j == l2:
                break

        elif L1[i] < L2[j]:
            i += 1
            if i == l1:
                break
            if v:
                k += 1
        else:
            j += 1
            if j == l2:
                break
            if not v:
                k += 1

    return ans


def skiPointers(L1, L2):  # pointers method to obtain intersection between two lists in square root time

    """
    input: two internally sorted list of int
    output: one sorted list of int obtained by the intersection of elements in the two lists
    """

    if L1 == [] or L2 == []:

        return []

    l1 = len(L1)
    l2 = len(L2)

    if len(L1) > len(L2):
        l = l1
        v = True
        skip = int(np.sqrt(l2))
    else:
        l = l2
        v = False
        skip = int(np.sqrt(l1))

    ans = []
    i = 0
    j = 0
    k = 0

    while k < l:

        if L1[i] == L2[j]:
            ans.append(L1[i])
            i += 1
            j += 1
            k += 1
            if i == l1:
                break
            if j == l2:
                break

        elif L1[i] < L2[j]:
            while L1[i] < L2[j]:
                if i + skip >= l1:

                    ans.extend(intersection(L1[i:], L2[j:]))
                    return ans

                else:
                    i += skip
                    if v:
                        k += skip
            i -= skip - 1
            if v:
                k -= skip - 1
        else:
            while L1[i] > L2[j]:
                if j + skip >= l2:

                    ans.extend(intersection(L1[i:], L2[j:]))
                    return ans
                else:
                    j += skip
                    if not v:
                        k += skip
            j -= skip - 1
            if not v:
                k -= skip - 1

    return ans


def queryPointers(Xtot, s, n, invertedPost, indices, f):

    """
    input: 

    Xtot ---> matrix |elements = (tf*id)*weight |nrow = len(n. words)| ncol = len(n. recipes)
    s,n  ---> preprocessed input
    invertedPost ---> dict keys:words |values:list of recipes(number) containing the key
    indices ---> dict keys: number(str) |values: words


    output: list of index
    """

    r = []

    neg = []
    value = True
    for i in s:

        if f == "y":
            if value:
                r = union(r, invertedPost[i])

                value = False
            else:
                r = skiPointers(r, invertedPost[i])

        if f == "n":
            r = union(r, invertedPost[i])

    for j in n:
        try:
            neg = union(neg, invertedPost[j])
        except:
            neg.append("")

    if neg != [] and r != []:
        r = negation(r, neg)

    if r == []:
        return r

    new = subroutine(Xtot, r, s, indices)

    return new


def subroutine(Xtot, r, s, indices):

    X = BuildQueryFromMatrix(Xtot, r)

    y = BuildVector(indices, s)

    res = cosineSimilarity(X, y, r)

    answer = rank(res)  # list

    new = []
    for i in answer:

        new.append(int(i))

    return new


def partialQueryPointers(Xtot, s, n, invertedPost, indices):

    r = []
    neg = []
    for i in s:
        for key in invertedPost:

            if re.search(i, key):
                try:
                    r = union(r, invertedPost[key])

                except:
                    continue
    for j in n:
        for key in invertedPost:

            if re.search(j, key):
                try:
                    neg = union(neg, invertedPost[key])
                except:
                    continue

    if neg != [] and r != []:
        r = negation(r, neg)

    if r == []:
        return r

    new = subroutine(Xtot, r, s, indices)

    return new


def BuildMatrix(wordsDict, indices, d_normalized):

    n = len(indices)
    m = len(d_normalized)
    X = np.zeros((n, m))

    for i in range(n):  # we need an order but it's not important

        docs = wordsDict[indices[str(i)]]  # recipes that contains i-th word

        for recipe in range(1, m):  # the recipes number are correspondent with the number on recipes

            if str(recipe) in docs:

                X[i, recipe] = wordsDict[indices[str(i)]][str(recipe)]

    return X


def BuildVector(indices, string):

    n = len(indices)
    y = np.zeros(n)

    for i in range(n):
        if indices[str(i)] in string:

            y[i] = 1

    return y


def BuildQueryFromMatrix(X, r):

    X_c = np.zeros((X.shape[0], len(r)))

    X_c = X[:, [int(j) for j in r]]

    return X_c


def cosineSimilarity(X, y, r):

    c = (np.transpose(X) * y).sum(axis=1)

    lx = np.sqrt((X ** 2).sum(axis=0))
    ly = np.sqrt((y ** 2).sum(axis=0))

    similarity = c / (lx * ly) * 100

    resDict = {k: v for k, v in zip(similarity, r)}

    return resDict


def rank(resDict):

    final = []

    res = sorted(resDict, reverse=True)

    for h in res:

        t = resDict[h]

        final.append(t)

    return final


def ByCategory(header):

    print("\n")
    print("Categories:")
    for i in range(len(header)):

        print(i, header[i])

    print(8, "Fast Recipes")
    print(9, "No Lactose")

    choose = -1
    while choose < 0 or choose > len(header) + 1 or type(choose) != int:

        print("Please choose a category: ")

        try:
            choose = int(input())

        except:
            continue

    return choose


def OrderByCategory(n, ans, d_normalizedDict, s, term):

    dd = []
    l = len(s)

    ans2 = ans[:term][:]

    for k in ans2[:]:
        count = 0
        for i in s:

            if i in d_normalizedDict[str(k)][n]:
                count += 1

        if count == l:

            dd.append(k)
            ans2.remove(k)

    dd.extend(ans2)

    return dd


def OrderByCategoryPartialMatch(n, ans, d_normalizedDict, s, term):

    dd = []
    l = len(s)

    ans2 = ans[:term][:]
    for k in ans2[:]:

        for i in s:

            if re.search(i, str(d_normalizedDict[str(k)][n])):

                dd.append(k)
                ans2.remove(k)

    dd.extend(ans2)

    return dd


def OrderByOther(n, answer2, d8, d9, term):

    d = []
    if n == 8:
        for k in answer2:
            if len(d) > term:
                break
            if d8[str(k)] == 1:

                d.append(k)
    elif n == 9:
        for k in answer2:
            if len(d) > term:
                break
            if d9[str(k)] == 0:

                d.append(k)

    return d


def chooseRec(d, num, data, dictRecipes):

    b = ""
    while b != "n":

        for key in num:
            if num[key] == d:
                recipe = data[key]
                break

        print("\nwhat do you want to see?")

        for i in range(len(data[0])):

            print(i, data[0][i])

        print(8, "web page")
        print("\n")
        print("choose something:\n")
        ss = -1

        while ss not in [k for k in range(0, 9)]:
            try:
                ss = int(input())
            except:
                continue

        if ss == 8:

            webbrowser.open("http://www.bbc.co.uk/food/recipes/" + dictRecipes[str(key - 1)])
        else:

            print("\n")
            print(data[0][ss] + ":")
            print(formatting(recipe, ss))

        print("\nDo you want to do something else with this recipe?")
        b = ""
        while b not in ["y", "n"]:

            print("y")
            print("n")

            b = input()

    return None


def formatting(recipe, ss):

    if recipe[ss] == "NA":

        return "We don't have this information"

    if ss == 0:

        return re.sub("BBC Food - Recipes - ", "", recipe[ss])

    if ss == 5:

        return recipe[ss].split()[0]

    if ss == 6:

        return re.sub("[\[\]]|'", "", recipe[ss])

    if ss == 7:

        return re.sub("[\[\]]|', '|'", "", recipe[ss])

    return recipe[ss]
