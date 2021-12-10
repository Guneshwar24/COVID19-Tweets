from flask import Flask, render_template

# importing libraries
from bs4 import BeautifulSoup as BS
import requests


# method to get the info
def get_info(url):
	
	# getting the request from url
	data = requests.get(url)

	# converting the text
	soup = BS(data.text, 'html.parser')
	
	# finding meta info for total cases
	total = soup.find("div", class_ = "maincounter-number").text
	
	# filtering it
	total = total[1 : len(total) - 2]
	
	# finding meta info for other numbers
	other = soup.find_all("span", class_ = "number-table")
	
	# getting recovered cases number
	recovered = other[2].text
	
	# getting death cases number
	deaths = other[3].text
	
	# filtering the data
	deaths = deaths[1:]
	
	# saving details in dictionary
	ans ={'Total Cases' : total, 'Recovered Cases' : recovered,
								'Total Deaths' : deaths}
	
	# returning the dictionary
	return ans

# url of the corona virus cases
url = "https://www.worldometers.info/coronavirus/"

# calling the get_info method
ans = get_info(url)



app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('dashboard.html')

@app.route("/tweet", methods=['GET', 'POST'])
def tweet():
    return render_template('tweethigh.html')

@app.route("/time", methods=['GET', 'POST'])
def time():
    return render_template('time.html')

@app.route("/vaccine", methods=['GET', 'POST'])
def vaccine():
    return render_template('vaccine.html')


@app.route("/senti", methods=['GET', 'POST'])
def senti():
    return render_template('senti.html')

@app.route("/aboutus", methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus.html')

@app.route("/dash", methods=['GET', 'POST'])
def dash():
    return render_template('dash.html')

@app.route("/realtime", methods=['GET', 'POST'])
def realtime():
    return render_template('realtime.html')

@app.route("/livecount", methods=['GET', 'POST'])
def livecount():
    url = "https://www.worldometers.info/coronavirus/"
    ans = get_info(url)
    total_c=ans.get("Total Cases")
    recovered=ans.get("Recovered Cases")
    total_d=ans.get("Total Deaths")
    return render_template('livecount.html',total_c=total_c,recovered=recovered,total_d=total_d)

if __name__=="__main__":
    app.run(debug=True)