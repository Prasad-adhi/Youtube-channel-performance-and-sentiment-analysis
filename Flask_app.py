# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import statistics
from flask import Flask, render_template, request,jsonify
import requests
import pandas as pd
import time
import json
import plotly
import plotly.express as px
import plotly.graph_objs as go
from SentimentAnalysis import sentiment_analysis
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
from API_call import get_channel_id,get_video_details,get_comments,get_statistics,get_all_details
# Flask constructor takes the name of
# current module (__name__) as argument.
API_KEY = "YOUR API KEY"


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def dashboard():
	return render_template("channel.html")

@app.route('/callback', methods=['POST','GET'])
def cb():
	return gm(request.args.get('nval'), request.args.get('yval'))

@app.route('/analysis',methods=["GET","POST"])
def index():
	global statistics_df
	global comments_df

	if request.method == 'POST':
		channel_name = request.form['uname']
		statistics_df,comments_df = get_all_details(channel_name,API_KEY)
	return render_template('gap.html' , graphJSON=gm())

def gm(n='5', gtype ="view_count"):
	global statistics_df
	n = int(n)
	df = pd.read_csv('statistics.csv')
	#df = statistics_df
	dfreduced = df.head(n)
	nlist = []
	for i in range(1,n+1):
		nlist.append(i)
	print(nlist)
	dfreduced['nval'] = nlist
	fig = px.line(dfreduced, x="nval", y=gtype)
	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

@app.route('/sentiment',methods=["GET","POST"])
def sentiment():
	return render_template('pie.html' , graphJSON1=graph())

def graph():
	x = sentiment_analysis("comments.csv")
	y = ['negative', 'positive', 'neutral']
	
	fig_pie = px.pie(values=x, names=y)
	fig_pie.update_layout(autosize=False, width=400,height=300, margin=go.layout.Margin(
        l=10,
        r=10,
        b=20,
        t=20,
        pad = 1
    ))
	graphJSON1 = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON1

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run(debug=True)
