#Importing libraries for visualization

import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


df = pd.read_csv("netflix_titles.csv")
df.columns
df.dtypes
df.info()


# Missing data
for i in df.columns:
  null_rate = df[i].isna().sum() / len(df) * 100
  if null_rate > 0:
    print("{} null_rate:{}%".format(i,round(null_rate,2)))



# Plot graph for missing data
plt.figure(figsize=(10,6))
sns.displot(
    data = df.isna().melt(value_name="missing"),
    y = "variable",
    hue = "missing",
    multiple = "fill",
    aspect = 1.25)
    
# Replacements
df["country"] = df["country"].fillna(df["country"].mode()[0])
df["cast"].replace(np.nan, "No Data", inplace= True)
df["director"].replace(np.nan, "No Data", inplace = True)
#Drops
df.dropna(inplace=True)
#Drop Duplicates
df.drop_duplicates(inplace = True)

df.isnull().sum()    

# Managing data format
df["date_added"] = pd.to_datetime(df["date_added"])
df["month_added"] = df["date_added"].dt.month
df["month_name_added"] = df["date_added"].dt.month_name()
df["year_added"] = df["date_added"].dt.year

#Example 1, countplot
plt.figure(figsize=(12,5))
plt.title("Top 10 Years", fontfamily = "serif", loc="left", fontsize =20, y = 1.05)
sns.countplot(x="year_added",data=df, order = df["year_added"].value_counts().index[:10], facecolor = (0,0,0,0), linewidth = 5, edgecolor=sns.color_palette("flare"))
plt.show
plt.savefig('Top_10_Years.png')

# Example 2, lineplot
type_year = (df.groupby(["type","year_added"])["title"].size()).reset_index()
fig = plt.figure(figsize=(16,5))
sns.lineplot(data = type_year, x = "year_added", y ="title", hue = "type",style = "type", palette = "magma_r", markers = True, dashes = True)

plt.title("Total content across the years", loc="left", fontsize=20, fontfamily="serif", y=1.05)
plt.show()
plt.savefig("total_content_across_the _years.png")

#Example 3, Displot
type_year = (df.groupby(["type","year_added"])["title"].size()).reset_index()
plt.figure(figsize=(10,8))
sns.displot( 
    data = type_year,
    x = "year_added",
    y = "title",
    hue = "type"
)

#Example 4, Countplot
fig1 = plt.figure(figsize=(15,5))
plt.title("Top countries having most content", fontsize= 20, loc="left",fontfamily ="serif", color="black",y=1.02)
sns.countplot(
    data= df,
    x = "country",
    order = df["country"].value_counts().index[:10],hue= "type", palette = "magma_r")
plt.xlabel("Country Name")
plt.ylabel("Count of contents")
kde = True
plt.show()
plt.savefig("Top countries")

#Cleaning the No Data values to calculate top 5 Director
director = df[df.director!="No Data"].set_index("title").director.str.split(",",expand= True,).stack().reset_index(level=1,drop=True)
(df["director"] == "No Data").sum() # Expected value is 0 


plt.figure(figsize=(13,7))
plt.title("Top 5 Director Based on The Number of Titles", fontsize= 20, loc="left",fontfamily ="serif", color="black",y=1.02)
sns.countplot(y = director, order=director.value_counts().index[:5], palette='magma_r')
plt.show()

#Separating data in two types as TV Shows and Movies
tv_shows = df[df.type == "TV Show"].copy()
movie = df[df.type == "Movie"].copy()
cast = tv_shows[tv_shows.cast!='No Data'].set_index('title').cast.str.split(",",expand=True).stack().reset_index(level=1,drop=True)

plt.figure(figsize=(13,7))
plt.title("Top 5 Cast of TV Shows Based on The Number of Titles", fontsize= 20, loc="left",fontfamily ="serif", color="black",y=1.02)
sns.countplot(y = cast, order=cast.value_counts().index[:5], palette='magma_r')
plt.show()

#Example 5, Displot
plt.figure(figsize=(10,8))
sns.displot(
    data=movie, 
    x ="duration",
    kde=True,
    aspect=2.5
)
plt.show()
print("Mean of movie duration is",(round(movie["duration"].mean(),2)),"minutes")
plt.savefig("Duration analysis")

#Analysing genre of content
genre = df.set_index('title').listed_in.str.split(",",expand=True).stack().reset_index(level=1,drop=True)
plt.figure(figsize=(12,6))
sns.countplot(y = genre, order=genre.value_counts().index[:20])
plt.xlabel("Count of Movies")
plt.show()

