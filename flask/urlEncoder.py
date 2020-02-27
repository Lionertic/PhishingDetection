import regex    
from tldextract import extract
import ssl
import socket
from bs4 import BeautifulSoup
import urllib.request
import whois
import datetime
import favicon
import dns.resolver as resolver
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import tldextract
import requests
import json
import validators
import datetime
import time

def url_having_ip(url):
    symbol = regex.findall(r'(http((s)?)://)((((\d)+).)*)((\w)+)(/((\w)+))?',url)
    if(len(symbol)!=0):
       having_ip = 1 #phishing
    else:
       having_ip = -1 #legitimate
    return having_ip

def url_length(url):
    length=len(url)
    if(length<54):
        return 1
    elif(54<=length<=75):
        return 0
    else:
        return -1


def url_short(url):
    #ongoing
    return 0

def having_at_symbol(url):
    symbol=regex.findall(r'@',url)
    if(len(symbol)==0):
        return 1
    else:
        return -1 
    
def doubleSlash(url):
    isDoubleSlash = url.find("//")
    
    isDoubleSlash = url[ isDoubleSlash + 2 : ].find("//")
    
    if isDoubleSlash > 0 :
        return -1
    return 1

def prefix_suffix(url):
    _, domain, _ = extract(url)
    if(domain.count('-')):
        return -1
    else:
        return 1

def sub_domain(url):
    subDomain, _, _ = extract(url)
    if(subDomain.count('.') == 0):
        return 1
    elif(subDomain.count('.') == 1):
        return 0
    else:
        return -1

def SSLfinal_State(url):
    try:
        if(regex.search('^https',url)):
            usehttps = 1
        else:
            usehttps = 0

        _, domain, suffix = extract(url)
        host_name = domain + "." + suffix
        context = ssl.create_default_context()
        sct = context.wrap_socket(socket.socket(), server_hostname = host_name)
        sct.connect((host_name, 443))
        certificate = sct.getpeercert()
        issuer = dict(x[0] for x in certificate['issuer'])
        certificate_Auth = str(issuer['commonName'])
        certificate_Auth = certificate_Auth.split()
        if(certificate_Auth[0] == "Network" or certificate_Auth == "Deutsche"):
            certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]
        else:
            certificate_Auth = certificate_Auth[0] 
        trusted_Auth = ['Comodo','Symantec','GoDaddy','GlobalSign','DigiCert','StartCom','Entrust','Verizon','Trustwave','Unizeto','Buypass','QuoVadis','Deutsche Telekom','Network Solutions','SwissSign','IdenTrust','Secom','TWCA','GeoTrust','Thawte','Doster','VeriSign','GTS']        

        # startingDate = certificate['notBefore']
        # endingDate = certificate['notAfter']
        # startingYear = int(startingDate.split()[3])
        # endingYear = int(endingDate.split()[3])
        # Age_of_certificate = endingYear-startingYear

        if(usehttps==1) and (certificate_Auth in trusted_Auth) :#and (Age_of_certificate>=1) ):
            return 1 
        elif((usehttps==1) and (certificate_Auth not in trusted_Auth)):
            return 0 
        else:
            return -1 
        
    except:
        return -1

def domain_registration(url):
    try:
        w = whois.whois(url)
        updated = w.updated_date
        exp = w.expiration_date

        if updated and exp:
            length = (exp[0]-updated[0]).days
            if(length<=365):
                return -1
            else:
                return 1
        else:
            return -1
    except:
        return -1

def faviconCheck(url):
    try:
        icon = favicon.get(url)
        if(icon):
            return 1
        else:
            return -1
    except:
        return -1

def port(url):
    #ongoing
    return 0

def https_token(url):
    subDomain, domain, suffix = extract(url)
    host = subDomain +'.' + domain + '.' + suffix 

    if(host.count('https') == 0):
        return 1
    else:
        return -1

