from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup
import pymysql.cursors
import pymysql
from datetime import datetime as dt, timedelta

from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup
import pymysql.cursors
import pymysql
from datetime import datetime as dt, timedelta

url = "https://www.betfair.com/exchange/football/coupon?id=6&goingInPlay=false"
driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(str(html), 'html.parser')
for tr in soup.find_all("tr", {"class": "inplaynow"}):
    home = tr.find("span", {"class": "home-team"}).text
    away = tr.find("span", {"class": "away-team"}).text
    period = tr.find("span", {"class": "dtstart time"}).text.replace('\n','')
    print (home + " " + tr.find("span", {"class": "inplaynow-score"}).text.replace('\n','')+ " " + away + " " + period)
    #print (tr.text)
#driver.execute_script("window.open()")
#driver.switch_to_window(driver.window_handles[1])
#river.switch_to_window(driver.window_handles[0])
#print (len(driver.window_handles))
driver.close()

class betfair:
    def __init__(self):
        #self.indexurl = "https://www.betfair.com/exchange/football/coupon?id=4&goingInPlay=false&fdcPage=1&markettype=OVER_UNDER_15"
        self.indexurl1 = "https://www.betfair.com/exchange/football/coupon?id="
        self.indexurl2 = "&goingInPlay=false"
        self.matchNames = []
        self.matchUrls = []
        self.matchList = []
        self.match15Odds = []
        self.match05Odds = []
        self.match25Odds = []
        self.country = []
        self.tournament = []
        self.nextPage = ""
        self.year = 0
        self.findNextPage = True

    def GetHtml(self, url):
        """
        获取页面源码
        """
        driver = webdriver.Chrome()
        driver.get(url)
        return driver.page_source
        driver.close()

    def GetAllOdds(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)
        markets = driver.find_elements_by_tag_name("li")
        full = []
        UO05 = [0,0]
        UO15 = [0,0]
        UO25 = [0,0]
        UO35 = [0,0]
        HUO05 = [0,0]

        for market in markets:
            #print(market.text)
            if market.text == "Goals":
                market.click()
                time.sleep(3)
                html = driver.page_source
                soup = BeautifulSoup(str(html), 'html.parser')
                li =  soup.find_all("li", {"class": "node"})[1]
                #for aa in li.find_all("a"):
                #    print (aa.text)
                country = li.find_all("a")[1].text
                tournament=li.find_all("a")[2].text
                header = soup.find_all("div", {"class":"event-header default ng-scope bf-col-15-24"})[0]
                matchname = header.find_all("span", {"class": "title"})[0].text
                matchtime = header.find_all("div", {"class": "date ng-binding ng-scope"})[0].text
                matchtime = str(self.year) + " " + matchtime
                eventtime = dt.strptime(matchtime, '%Y %a %d %b, %H:%M')
                #print (country + tournament + matchname + matchtime)
                for price in soup.find_all("button", {"class": "back mv-bet-button ng-isolate-scope back-button back-selection-button"}):
                    try:
                        full.append(price.find_all("span")[0].text)
                        #print (price.find_all("span")[0].text)
                    except IndexError:
                        full.append(1)

                        #co = soup.find_all("div", {"class": "other-markets-tab-content ng-scope"})[0]
                        #x=0
                        #for se in soup.find_all("span", {"class": "market-name-label ng-binding"}):
                        #co = se.find_all("span", {"class": "market-name-label ng-binding"})[0]
                        #    print (se.text)
                        #   print (soup.find_all("button", {"class": "mv-bet-button ng-isolate-scope back-button back-selection-button empty"})[x].text)
                        #  x = x+1
                for tab in soup.find_all("div", {"id": "mini-marketview-mod"}):
                    #print (tab.text)
                    #print (tab.find_all("span", {"class": "market-name-label ng-binding"})[0].text)
                    if tab.find_all("span", {"class": "market-name-label ng-binding"})[0].text == "Over/Under 1.5 Goals":
                        UO15[0] = tab.find_all("span", {"class": "bet-button-price"})[0].text
                        UO15[1] = tab.find_all("span", {"class": "bet-button-price"})[2].text
                    elif tab.find_all("span", {"class": "market-name-label ng-binding"})[0].text == "Over/Under 2.5 Goals":
                        UO25[0] = tab.find_all("span", {"class": "bet-button-price"})[0].text
                        UO25[1] = tab.find_all("span", {"class": "bet-button-price"})[2].text
                    elif tab.find_all("span", {"class": "market-name-label ng-binding"})[0].text == "Over/Under 0.5 Goals":
                        UO05[0] = tab.find_all("span", {"class": "bet-button-price"})[0].text
                        UO05[1] = tab.find_all("span", {"class": "bet-button-price"})[2].text
                    elif tab.find_all("span", {"class": "market-name-label ng-binding"})[0].text == "Over/Under 3.5 Goals":
                        UO35[0] = tab.find_all("span", {"class": "bet-button-price"})[0].text
                        UO35[1] = tab.find_all("span", {"class": "bet-button-price"})[2].text
                    elif tab.find_all("span", {"class": "market-name-label ng-binding"})[0].text == "First Half Goals 0.5":
                        HUO05[0] = tab.find_all("span", {"class": "bet-button-price"})[0].text
                        HUO05[1] = tab.find_all("span", {"class": "bet-button-price"})[2].text
                #print (str(UO15[0]) + " " + str(UO15[1]))
                self.SaveDatatoMysql(eventtime, matchname, country, tournament, full[0], full[1], full[2], UO05[1], UO05[0], UO15[1], UO15[0], UO25[1], UO25[0], UO35[1], UO35[0], HUO05[1], HUO05[0])
                print(str(eventtime)+", "+matchname+", "+country+", "+tournament+", "+str(full[0])+", "+str(full[1])+", "+str(full[2])+", "+str(UO05[0])+", "+str(UO05[1])+", "+str(UO15[0])+", "+str(UO15[1])+", "+str(UO25[0])+", "+str(UO25[1])+", "+str(UO35[0])+", "+str(UO35[1])+", "+str(HUO05[0])+", "+str(HUO05[1]))
                #print(tab.find_all("div", {"class": "default name ng-scope"})[0].text + tab.find_all("div", {"class": "default name ng-scope"})[1].text)
                #print(tab.find_all("span", {"class": "bet-button-price"})[0].text + tab.find_all("span", {"class": "bet-button-price"})[2].text)
                #x = 0
                #for se in soup.find_all("tr", {"class": "mini-mv-runner-line ng-scope active-runner"}):
                #    print (se.text)
                #for o in se.find_all("button"):
                #    print (se.find_all("div", {"class": "default name ng-scope"})[0].text)
                #    print (se.find_all("span", {"class": "bet-button-price"})[0].text)
                #x = x +1
                #print ("price" + se.find("button").text)

                #if soup.find_all("button", {"class": "back mv-bet-button ng-isolate-scope back-button back-selection-button"})[1]:
                #try:
                #    price = soup.find_all("button", {"class": "back mv-bet-button ng-isolate-scope back-button back-selection-button"})
                #    price = soup.find_all("button", {"class": "back mv-bet-button ng-isolate-scope back-button back-selection-button"})[1]
                #    odd = price.find_all("span")[0].text
                #except IndexError:
                #    odd = "1.00"
                driver.quit()
                break
        #return odd
        driver.quit()

    def SaveDatatoMysql(self, matchtime, matchname, country, tournament, home, draw, away, over05, under05, over15, under15, over25, under25, over35, under35, hover05, hunder05):
        connection = pymysql.connect(host='localhost',
                                     user='leonmyhero',
                                     password='aaaaaa',
                                     db='betfair',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `soccer` (`Matchdate`, `Matchname`, `Country`, `Tournament`, `Home`, `Draw`, `Away`, `Over05`, `Under05`, `Over15`, `Under15`, `Over25`, `Under25`, `Over35`, `Under35`, `HalfOver05`, `HalfUnder05`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (matchtime, matchname, country, tournament, home, draw, away, over05, under05, over15, under15, over25, under25, over35, under35, hover05, hunder05))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            #with connection.cursor() as cursor:
            #    # Read a single record
            #    sql = "SELECT `id`, `MatchName` FROM `soccer` WHERE `MatchName`=%s"
            #    cursor.execute(sql, ('man',))
            #    result = cursor.fetchone()
            #    print(result)
        finally:
            connection.close()

    def GetAllMatchNameUrl(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        for match in soup.find_all("td",{"class":"name"}):
            #self.matchNames.append(match.text)
            m = match.find("a")
            matchName = m.find_all("span")[0].text + ' v ' + m.find_all('span')[5].text
            #matchName = match.find("a").text
            url = match.find("a")['href']
            self.matchNames.append(matchName)
            self.matchUrls.append(url)
        for tr in soup.find_all("tr", {"class": "inplaynow"}):
            home = tr.find("span", {"class": "home-team"}).text
            away = tr.find("span", {"class": "away-team"}).text
            period = tr.find("span", {"class": "dtstart time"}).text.replace('\n', '')
            result = tr.find("span", {"class": "inplaynow-score"}).text.replace('\n','')
            matchdetail = []
            if result.find(" - ") != -1:
                hscore = int(result[:result.find(" v ")-2])
                ascore = int(result[result.find(" v ") + 5:])
                print(home + " " + tr.find("span", {"class": "inplaynow-score"}).text.replace('\n','') + " " + away + " " + period + " " + str(hscore) + " " + str(ascore))
                matchdetail.append(home)
                matchdetail.append(away)
                matchdetail.append(hscore)
                matchdetail.append(ascore)
                print (matchdetail)
        #for odd in soup.find_all("td", {"class":"odds back selection-2"}):
        #    o = odd.text.replace('\n','')
        #    o = o.replace(' ','')
        #    self.match15Odds.append(o)
        #if soup.find("a", {"class":"next-page"}):
        #     self.findNextPage = True
        #     self.nextPage = soup.find("a", {"class":"next-page"})['href']
        # else:
        #     self.findNextPage = False
            #print(self.nextPage)

    def Get25ODDs(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        for odd in soup.find_all("td", {"class":"odds back selection-2"}):
            o = odd.text.replace('\n','')
            o = o.replace(' ','')
            self.match25Odds.append(o)
        if soup.find("a", {"class":"next-page"}):
            self.findNextPage = True
            self.nextPage = soup.find("a", {"class":"next-page"})['href']
        else:
            self.findNextPage = False
            #print(self.nextPage)

    def run(self):
        #shtml = self.GetHtml(self.indexurl2)
        #self.Get25ODDs(shtml)
        today = dt.today()
        #tomorrow = today + timedelta(days=1)
        dayid = today.toordinal()%7 + 1
        surl = self.indexurl1 + str(dayid) + self.indexurl2
        print (surl)
        shtml = self.GetHtml(surl)
        self.GetAllMatchNameUrl(shtml)

        # d = open('betfair0110.txt', 'w')
        # while True:
        #     shtml = self.GetHtml("https://www.betfair.com" + self.nextPage)
        #     self.GetAllMatchNameUrl(shtml)
        #     print(self.findNextPage)
        #     print (self.nextPage)
        #     if self.findNextPage == False:
        #         break
        #
        # i = 0
        #
        # self.year = dt.now().year
        #
        # for url in self.matchUrls:
        #     ourl = "https://www.betfair.com" + url
        #     print (self.matchNames[i] + " " + ourl)
        #     i += 1
    # i = 0
    # for url in self.matchUrls:
    #     ourl = "https://www.betfair.com" + url
    #     #print (ourl)
    #     try:
    #         self.GetAllOdds(ourl)
    #     except IndexError:
    #         continue
    # d.close()

if __name__ == '__main__':
    betfair = betfair()
    betfair.run()
