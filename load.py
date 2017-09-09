# -*- coding: utf-8 -*-
import sys
import re
import ttk
import Tkinter as tk
import requests
import os
import json
from  math import sqrt,pow,trunc

from config import applongname, appversion
import myNotebook as nb
from config import config


this = sys.modules[__name__]
this.s = None
this.prep = {}

# Lets capture the plugin name we want the name - "EDMC -"
myPlugin = 'Alien Tour'
sites_file = []

with open(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/alien_sites.json') as sites_file: 
	sites = json.load(sites_file)	
	

def plugin_start():
	"""
	Load Template plugin into EDMC
	"""
		
	print myPlugin + "Loaded!"
	
	return myPlugin

	

def plugin_prefs(parent,cmdr,is_beta):  
	frame = nb.Frame(parent)
	frame.columnconfigure(1, weight=1)

	mySetting_label = nb.Label(frame, text="Need a reset button")
	mySetting_label.grid(padx=10, row=10, sticky=tk.W)

	mySetting_entry = nb.Entry(frame, textvariable=this.mySetting)
	mySetting_entry.grid(padx=10, row=10, column=1, sticky=tk.EW)
		
	return frame

def plugin_app(parent):
	label = tk.Label(parent, text=  "Next Tour:")
	this.status = tk.Label(parent, anchor=tk.W, text="Ready")
	
		
	return (label, this.status)

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
	for key,value in list.iteritems():
		#print str(n) +  ">"  + str(sysrec['distance'])
		d = getDistance(jumpsystem["x"],jumpsystem["y"],jumpsystem["z"],value["x"],value["y"],value["z"])
		if float(n) > float(d) and value["visited"]==0:
			try:
				n = d
				nearest=key
			except:
				print exception
	return key,n,list[key]["lat"],list[key]["lon"],list[key]["active"],list[key]["body"],list[key]["text"]		
	
# Detect journal events
def journal_entry(cmdr, system, station, entry):

	if entry['event'] == 'FSDJump':
		this.jumpsystem = { "x": entry["StarPos"][0], "y": entry["StarPos"][1], "z": entry["StarPos"][2], "name": entry["StarSystem"] }	
		print this.jumpsystem
		nearest,distance,lat,lon,active,body,text = findNearest(this.jumpsystem,sites)
		print nearest
		print distance
		this.status['text'] = nearest + " (" + str(distance) +"ly)"
		print "Commander Data"
		
	if entry['event'] == 'Location':
		print "Location"
		print entry
		this.lastsystem = { "x": entry["StarPos"][0], "y": entry["StarPos"][1], "z": entry["StarPos"][2], "name": entry["StarSystem"] }
		nearest,distance,lat,lon,active,body,text = findNearest(this.lastsystem,sites)
		print nearest
		print distance
		this.status['text'] = nearest + " (" + str(distance) +"ly)"
		print "Commander Data"
	
	
def edsmGetSystem(system):
	url = 'https://www.edsm.net/api-v1/system?systemName='+system+'&showCoordinates=1'		
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
	nearest,distance,lat,lon,active,body,text = findNearest(this.lastsystem,sites)
	print nearest
	print distance
	print "setting status"
	this.status['text'] = nearest + " (" + str(distance) +"ly)"
	print "Commander Data"

