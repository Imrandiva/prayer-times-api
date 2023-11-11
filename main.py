from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive"

@app.route('/api', methods=['GET'])
def prayer():
  s = request.args.get('s')
  query = str(s + " prayer time site:muslimpro.com")
  data = {}
  urls = ddg(query, max_results=1)
  try :
    url = urls[0]['href']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    city = soup.find("p", attrs ={"class": "location"})
    dates = soup.find("div", attrs ={"class": "prayer-daily-title-location"})
    data["city"] = city.get_text()
    data["date"] = dates.get_text()
    data["today"] = {}
    data["tomorrow"] = {}
    prayer_name = soup.find_all("span", attrs ={"class": "waktu-solat"})
    jam = soup.find_all("span", attrs ={"class": "jam-solat"})
    for x,y in zip(prayer_name,jam):
      data["today"][x.get_text()] = y.get_text()
    names = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha'a"]
    try:
      tomorrow = soup.find("tr", attrs={"class": "active"}).find_next("tr").find_all("td", attrs={"class": "prayertime"})
      for x,y in zip(names,tomorrow):
        data["tomorrow"][x] = y.get_text()
    except :
      month = str(dateparser.parse(data["date"]))[5:7]
      url = url + '?date=2021-' + str(int(month)+1)
      response = requests.get(url)
      soup = BeautifulSoup(response.content, "html.parser")
      tomorrow = soup.find_all("tr")[1].find_all("td", attrs={"class": "prayertime"})
      for x,y in zip(names,tomorrow):
        data["tomorrow"][x] = y.get_text()
  except Exception as e:
    print(e)
    data["Error"] = "Result Not Found"
  return jsonify(data)

# def run():
# 	app.run(host='0.0.0.0',port=3000)

# t = Thread(target=run)
# t.start()

# Entry point for Vercel
def handler(request):
    return app(request)