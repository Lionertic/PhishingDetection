import regex
from tldextract import extract
import ssl
import socket
from bs4 import BeautifulSoup
import whois
import favicon
import dns.resolver as resolver
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import tldextract
import requests
import json
import validators
import datetime


def urlHavingIp(url):
    symbol = \
        regex.findall(r'(http((s)?)://)((((\d)+).)*)((\w)+)(/((\w)+))?'
                      , url)
    if len(symbol) != 0:
        having_ip = 1
    else:
        having_ip = -1
    return having_ip


def havingAtSymbol(url):
    symbol = regex.findall(r'@', url)
    if len(symbol) == 0:
        return 1
    else:
        return -1


def urlLength(url):
    length = len(url)
    if length < 54:
        return 1
    elif 54 <= length <= 75:
        return 0
    else:
        return -1


def doubleSlash(url):
    isDoubleSlash = url.find('//')

    isDoubleSlash = url[isDoubleSlash + 2:].find('//')

    if isDoubleSlash > 0:
        return -1
    return 1


def prefixDomain(domain):
    if domain.count('-'):
        return -1
    else:
        return 1


def subDomainCheck(subDomain):
    if subDomain.count('.') == 0:
        return 1
    elif subDomain.count('.') == 1:
        return 0
    else:
        return -1


def httpsToken(host):
    if host.count('https') == 0:
        return 1
    else:
        return -1


def requestUrl(soup, websiteDomain):
    try:
        images = soup.findAll('img', src=True)
        total = len(images)

        linked_to_same = 0
        avg = 0
        for image in images:
            (_, imageDomain, _) = extract(image['src'])
            if websiteDomain == imageDomain or imageDomain == '':
                linked_to_same = linked_to_same + 1

        videos = soup.findAll('video', src=True)
        total = total + len(videos)

        for video in videos:
            (_, vidDomain, _) = extract(video['src'])
            if websiteDomain == vidDomain or vidDomain == '':
                linked_to_same = linked_to_same + 1

        linked_outside = total - linked_to_same

        if total != 0:
            avg = linked_outside / total

        if avg < 0.22:
            return 1
        elif 0.22 <= avg <= 0.61:
            return 0
        else:
            return -1
    except:
        return -1


def urlOfAnchor(soup, websiteDomain):
    try:
        anchors = soup.findAll('a', href=True)
        total = len(anchors)
        linked_to_same = 0
        avg = 0
        for anchor in anchors:
            (_, anchorDomain, _) = extract(anchor['href'])
            if websiteDomain == anchorDomain or anchorDomain == '':
                linked_to_same = linked_to_same + 1
        linked_outside = total - linked_to_same

        if total != 0:
            avg = linked_outside / total

        if avg < 0.31:
            return 1
        elif 0.31 <= avg <= 0.67:
            return 0
        else:
            return -1
    except:
        return -1


def linksInTags(soup):
    try:
        no_of_meta = 0
        no_of_link = 0
        no_of_script = 0
        anchors = 0
        avg = 0
        for _ in soup.find_all('meta'):
            no_of_meta = no_of_meta + 1
        for _ in soup.find_all('link'):
            no_of_link = no_of_link + 1
        for _ in soup.find_all('script'):
            no_of_script = no_of_script + 1
        for _ in soup.find_all('a'):
            anchors = anchors + 1
        total = no_of_meta + no_of_link + no_of_script + anchors
        tags = no_of_meta + no_of_link + no_of_script
        if total != 0:
            avg = tags / total

        if avg < 0.25:
            return 1
        elif 0.25 <= avg <= 0.81:
            return 0
        else:
            return -1
    except:
        return -1


def emailSubmit(soup):
    try:
        if soup.find('mailto:'):
            return -1
        else:
            return 1
    except:
        return -1


def abnormalUrl(soup, orgDomain):
    try:
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
            (subdomain, domain, _) = extract(link)
            if not domain == orgDomain and not subdomain == orgDomain:
                count = count + 1

        if count >= len(links) / 2:
            return -1
        else:
            return 1
    except:

        return -1


def iframe(soup):
    try:
        iFrames = soup.find_all('iframe')

        countOfSuspiciousIframe = 0
        for iFrame in iFrames:
            if iFrame.get('frameborder'):
                if iFrame['frameborder'] == 0:
                    countOfSuspiciousIframe = countOfSuspiciousIframe \
                                              + 1

        if countOfSuspiciousIframe >= len(iFrames) / 2 and len(iFrames) \
                > 1:
            return -1
        else:
            return 1
    except:

        return -1


