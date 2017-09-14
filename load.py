# -*- coding: utf-8 -*-
import sys
import re
import ttk
import Tkinter as tk
import requests
import os
import json
from  math import sqrt,pow,trunc
from ttkHyperlinkLabel import HyperlinkLabel
from urllib import quote_plus

from config import applongname, appversion
import myNotebook as nb
from config import config


this = sys.modules[__name__]
this.s = None
this.prep = {}
window=tk.Tk()
window.withdraw()
# Lets capture the plugin name we want the name - "EDMC -"
myPlugin = 'Alien Tour'
sites_file = []

with open(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/tours/alien_sites.json') as sites_file: 
	sites = json.load(sites_file)	
	
def max_priority(list):
	y = []
	for key,value in list.iteritems():	
		y.append(value["priority"])
	return max(y)
		

def plugin_start():
	"""
	Load Template plugin into EDMC
	"""
	#this._IMG_KNOWN    = tk.PhotoImage(data = 'R0lGODlhEAAQAMIEAFWjVVWkVWS/ZGfFZ////////////////yH5BAEKAAQALAAAAAAQABAAAAMvSLrc/lAFIUIkYOgNXt5g14Dk0AQlaC1CuglM6w7wgs7rMpvNV4q932VSuRiPjQQAOw==')	# green circle	
	this._IMG_VISITED = tk.PhotoImage(file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/tick3.gif')
	this._IMG_IGNORE = tk.PhotoImage(file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/cross.gif')
	this._IMG_CLIPBOARD = tk.PhotoImage(file = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/clipboard.gif')
	print myPlugin + "Loaded!"
	
	return myPlugin

def mark_visited(event):
	print this.lastsystem
	sites[this.nearest]["visited"] = 1
	print sites[this.nearest]
	this.nearest,distance,lat,lon,active,body,text,priority,x,y,z = findNearest(this.lastsystem,sites)
	print this.nearest
	print distance
	this.status['text'] = this.nearest + " (" + str(distance) +"ly)"
	this.status['url'] = 'https://www.edsm.net/show-system?systemName=%s' % quote_plus(nearest)
	this.description["text"] = text

	
def drop_priority(event):
	print this.lastsystem
	sites[this.nearest]["priority"] = max_priority(sites)+1
	print sites[this.nearest]
	this.nearest,distance,lat,lon,active,body,text,priority,x,y,z = findNearest(this.lastsystem,sites)
	print this.nearest
	print distance
	this.status['text'] = this.nearest + " (" + str(distance) +"ly)"
	this.status['url'] = 'https://www.edsm.net/show-system?systemName=%s' % quote_plus(nearest)	
	this.description["text"] = text
	
def copy_text_to_clipboard(event):
	window.clipboard_clear()  # clear clipboard contents
	window.clipboard_append(this.nearest)  	

def plugin_prefs(parent,cmdr,is_beta):  
	frame = nb.Frame(parent)
	frame.columnconfigure(1, weight=1)

	mySetting_label = nb.Label(frame, text="Need a reset button")
	mySetting_label.grid(padx=10, row=10, sticky=tk.W)

	mySetting_entry = nb.Entry(frame, textvariable=this.mySetting)
	mySetting_entry.grid(padx=10, row=10, column=1, sticky=tk.EW)
		
	return frame

def plugin_app(parent):
	#create a new frame as a containier for the status
	this.frame = tk.Frame(parent)
	#We want three columns, label, text, button
	this.frame.columnconfigure(5, weight=1)
	
	# maybe we want to be able to change the labels?
	this.label = tk.Label(this.frame, text=  "Alien Sites:")
	#this.status = tk.Label(this.frame, anchor=tk.W, text="Getting current location")
	this.status = HyperlinkLabel(this.frame, compound=tk.RIGHT, popup_copy = True)
	this.status["url"] = None
	
	this.system = HyperlinkLabel(parent, compound=tk.RIGHT, popup_copy = True)
	this.clipboard = tk.Label(this.frame, anchor=tk.W, image=this._IMG_CLIPBOARD)
	this.clipboard.bind("<Button-1>", copy_text_to_clipboard)  
	
	this.tick = tk.Label(this.frame, anchor=tk.W, image=this._IMG_VISITED)
	this.tick.bind("<Button-1>", mark_visited)  
	this.cross = tk.Label(this.frame, anchor=tk.W, image=this._IMG_IGNORE)	
	this.cross.bind("<Button-1>", drop_priority)  
	this.spacer = tk.Frame(this.frame)
	this.description = tk.Label(this.frame)
	
	this.label.grid(row = 0, column = 0, sticky=tk.W)
	this.status.grid(row = 0, column = 1, sticky=tk.W)
	this.clipboard.grid(row = 0, column = 2, sticky=tk.W)
	this.tick.grid(row = 0, column = 3, sticky=tk.W)
	this.cross.grid(row = 0, column = 4, sticky=tk.W)
	this.description.grid(row = 1, column = 0, columnspan=4, sticky=tk.W)
	#label.grid(row = 1, column = 0, sticky=tk.W)
	#this.status.grid(row = 1, column = 1, sticky=tk.W)
	#this.icon.pack(side=RIGHT)
	return this.frame

# Log in

# Settings dialog dismissed
def prefs_changed():
	config.set("mySetting", this.bmp_loc.get())
	
	#this.status['text'] = "Prefs changed"
	# config.setint('BMP', this.bmp_loc.get())	# Store new value in config

	
def getDistance(x1,y1,z1,x2,y2,z2):
	return round(sqrt(pow(float(x2)-float(x1),2)+pow(float(y2)-float(y1),2)+pow(float(z2)-float(z1),2)),2)	
	
def findNearest(jumpsystem,list):
	nearest	= { 'distance': 999999, 'name': "Tour Completed" } 
	n=999999
	p=0
	for key,value in list.iteritems():
		#print str(n) +  ">"  + str(sysrec['distance'])
		d = getDistance(jumpsystem["x"],jumpsystem["y"],jumpsystem["z"],value["x"],value["y"],value["z"])
		if value["visited"] == 0:
			if  float(d) < float(n) and value["priority"] <= p:
				try:
					n = d
					p = value["priority"]
					nearest=key
				except:
					print exception
	
	return nearest,n,list[nearest]["lat"],list[nearest]["lon"],list[nearest]["active"],list[nearest]["body"],list[nearest]["text"],list[nearest]["priority"],list[nearest]["x"],list[nearest]["y"],list[nearest]["z"]
		
		
	
# Detect journal events
def journal_entry(cmdr, system, station, entry):

	if entry['event'] == 'FSDJump':
		this.jumpsystem = { "x": entry["StarPos"][0], "y": entry["StarPos"][1], "z": entry["StarPos"][2], "name": entry["StarSystem"] }	
		print this.jumpsystem
		this.nearest,distance,lat,lon,active,body,text,priority,x,y,z = findNearest(this.jumpsystem,sites)
		print nearest
		print distance
		this.status['text'] = nearest + " (" + str(distance) +"ly)"
		this.status['url'] = 'https://www.edsm.net/show-system?systemName=%s' % quote_plus(nearest)
		this.description["text"] = text
		print "Commander Data"
		
	if entry['event'] == 'Location':
		print "Location"
		print entry
		this.lastsystem = { "x": entry["StarPos"][0], "y": entry["StarPos"][1], "z": entry["StarPos"][2], "name": entry["StarSystem"] }
		this.nearest,distance,lat,lon,active,body,text,priority,x,y,z = findNearest(this.lastsystem,sites)
		print nearest
		print distance
		this.status['text'] = nearest + " (" + str(distance) +"ly)"
		this.status['url'] = 'https://www.edsm.net/show-system?systemName=%s' % quote_plus(nearest)
		this.description["text"] = text
		print "Commander Data"
	
	
def edsmGetSystem(system):
	url = 'https://www.edsm.net/api-v1/system?systemName='+quote_plus(system)+'&showCoordinates=1'		
	print url
	r = requests.get(url)
	s =  r.json()
	print s
	return { "x": s["coords"]["x"], "y": s["coords"]["y"], "z": s["coords"]["z"], "name": s["name"] }		
	

# Update some data here too
def cmdr_data(data):
	print "Commander Data"
	#print data
	this.lastsystem = edsmGetSystem(data['lastSystem']['name'])
	this.nearest,distance,lat,lon,active,body,text,priority,x,y,z = findNearest(this.lastsystem,sites)
	print this.nearest
	print distance
	print "setting status"
	this.status['text'] = this.nearest + " (" + str(distance) +"ly)"
	this.status['url'] = 'https://www.edsm.net/show-system?systemName=%s' % quote_plus(nearest)
	this.description["text"] = text
	print "Commander Data"

