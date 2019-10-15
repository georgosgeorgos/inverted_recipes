with open("dictHTML.json", "r") as fp:

    dHTML = json.load(fp)  # ATTENTION DON'T PRINT ALL THIS


with open("dictRecipes.json", "r") as fp:

    dictRecipes = json.load(fp)


# tsv = open('data.csv', 'w')

# fieldnames = ["title","author","serves","prepTime", "cookTime", "dietary", "ingredients", "methods"]
# writer = csv.DictWriter(tsv, fieldnames=fieldnames, delimiter = "\t")
# writer.writeheader()

# it works because the keys are the same in dictRecipes and dHTML

# for key in range(0,len(dictRecipes)):
#    print(key)

#    if key%1000 == 0:
#        time.sleep(10)
#    soup = BeautifulSoup(dHTML[str(key)], "lxml")
#    title,author,serves,prepTime, cookTime, dietary, ingredients, methods = extract(soup)

#    writer.writerow({"title": title, "author": author, "serves": serves, "prepTime":prepTime,
#                     "cookTime":cookTime, "dietary": dietary, "ingredients": ingredients, "methods": methods})

# tsv.close()


with open("data.csv") as tsv:
    fieldnames = ["title", "author", "serves", "prepTime", "cookTime", "dietary", "ingredients", "methods"]
    reader = csv.DictReader(tsv, fieldnames=fieldnames, delimiter="\t")
    for row in reader:
        print(row["serves"])


with open("data.csv") as tsv:

    frame = pd.read_csv(tsv, header=0, sep="\t")
