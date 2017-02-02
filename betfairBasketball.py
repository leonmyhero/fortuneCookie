from selenium import webdriver
import time
import csv
from bs4 import BeautifulSoup

class betfair:
    def __init__(self):
        self.indexurl = "https://www.betfair.com/sport/basketball"
        self.matchNames = []
        self.matchUrls = []
        self.matchData = []
        #self.match05Odds = []
        #self.country = []
        #self.tournament = []
        #self.nextPage = ""
        #self.findNextPage = True

    def GetHtml(self, url):
        """
        获取页面源码
        """
        driver = webdriver.Chrome()
        driver.get(url)
        return driver.page_source

    def GetAllNBAUrls(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)
        #el = driver.find_element_by_id('select-odds-setting')
        #for option in el.find_elements_by_tag_name('option'):
        #    print (option.text)
         #   if option.text == 'decimal':
         #       option.click()  # select() in earlier versions of webdriver
         #       time.sleep(3)
         #       break
        select = driver.find_element_by_css_selector('div.ui-clickselect-container')
        #select = driver.find_element_by_class_name("coupon-list ui-clickselect-container")
        #print (select.text)
        markets = driver.find_elements_by_tag_name("li")
        for market in markets:
            #print(market.text)
            if market.text == "NBA Matches":
                market.click()
                time.sleep(3)
                html = driver.page_source
                soup = BeautifulSoup(str(html), 'html.parser')
                for li in soup.find_all("li", {"class": "avb-row"}):
                    url = li.find("a")['href']
                    #print (url)
                    self.matchUrls.append(url)
                #for option in el.find_elements_by_tag_name('option'):
                #    print(option.text)
                #    if option.text == 'decimal':
                 #       option.click()  # select() in earlier versions of webdriver
                 #       time.sleep(3)
                 #       break
                break
            #    html = driver.page_source
            #    soup = BeautifulSoup(str(html), 'html.parser')
            #    li =  soup.find_all("li", {"class": "node"})[1]
                #for aa in li.find_all("a"):
                #    print (aa.text)
            #    self.country.append(li.find_all("a")[1].text)
            #    self.tournament.append(li.find_all("a")[2].text)

                #if soup.find_all("button", {"class": "back mv-bet-button ng-isolate-scope back-button back-selection-button"})[1]:
            #    try:
            #        price = soup.find_all("button", {"class": "back mv-bet-button ng-isolate-scope back-button back-selection-button"})[1]
            #        odd = price.find_all("span")[0].text
            #    except IndexError:
            #        odd = "1.00"
            #    driver.quit()
                #return odd
                #prices = driver.find_elements_by_css_selector("button[class='back mv-bet-button ng-isolate-scope back-button back-selection-button']")
                #print(prices[1].text)
                #return prices[1].text
                #driver.quit()
             #   break
        #return odd
        #driver.quit()
    def GetAllMarketData(self, html):
        soup = BeautifulSoup(str(html), 'html.parser')
        hteam = soup.find("td",{"class":"home-runner"}).text
        ateam = soup.find("td",{"class":"away-runner"}).text
        #match = []
        #matchname = []
        #matchname.append(hteam)
        #matchname.append(ateam)
        matchStr = hteam + "; " + ateam + "; "
        #match.append(matchname)
        stage = soup.find("span",{"class":"ui-countdown "}).text.replace('\n', '')
        stage = stage.replace('\n','')
        #match.append(stage)
        matchStr = matchStr + stage + "; "
        #markets = []
        for div in soup.find_all("div", {"class": "mod-minimarketview mod-minimarketview-minimarketview yui3-minimarketview-content"}):
            #print (div.find("span", {"class": "title"}).text + str(len(div.find_all("span", {"class": "runner-name"}))))
            if len(div.find_all("span", {"class": "runner-name"}))== 2:
                #marketdata = []
                matchStr = matchStr + div.find("span", {"class": "title"}).text + ": "
                #marketdata.append(div.find("span", {"class": "title"}).text)
                #marketdata.append(div.find_all("li")[0].text.replace('\n', ''))
                matchStr = matchStr + div.find_all("li")[0].text.replace('\n', '') + ", "
                #marketdata.append(div.find_all("li")[1].text.replace('\n', ''))
                matchStr = matchStr + div.find_all("li")[1].text.replace('\n', '') + "; "
                #print (div.find("span", {"class": "title"}).text)
                #print (div.find_all("li")[0].text.replace('\n',''))
                #print (div.find_all("li")[1].text.replace('\n', ''))
                #markets.append(marketdata)
            #match.append(markets)
                #print (div.find_all("li", {"class": "runner-item "})[0].text)
        self.matchData.append(matchStr)

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
        for odd in soup.find_all("td", {"class":"odds back selection-2"}):
            o = odd.text.replace('\n','')
            o = o.replace(' ','')
            self.match15Odds.append(o)
        if soup.find("a", {"class":"next-page"}):
            self.findNextPage = True
            self.nextPage = soup.find("a", {"class":"next-page"})['href']
        else:
            self.findNextPage = False
            #print(self.nextPage)

    def run(self):
        self.GetAllNBAUrls(self.indexurl)
        for url in self.matchUrls:
            ourl = "https://www.betfair.com" + url
            print (ourl)
            shtml = self.GetHtml(ourl)
            self.GetAllMarketData(shtml)
        d = open('basketball0118.txt', 'w')
        for data in self.matchData:
            print (data)
            d.write(str(data) + '\n')
        d.close()



if __name__ == '__main__':
    betfair = betfair()
    betfair.run()