def redirect(resp, url):
    try:
        subDomainAfterLoading, domainAfterLoading, suffixAfterLoading = extract(resp.url)
        fullUrlAfterLoading = subDomainAfterLoading + '.' + domainAfterLoading + '.' + suffixAfterLoading

        subDomainBeforeLoading, domainBeforeLoading, suffixBeforeLoading = extract(url)
        if(subDomainBeforeLoading == ""):
            subDomainBeforeLoading = "www"
        elif (not subDomainBeforeLoading.startswith("www.") and not subDomainBeforeLoading == ""):
            subDomainBeforeLoading = "www." + subDomainBeforeLoading
        fullUrlBeforeLoading = subDomainBeforeLoading + '.' + domainBeforeLoading + '.' + suffixBeforeLoading

        if fullUrlAfterLoading == fullUrlBeforeLoading:
            return 1
        else:
            return -1
    except:
        return -1

def faviconCheck(url):
    try:
        icon = favicon.get(url)
        if icon:
            return 1
        else:
            return -1
    except:
        return -1


def domainRegistration(w):
    try:
        expiryDate = w['expiration_date'].replace(tzinfo=None)
        createdDate = w['creation_date'].replace(tzinfo=None)
        if expiryDate and createdDate:
            length = (expiryDate - createdDate).days
            if length <= 365:
                return -1
            else:
                return 1
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def ageOfDomain(w):
    try:
        start_date = w['creation_date']
        if start_date:
            current_date = datetime.datetime.now()
            age = (current_date - start_date).days
            if age >= 180:
                return 1
            else:
                return -1
        else:
            return -1
    except Exception as e:
        print(e)
        return -1


def dns(ans):
    if ans['name']:
        return 1
    else:
        return -1


def sslState(useHttps, url):
    try:
        (_, domain, suffix) = extract(url)
        host_name = domain + '.' + suffix
        context = ssl.create_default_context()
        sct = context.wrap_socket(socket.socket(),
                                  server_hostname=host_name)
        sct.connect((host_name, 443))
        certificate = sct.getpeercert()
        issuer = dict(x[0] for x in certificate['issuer'])
        certificate_Auth = str(issuer['commonName'])
        certificate_Auth = certificate_Auth.split()
        if certificate_Auth[0] == 'Network' or certificate_Auth \
                == 'Deutsche':
            certificate_Auth = certificate_Auth[0] + ' ' \
                               + certificate_Auth[1]
        else:
            certificate_Auth = certificate_Auth[0]
        trusted_Auth = [
            'Comodo',
            'Symantec',
            'GoDaddy',
            'GlobalSign',
            'DigiCert',
            'StartCom',
            'Entrust',
            'Verizon',
            'Trustwave',
            'Unizeto',
            'Buypass',
            'QuoVadis',
            'Deutsche Telekom',
            'Network Solutions',
            'SwissSign',
            'IdenTrust',
            'Secom',
            'TWCA',
            'GeoTrust',
            'Thawte',
            'Doster',
            'VeriSign',
            'GTS',
        ]

        # startingDate = certificate['notBefore']
        # endingDate = certificate['notAfter']
        # startingYear = int(startingDate.split()[3])
        # endingYear = int(endingDate.split()[3])
        # Age_of_certificate = endingYear-startingYear

        if useHttps == 1 and certificate_Auth in trusted_Auth:  # and (Age_of_certificate>=1) ):
            return 1
        elif useHttps == 1 and certificate_Auth not in trusted_Auth:
            return 0
        else:
            return -1
    except Exception as e:
        # print(e)
        return -1

# print(sslState(1,"https://google.com"))

def pageRank(url):
    try:
        response = requests.get('https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + url,
                                headers={'API-OPR': 's8gcgokggo8w4oowo4c4o4wsw4csw0wccco0wws4'})

        resp = json.loads(response.content)

        if resp['status_code'] == 200:
            ranking = resp['response'][0]['page_rank_decimal']
            if isinstance(ranking, str):
                return -1

            if ranking > 3:
                return 1
            else:
                return -1
        else:
            return 0
    except Exception as e:
        return -1


