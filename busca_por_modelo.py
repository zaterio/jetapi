from bs4 import BeautifulSoup
import requests
import json
import time


def busca_aeronaves(soup):

    result_divs = soup.find_all("div", class_="result", attrs={"data-photo": True})

    airplanes = []

    for result in result_divs:

        links = result.find_all("a", class_="link")

        airplane_info = {}

        for link in links:

            href = link.get("href")

            if "/airline/" in href:

                airline_name = href.split("/")[-1]

                airplane_info["airline"] = airline_name

            if "/registration/" in href:

                airplane_id = href.split("/")[-1]

                airplane_info["airplane_id"] = airplane_id

            if "/photo/" in href:

                airplane_info["photo_url"] = "https://www.jetphotos.com" + href

            if "/aircraft/" in href:

                if "/manufacturer/" in href:

                    manufacturer = href.split("/")

                    airplane_info["manufacturer"] = manufacturer[3]

                    airplane_info["serial"] = manufacturer[5]

                else:
                    model = href.split("/")[-1]
                    airplane_info["model"] = model

        airplanes.append(airplane_info)

    return airplanes


request_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "AWSALB=Sw/aq0yg7wT0s5uL/s/RuHWW1eeOMcMSJdvbDz5Qtq1jp5YNr5o0YcHJJdnEfp+li3tE3j0fh83wvP/IK6VCdXVxdEV4olLQDjhxxeOEwxeDd8es2TFn7bKqFE3m; AWSALBCORS=Sw/aq0yg7wT0s5uL/s/RuHWW1eeOMcMSJdvbDz5Qtq1jp5YNr5o0YcHJJdnEfp+li3tE3j0fh83wvP/IK6VCdXVxdEV4olLQDjhxxeOEwxeDd8es2TFn7bKqFE3m; cf_clearance=0zqT.49q1sy_2M_50.sx4n3326q7bENPuxB41tImZBU-1766167793-1.2.1.1-3GjRChqOydeeToUvq8IHc2cH2VpDVktqQtK163Nbu9gwaLS4Dldz5riHvPmHYHfN9A25DlXNBk8gng7jJK3s.BvDVjqlyoY8pjDj0Rv6YSnAnzV2aMjg0slcFPJfm3WQfFC5xicb_99vbNApvLYB_CzkyDKe1YbAANclR8ISVraKZugVmjY8FmpwOqpswx0qjURPUIHTHZWaMpsriw.B8iFqiBDp4gJNA_xuUHOgFxQ; didomi_dcs=CGazIAynMbjOEnoddpATKoEG6UfOkG6UfUwABBBsAAFooINiAAkUgABoAAQACg0pCbWIZMc4Y7vx4GwDelEGUQsol5RPyiklFaUV0AAGgAFHOGO78eBsA35RXAAA...; euconsent-v2=CQbmPwAQbmPwAAHABBENCGFsAP_gAEPgACQgKhwK4AFAAWAA0ACoAFwAOAAgABaADIAGgARQAmABQAC2AGEANoAgIBBgEIAI4AVoA5AB3ADxAH6AScApoBnADTgG8AToAn8BTYC4QF5gMZAccA5MCEgEZgJGgSZApKBSsCoYKSwFQAFgAVAAuABwAEAAMgAaABMAEIAI4AVoA5AB3AD9AU2AvMBuYDkwJGgSZApKAAAA.fXgAAGgAAAAA; _cfuvid=kIBDq.1Wwx35x29M_pPKjZnr15ApahWEZi45I8R3Eus-1766167043512-0.0.1.1-604800000; JPSESSID=nhfk6n5bfvm4cv20ubtlvr5jnl",
    "Host": "www.jetphotos.com",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Referer": "https://www.jetphotos.com/photo/keyword/AIR%20TRACTOR",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
}


brand = "air tractor"


response = requests.get(
    f"https://www.jetphotos.com/photo/keyword/{brand}", headers=request_headers
)
soup = BeautifulSoup(response.content, "html.parser")
pagings = soup.find_all("a", class_="paging__pager")

# crear variable set vacia, que se llame links_to_pages
links_to_pages = set()

for pag in pagings:
    href = pag.get("href")
    if href != "#":
        try:
            links_to_pages.add("https://www.jetphotos.com" + href)
        except Exception as e:
            print(f"Error al procesar el enlace de paginación: {e}")


airplanes = busca_aeronaves(soup)

for pages in links_to_pages:
    response = requests.get(pages, headers=request_headers)
    soup = BeautifulSoup(response.content, "html.parser")
    new_airplanes = busca_aeronaves(soup)
    airplanes = airplanes + new_airplanes
    time.sleep(5)


epoch = int(time.time())

# Define the filename
filename = f"{brand}_{epoch}.txt"

# Open the file in write mode ('w') and dump the data
try:
    with open(filename, "w") as json_file:
        json.dump(airplanes, json_file, indent=4)
    print(f"Dictionary successfully saved to {filename}")
except IOError as e:
    print(f"Error saving file: {e}")
