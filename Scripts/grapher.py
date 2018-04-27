import os, math, json

from bokeh.layouts import row,column
from bokeh.charts import Histogram, output_file, show, HeatMap, bins,Bar
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6


#length of packet responses



def main():
	ipids = []
	ttls = []
	responses = []
	blocked, allowed = 0,0
	total = 0
	errors = 0
	for file in os.listdir("../Out"):
		data = json.load(open("../Out/"+file))
		domains = data["domains"]
		blocked+=data["meta"]["blocked"]
		allowed+=data["meta"]["allowed"]
		total+=data["meta"]["tried"]
		errors+=data["meta"]["errors"]
		for k,v in domains.items():
			ipid = domains[k]["ipid"]
			ipids.append(ipid)
			ttl = domains[k]["ttl"]
			ttls.append(ttl)
			response = domains[k]["responses"]
			responses.append(response)
	
	output_file("graiphs.html")
	p1 = Histogram(ipids,title="IPID Distribution")
	p1.xaxis.axis_label = "IPID Values"
	p1.yaxis.axis_label = "Count"

	p2 = Histogram(ttls,title="TTL Distribution")
	p2.xaxis.axis_label = "TTL Values"
	p2.yaxis.axis_label = "Count"

	p3 = Histogram(responses,title="Response Number")
	p3.xaxis.axis_label = "Number of Responses"
	p3.yaxis.axis_label = "Count"

	categories = ["blocked","allowed"]
	quants = [blocked,allowed]
	print("blocked: ",blocked)
	print("allowed: ",allowed)
	print("total: ",total)
	print("errors: ",errors)
	p4 = figure(x_range=categories,title="Blocked vs Allowed")
	p4.vbar(x=categories,top=quants,width=0.3)

	p5 = figure(x_range=["April 2014","April 2018"],title="April 2014 v April 2018")
	p5.vbar(x=["April 2014", "April 2018"],top=[35332,blocked],width=0.3)

	#hmdata = {"ttl":ttls,"ipids":ipids}
	#p3 = HeatMap(hmdata,x=bins("ipids"),y=bins("ttl"),stat='mean')
	show(column(row(p1,p2),row(p3,p4),row(p5)))







if __name__ == '__main__':
	main()
