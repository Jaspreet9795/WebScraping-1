import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

def convert_to_num(rating):
    if(rating == 'Five'):
        return 5
    if(rating == 'Four'):
        return 4
    if(rating == 'Three'):
        return 3
    if(rating == 'Two'):
        return 2
    if(rating == 'One'):
        return 1
    return 0

def books_list():

    title_list=[]
    title_len_list=[]
    image_name_list=[]
    image_type_list=[]
    category_list=[]
    rating_list=[]

    with open("books.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "category","price", "In_stock","Star_rating", "Image_url","Page_url" ])
        for i in range(1,51):
            page= requests.get(f"http://books.toscrape.com/catalogue/page-{i}.html")
            soup= BeautifulSoup(page.content,'html.parser')
            articles=soup.findAll("article", class_="product_pod")
        
            for article in articles:
                title = article.find('h3').text
                price = article.find("p", class_= "price_color").text
                in_stock= article.find("p", class_= "instock availability").text
                image_url = article.find('img', class_="thumbnail")['src']
                star_rating = convert_to_num( article.find("p")["class"][1] )
                page_url= article.find("a")["href"]
                page_load= requests.get("http://books.toscrape.com/catalogue/"+ page_url)
                page_soup= BeautifulSoup(page_load.content, "html.parser")
                category= page_soup.find("ul", class_="breadcrumb").findAll("a")[2].text
                writer.writerow([title,category, price, in_stock, star_rating, image_url, page_url]) 

                book_title_length=len(title)
                image_filename= image_url.split(".")[-2].split("/")[-1]
                image_type= image_url.split(".")[-1]
                
                image_name_list.append(image_filename)
                image_type_list.append(image_type)
                title_list.append(title)
                title_len_list.append(book_title_length)
                # category_list.append(category)
                # rating_list.append(star_rating)

    # Part 2 Renaming the columns of books.csv and creating booksRenamed.csv using Pandas
    df= pd.read_csv("books.csv")
    df.columns.values[0]= "Title"  
    df.columns.values[1]= "genre"
    df.columns.values[2]= "listing_price"
    df.columns.values[3]="currently_available"
    df.columns.values[4]= "rating"
    df.columns.values[5]= "book_cover"
    df.columns.values[6]= "book_url"
    df.to_csv("booksRenamed.csv")

    #Part 3 : Creating bookStats.csv with new columns using pandas

    data={"book_title":title_list, "book_title_length":title_len_list, "image_filename":image_name_list, "image_type":image_type_list}
    data_frame =pd.DataFrame(data)
    data_frame.to_csv("bookStats.csv")

    #Part 4  Sorting Category and Rating 
    data_frame_sorted= df.sort_values(by=["genre", "rating"])
    data_frame_sorted.to_csv("sortByCategoryAndRating.csv")
    
    #Part 5 i)
     
    with_A=[]
    with_H=[]
    with_L=[]
    for i in title_list:
        if (i[0]=="A"):
            with_A.append(i)
        if (i[0]=="H"):
            with_H.append(i)
        if (i[0]=="L"):
            with_L.append(i)
    
    length_A=len(with_A)
    length_H=len(with_H)
    length_L=len(with_L)
    # print(str(length_A)+" "+ str(length_H) +" "+ str(length_L))
  

    # ii)
    # category_rating_filter=[]
    # filter_category_rating= df.loc[(df["genre"]== "Mystery" | "Nonfiction") & (df["rating"]==3)]
    # category_rating_filter.append(filter_category_rating)
    
    # filter_category= df.loc[ (df['genre']=='Mystery')|(df['genre']=='Nonfiction') ]
    # filter_category= df[df['genre'].isin(['Mystery', 'Nonfiction'] & (df["rating"]==3) )]
    # category_rating_filter.append(filter_category)
    # filter_rating= filter_category.[()]
    
    # print(len(category_rating_filter))
    # print(filter_category)




books_list()





