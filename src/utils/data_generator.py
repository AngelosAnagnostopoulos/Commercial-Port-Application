#! python3
# A script to populate the projectDB database.

import pprint, random, bs4, requests, re, datetime

ship_url = "https://kidadl.com/articles/boat-names-from-history-nature-and-fiction"
ship_page = requests.get(ship_url)
ship_soup = bs4.BeautifulSoup(ship_page.content, 'lxml')
ship_names_raw = ship_soup.find("div", {"class": "Box-sup55n-0 ArticleBody__BaseArticleBody-yq0zjv-0 ArticleBody__ArticlesBody-yq0zjv-1 gzqKZH jxtqVj edNru rich-text-article-body in-content-ads"}).find_all("strong")

ship_names = [] 

ship_name_pattern = "([0-9]+\. )([a-zA-Z]+ ?[a-zA-Z]+)"
for name in ship_names_raw:
    data = name.get_text()
    data = re.search(ship_name_pattern,data)
    if data is not None:
        data = data.group(2)
        ship_names.append(data)

flags = ["Somali","Pakistani","Australian","German","French","Irish","Sweedish","Finish","Danish","Austrian","Czech","Spanish"]
ports = ["Shanghai, China", "Singapore, Singapore", "Vizag, India","Busan, South Korea","Qingdao, China","Shenzhen, China","Moscow, Russia", "Delhi, India", "Tokyo, Japan", "Heraklion, Crete", "Malta, Malta"]


def random_date(start, end):
    delta = end - start
    int_delta = delta.days 
    res = start + datetime.timedelta(random.randrange(int_delta))
    
    return res.strftime("%Y-%m-%d")

insert_str = """INSERT INTO Ship (S_Name, PrevPort, EstimatedArrivalTime, Constructed, Flag, Length_, GT, DWT) VALUES ('{}','{}',{},{},'{}',{},{},{});"""

def make_ship():
    
    with open("../../sqlStuff/randomShips.sql", "a") as all_ships:
        port = str(random.choice(ports))
        con = "DATE '" + random_date(datetime.datetime.strptime("1940-1-1", "%Y-%m-%d"),datetime.datetime.strptime("2020-1-1", "%Y-%m-%d")) + "'"
        EAT = "DATE '" + random_date(datetime.datetime.strptime("1940-1-1", "%Y-%m-%d"),datetime.datetime.strptime("2020-1-1", "%Y-%m-%d")) + "'"
        flag = str(random.choice(flags))
        name = str(random.choice(ship_names))
        length = random.randint(0,100)
        gt = random.randint(0,10)
        dwt = random.randint(0,100)
        
        ship_data = (name,port,EAT,con,flag,length,gt,dwt)
        sql = (str(insert_str.format(*ship_data)))
        all_ships.write(sql)
        all_ships.write("\n")
        
for i in range(100000):
    make_ship()