def request_url(url):   
    try:
        _, domain, _ = extract(url)
        websiteDomain = domain
        
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'html.parser')
        imgs = soup.findAll('img', src=True)
        total = len(imgs)
        
        linked_to_same = 0
        avg =0
        for image in imgs:
            _, domain, _ = extract(image['src'])
            imageDomain = domain
            if(websiteDomain==imageDomain or imageDomain==''):
                linked_to_same = linked_to_same + 1
        vids = soup.findAll('video', src=True)
        total = total + len(vids)
        
        for video in vids:
            _, domain, _ = extract(video['src'])
            vidDomain = domain
            if(websiteDomain==vidDomain or vidDomain==''):
                linked_to_same = linked_to_same + 1
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total
            
        if(avg<0.22):
            return 1
        elif(0.22<=avg<=0.61):
            return 0
        else:
            return -1
    except :
        return -1

def url_of_anchor(url):
    try:
        _, domain, _ = extract(url)
        websiteDomain = domain
        
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'html.parser')
        anchors = soup.findAll('a', href=True)
        total = len(anchors)
        linked_to_same = 0
        avg = 0
        for anchor in anchors:
            _, domain, _ = extract(anchor['href'])
            anchorDomain = domain
            if(websiteDomain==anchorDomain or anchorDomain==''):
                linked_to_same = linked_to_same + 1
        linked_outside = total-linked_to_same
        if(total!=0):
            avg = linked_outside/total
            
        if(avg<0.31):
            return 1
        elif(0.31<=avg<=0.67):
            return 0
        else:
            return -1
    except:
        return -1

def Links_in_tags(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'html.parser')
        
        no_of_meta =0
        no_of_link =0
        no_of_script =0
        anchors=0
        avg =0
        for _ in soup.find_all('meta'):
            no_of_meta = no_of_meta+1
        for _ in soup.find_all('link'):
            no_of_link = no_of_link +1
        for _ in soup.find_all('script'):
            no_of_script = no_of_script+1
        for _ in soup.find_all('a'):
            anchors = anchors+1
        total = no_of_meta + no_of_link + no_of_script+anchors
        tags = no_of_meta + no_of_link + no_of_script
        if(total!=0):
            avg = tags/total

        if(avg<0.25):
            return 1
        elif(0.25<=avg<=0.81):
            return 0
        else:
            return -1        
    except:        
        return -1


def sfh(url):
    #ongoing
    return 0

def email_submit(url):
    try:
        opener = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(opener, 'html.parser')

        if(soup.find('mailto:')):
            return -1
        else:
            return 1 
    except:
        return -1


def abnormal_url(url):
    try:
        opener = requests.get(url)
        soup = BeautifulSoup(opener.content, 'html.parser')
        _, orgDomain, _ = extract(url)

        anchors = soup.find_all('a')
        links = []
        for anchor in anchors:
            link = anchor['href']
            if validators.url(link):
                links.append(link)

        cssLinks = soup.find_all('link')
        for cssLink in cssLinks:
            link = cssLink['href']
            if validators.url(link):
                links.append(link)
            
        
        jsLinks = soup.find_all('script')
        for jsLink in jsLinks:
            if jsLink.get('src'):
                link = jsLink['src']
                if validators.url(link):
                    links.append(link)
            elif jsLink.get('data-src'):
                link = jsLink['data-src']
                if validators.url(link):
                    links.append(link)    
        count = 0
        for link in links:
            subdomain, domain, _ = extract(link)
            if (not (domain == orgDomain)) and (not (subdomain == orgDomain)):
                count = count + 1  

        if count >= len(links)/2:
            return -1
        else:
            return 1
            
    except:        
        return -1

def redirect(url):
    try:
        resp = requests.get(url)
        redirected = resp.url != url
        print(redirected)
        if(not redirected):
            return 1
        else:
            return -1 
    except:
        return -1

def on_mouseover(url):
    #ongoing
    return 0

def rightClick(url):
    #ongoing
    return 0

def popup(url):
    #ongoing
    return 0

