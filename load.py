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

with open(os.path.realpath(os.path.dirname(os.path.realpath(__file__)))+'/sites.json') as sites_file: 
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
	label = tk.Label(parent, text= myPlugin + ":")
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
	for sysrec in list:
		#print str(n) +  ">"  + str(sysrec['distance'])
		d = getDistance(jumpsystem["x"],jumpsystem["y"],jumpsystem["z"],sysrec["x"],sysrec["y"],sysrec["z"])
		if float(n) > float(d) and sysrec["visited"]==0:
			try:
				n = d
				nearest=sysrec
			except:
				print exception
	return nearest["name"],n,nearest["lat"],nearest["lon"],nearest["active"]	
	
# Detect journal events
def journal_entry(cmdr, system, station, entry):

    if entry['event'] == 'FSDJump':
		this.jumpsystem = { "x": entry["StarPos"][0], "y": entry["StarPos"][1], "z": entry["StarPos"][2], "name": entry["StarSystem"] }	
		print this.jumpsystem
		nearest,distance,lat,lon,active = findNearest(this.jumpsystem,sites)
		print nearest
		print distance
		this.status['text'] = nearest + " (" + str(distance) +"ly)"
	
	
					
	

# Update some data here too
def cmdr_data(data):
	print "Commander Data"
	this.status['text'] = "Commander Data"

# Defines location (system)
def setLocation(location):
	# just clearing the screenshot location
	this.status['text'] = "setLocation"


