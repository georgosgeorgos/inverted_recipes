import requests
import re
import time
from bs4 import BeautifulSoup
import string
import json



# manage exceptions

def CheckRequest(r):
    
    '''
    input: url
    output: parsed html
    '''
    
    cnt = "N"
    
    while cnt == "N":
        
        try:
            cnt = requests.get(r)
            
        except:
            
            print("Problem")
            t = 1
    
    
    if cnt.status_code == requests.codes.ok:
     
        soup = BeautifulSoup(cnt.text, "lxml")
        
        
    else:
        
        soup = ""
        print("Problem: ", cnt.status_code)
        
    return soup




def foodsLetter(url, letter):
    
    '''
    input : a character and a string
    output : a list of string(ingredients starting with this character
    '''
    
    pageFoods = []
    
    r = "http://www.bbc.co.uk/food/"+url+"/by/letter/"+letter
    soup = CheckRequest(r)
    
    for link in soup.find_all("a"):
        
        
        if link.get("href").startswith("/food/") and link.img != None :
            
            try:
                food = link["href"]
                food = food.split("/")
                food = food[2]
                pageFoods.append(food)
            
            except:
                continue
    
    return pageFoods



# extract total number of pages of recipes with a certain ingredient
# we assume to be in "view all recipes page with this ingredient"

def multiPage(soup):
    
    '''
    input: html parsed
    output: max num pages
    '''
    
    temp = []

    for link in soup.find_all("a"):
        
        if link.get("class") != None:
            
            if link.get("class") == ["see-all-search"]:


                try:
                    temp.append(int(link.contents[0]))
                except:
                    continue
        
    if temp != []:
            
        return max(temp)
    else:
        
        return 1
    
    
    
# extract the search page for a particular ingredient

def extractSearch(ingredient):
    
    '''
    input: string
    output: url for all recipes with this string
    '''
    
    url = ""
    
    r = "http://www.bbc.co.uk/food/"+ingredient
    
    soup = CheckRequest(r)
    
    for link in soup.find_all("a"):
            
            if link.get("class") == ["see-all-search"]:
                
                try:
                    url = link["href"].split("=")[1]
                except:
                    
                    url = ingredient
                
    return url




def recipesTotal():
    
    '''
    return the total number of recipes
    '''
    
    tot = ""
    
   
    r = "http://www.bbc.co.uk/food/recipes/"  
    soup = soup = CheckRequest(r)

    for link in soup.find_all("h1"):

            if link.get("class") == ["recipe-finder__header"]:

                tot = link.contents[0]
                tot = tot.split(" ")
                tot = tot[0]
                
    tot = int(tot.replace(',' , ''))
    return tot
                
    


def recipesLink(url, v, recipes, page):
    '''
    input: v vector of foods, set recipes, page where we start
    output: a set of recipes 
    
    '''
    
    for index in range(len(v)):
        
        
        ingredient = v[index]
        c = 0
        print("ingredient: ", v[index])
        print("ingredient index: ", index)

        t = len(recipes)
        s = extractSearch(ingredient)
        
        r = "http://www.bbc.co.uk/food/recipes/search?"+ url +"="+ s
        soup = CheckRequest(r)

        
        if len(recipes) == recipesTotal():
            break
            
        else:
            
            link(soup, recipes)
             
            X = multiPage(soup)
            
            if X >=2:
                
                for x in range(page,X+1):

                    if len(recipes) != t and c == 0:
                        
                        print("recipes: ", len(recipes))
                        c = 1

                    page = x
                    print("page "+ v[index]+ " :",x)
                    
                    r = "http://www.bbc.co.uk/food/recipes/search?page="+ str(x) + "&"+url+"="+s
                    soup = CheckRequest(r)

                    link(soup, recipes)

                    if x == X:
                        page = 2
                        

    
    return recipes





def link(soup, recipes):
    
    '''
    search recipes and add
    to a recipes set
    '''
    
    for link in soup.find_all("a"):

                if link.get("href") != None:

                    cond = link.get("href") != "/food/recipes/" and "search" not in link.get("href")
                    

                    if link.get("href").startswith("/food/recipes") and cond:

                        rec = link["href"]
                        rec = rec.split("/")
                        try:
                            rec = rec[3]      # possible index problem!!!! 

                            recipes.add(rec)

                        except:
                            continue
                            
    return recipes