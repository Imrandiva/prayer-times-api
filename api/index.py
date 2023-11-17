# vercel dev

import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from flask_cors import CORS, cross_origin

import dateparser
from duckduckgo_search import ddg
from flask import Flask, jsonify, request


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def home():
    return "It's working!"

@app.route('/api/<string:s>', methods=['GET'])
@cross_origin(origin='*')
def prayer(s):
  # query = str(s + " prayer time site:muslimpro.com")
  data = {}
  # urls = ddg("google", query, max_results=1)")
  # print("hello")

  try :
    # url = urls[0]['href']
    url = "https://www.muslimpro.com/Prayer-times-adhan-Stockholm-Sweden-2673730"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    data = soup.find("div", attrs ={"class": "table-responsive p-0 col-12"})
    
    # Parse the HTML content
    # Find the table element
    table = soup.find('table', class_='prayer-times')

    if table:
        # Initialize an empty dictionary to store the parsed data
        prayer_times = {}

        # Extract the header row to get the prayer names
        header_row = table.find('tr', class_='text-center')

        if header_row:
            prayer_names = [th.get_text() for th in header_row.find_all('th')[1:]]

            # Extract rows containing prayer times
            prayer_rows = table.find_all('tr')[1:]

            # Iterate through each row and extract the data
            for row in prayer_rows:
                date_cell = row.find('td', class_='prayertime-1')
                if date_cell:
                    date = date_cell.get_text()
                    times = [td.get_text() for td in row.find_all('td', class_='prayertime')[1:]]
                    prayer_times[date] = dict(zip(prayer_names, times))

            # Print the parsed data
            print(prayer_times)
        else:
            print("Header row not found.")
    else:
        print("Table not found.")

  except Exception as e:
    print(e)
    data["Error"] = "Result Not Found"
  return jsonify(prayer_times)

# Entry point for Vercel
# def handler(request):
#     return app(request)