def iframe(url):
    try:
        opener = requests.get(url)
        soup = BeautifulSoup(opener.content, 'html.parser')

        iFrames = soup.find_all('iframe')

        countOfSuspiciousIframe = 0 
        for iFrame in iFrames:
            print(iFrame)
            if iFrame.get('frameborder') :
                if iFrame['frameborder'] == 0 :
                    countOfSuspiciousIframe =  countOfSuspiciousIframe + 1

        if countOfSuspiciousIframe >= len(iFrames)/2 and len(iFrames) > 1:
            return -1
        else:
            return 1
            
    except:
        return -1


def age_of_domain(url):
    try:
        w = whois.whois(url)
        start_date = w.creation_date
        if start_date:
            current_date = datetime.datetime.now()
            age =(current_date-start_date[0]).days
            if(age>=180):
                return 1
            else:
                return -1
        else:
            return -1
    except:
        return -1
        
def dns(url):
    subDomain,domain,d=extract(url)
    url = ''
    if subDomain :
        url = subDomain + "."
    url = url + domain + "." + d
    ans = whois.whois(url)
    if ans["domain_name"]:
        return 1
    else:
        return -1


def web_traffic(url):
    #ongoing
    return 0

def page_rank(url):
    try:
        response = requests.get("https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D="+url,headers={'API-OPR':'s8gcgokggo8w4oowo4c4o4wsw4csw0wccco0wws4'})

        resp = json.loads(response.content)

        if resp['status_code'] == 200 :
            ranking = resp['response'][0]['page_rank_decimal']
            
            if isinstance(ranking,str):
                return -1

            if ranking > 3 :
                return 1
            else :
                return -1
        else:
            return 0
    except:
        return -1

def google_index(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = { 'User-Agent' : user_agent}
    query = {'q': 'info:' + url}
    google = "https://www.google.com/search?" + urlencode(query)
    data = requests.get(google, headers=headers)
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), "html.parser")
    try:
        check = soup.find(id="rso").find("div").find("div").find("a")
        link = check['href']
        gotDomain = tldextract.extract(link).domain
        givenDomain = tldextract.extract(url).domain
        if gotDomain == givenDomain :
            return 1
        else :
            return -1 
    except:
        return -1


def links_pointing(url):
    #ongoing
    return 0

def statistical(url):
    #ongoing
    return 0

def getTimeStamp(times):
  timestamp = []

  timestamp.append(int(times[1]))

  month = times[0]
  if 'Jan' == month:
    timestamp.append(1)
  elif 'Feb' == month:
    timestamp.append(2)
  elif 'Mar' == month:
    timestamp.append(3)
  elif 'Apr' == month:
    timestamp.append(4)
  elif 'May' == month:
    timestamp.append(5)
  elif 'Jun' == month:
    timestamp.append(6)
  elif 'Jul' == month:
    timestamp.append(7)
  elif 'Aug' == month:
    timestamp.append(8)
  elif 'Sept' == month:
    timestamp.append(9)
  elif 'Oct' == month:
    timestamp.append(10)
  elif 'Nov' == month:
    timestamp.append(11)
  elif 'Dec' == month:
    timestamp.append(12)

  timestamp.append(int(times[3]))

  t = times[2].split(':')

  timestamp.append(int(t[0]))
  timestamp.append(int(t[1]))
  timestamp.append(int(t[2]))
  tim = datetime.datetime(timestamp[2],timestamp[1],timestamp[0],timestamp[3],timestamp[4],timestamp[5])
  ti = time.mktime(tim.timetuple())
  return ti


def process(url):
    
    check = [[url_having_ip(url),url_length(url),url_short(url),having_at_symbol(url),
             doubleSlash(url),prefix_suffix(url),sub_domain(url),SSLfinal_State(url),
              domain_registration(url),faviconCheck(url),port(url),https_token(url),request_url(url),
              url_of_anchor(url),Links_in_tags(url),sfh(url),email_submit(url),abnormal_url(url),
              redirect(url),on_mouseover(url),rightClick(url),popup(url),iframe(url),
              age_of_domain(url),dns(url),web_traffic(url),page_rank(url),google_index(url),
              links_pointing(url),statistical(url)]]

    return check