def googleIndex(url):
    user_agent = \
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}
    query = {'q': 'info:' + url}
    google = 'https://www.google.com/search?' + urlencode(query)
    data = requests.get(google, headers=headers)
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), 'html.parser')
    try:
        check = soup.find(id='rso').find('div').find('div').find('a')
        link = check['href']
        gotDomain = tldextract.extract(link).domain
        givenDomain = tldextract.extract(url).domain
        if gotDomain == givenDomain:
            return 1
        else:
            return -1
    except:
        return -1


def port(url):
    # ongoing
    return 0


def urlShort(url):
    # ongoing
    return 0


def sfh(url):
    # ongoing
    return 0


def mouseOver(url):
    # ongoing
    return 0


def rightClick(url):
    # ongoing
    return 0


def popup(url):
    # ongoing
    return 0


def webTraffic(url):
    # ongoing
    return 0


def linksPointing(url):
    # ongoing
    return 0


def statistical(url):
    # ongoing
    return 0


def process(url):
    ipUrl = urlLen = urlShortened = atSymbol = hasDoubleSlash = \
        containsHyphen = containMoreSubDomain = isGoodSSL = domainReg = \
        hasFavIcon = isPort = isHttps = inPageRequests = anchorUrls = \
        linkTags = isSFH = isMailTo = isAbnormalUrl = isRedirected = \
        isMouseOver = click = isPop = isIframe = domainAge = \
        hasDNSRecord = traffic = goodPageRank = isPageIndexed = \
        isLinks = isGoodStatistical = 0

    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        subDomain, domain, suffix = extract(resp.url)
        fullUrl = subDomain + '.' + domain + '.' + suffix
        w = whois.query(fullUrl).__dict__
        ipUrl = urlHavingIp(resp.url)
        atSymbol = havingAtSymbol(resp.url)
        urlLen = urlLength(resp.url)
        hasDoubleSlash = doubleSlash(resp.url)
        containsHyphen = prefixDomain(domain)
        containMoreSubDomain = subDomainCheck(subDomain)
        isHttps = httpsToken(fullUrl)
        inPageRequests = requestUrl(soup, domain)
        anchorUrls = urlOfAnchor(soup, domain)
        linkTags = linksInTags(soup)
        isMailTo = emailSubmit(soup)
        isAbnormalUrl = abnormalUrl(soup, domain)
        isIframe = iframe(soup)
        isRedirected = redirect(resp, url)
        hasFavIcon = faviconCheck(url)
        domainAge = ageOfDomain(w)
        domainReg = domainRegistration(w)
        hasDNSRecord = dns(w)
        isGoodSSL = sslState(isHttps, url)
        goodPageRank = pageRank(fullUrl)
        isPageIndexed = googleIndex(resp.url)
        isPort = port(url)
        urlShortened = urlShort(url)
        isSFH = sfh(url)
        isMouseOver = mouseOver(url)
        click = rightClick(url)
        isPop = popup(url)
        traffic = webTraffic(url)
        isLinks = linksPointing(url)
        isGoodStatistical = statistical(url)

        return [[
            ipUrl,
            urlLen,
            urlShortened,
            atSymbol,
            hasDoubleSlash,
            containsHyphen,
            containMoreSubDomain,
            isGoodSSL,
            domainReg,
            hasFavIcon,
            isPort,
            isHttps,
            inPageRequests,
            anchorUrls,
            linkTags,
            isSFH,
            isMailTo,
            isAbnormalUrl,
            isRedirected,
            isMouseOver,
            click,
            isPop,
            isIframe,
            domainAge,
            hasDNSRecord,
            traffic,
            goodPageRank,
            isPageIndexed,
            isLinks,
            isGoodStatistical,
        ]]
    except Exception as e:
        return [[
            ipUrl,
            urlLen,
            urlShortened,
            atSymbol,
            hasDoubleSlash,
            containsHyphen,
            containMoreSubDomain,
            isGoodSSL,
            domainReg,
            hasFavIcon,
            isPort,
            isHttps,
            inPageRequests,
            anchorUrls,
            linkTags,
            isSFH,
            isMailTo,
            isAbnormalUrl,
            isRedirected,
            isMouseOver,
            click,
            isPop,
            isIframe,
            domainAge,
            hasDNSRecord,
            traffic,
            goodPageRank,
            isPageIndexed,
            isLinks,
            isGoodStatistical,
        ]]