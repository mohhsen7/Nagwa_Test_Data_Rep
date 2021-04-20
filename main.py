import numpy as np #importing librraries
import pandas as pd
import csv
import warnings
import io
import os
import os.path
import sys
from ctypes import *
from os.path import isfile, join
from os import listdir
import xml.etree.ElementTree as et
import subprocess
import platform
warnings.filterwarnings("ignore")
# getting files' names
files = [f for f in listdir('Explainers') if isfile(join('Explainers', f))]
dts = []
names = []
dv_ns = []
n = 0
srcids =[]
seos = []
#storing file data
for f in files:
    path = os.path.join('Explainers',files[n])
    dts.append(et.parse(path))
    n = n+1
#parsing trees into lists	
for dt in dts:
    root = dt.getroot()
    atr=root.attrib
    name = atr["id"]
    names.append(name)
    seo = "None"
    x=0
    y=0
    z=0
    for child in root:
        if child.tag == 'seo_meta_description':
            seo = child.text
            x=1
            if seo == "":
                seo = "None"
            seos.append(seo)
        if child.tag == 'source_id':
            sid = child.text
            y=1
            if sid == "":
                sid = "None"
            srcids.append(sid)
        if child.tag == 'developer_name':
            dv_n = child.text
            z=1
            if dv_n == "":
                dv_n = "None"
            dv_ns.append(dv_n)
    if x == 0:
        seo = "None"
        seos.append(seo)
    if y == 0:
        sid = "None"
        srcids.append(sid)   
    if z == 0:
        dv_n = "None"
        dv_ns.append(dv_n)
l1 = []
#creating first column
for f in files:
    l1.append(f)
    l1.append(" ")
    l1.append(" ")
    l1.append(" ")
l2 = []
it=0
lenf = len(files)
#creating seconed column
for i in range(lenf):
    l2.append(names[it])
    l2.append(seos[it])
    l2.append(srcids[it])
    l2.append(dv_ns[it])    
    it = it+1
#creating and saving df to csv
df = pd.DataFrame(l2, index =l1,columns =['eDT'])
df.eDT.apply(str)
df['eDT'].fillna('None', inplace=True)
cwd = os.getcwd()
spath = os.path.join(cwd,'Explainers data.csv')
df.to_csv (spath, header=False)
files2 = [f for f in listdir('Video Transcripts') if isfile(join('Video Transcripts', f))]
trscs=[]
n2=0
#loading files
for f in files2:
    path = os.path.join('Video Transcripts',files2[n2])
    trscs.append(et.parse(path))
    n2 = n2+1
#setting column
lst = ["question id","media identifier","question title","question start-time","question end-time"]
nr=0
mr=0
#starting op
for tree in trscs:
    nr = nr+1
    troot = tree.getroot()
    tatr = troot.attrib
    idls=[]
    mr=0
    mids = []
    qts =[]
    tqts =[]
    itrtr=0
    flg = 0
    tgls = []
	#per file op
    for child in troot.iter():
        mr = mr +1	
        tgls.append(child.tag)
        if child.tag == 'question':
            flg = 1
            ch=child.attrib
            if 'id' in ch.keys():
                qid = ch['id']
                if qid == "":
                    qid = "None"
                idls.append(qid)
            else:
                idls.append("None")
            if 'media_identifier' in ch.keys():    
                mid = ch ['media_identifier']
                if mid == "":
                    mid = "None"
                mids.append(mid)
            else:
                mid = "None"
                mids.append(mid)
        if child.tag == 'question_title':
            qt = child.text
            tqts.append(qt)
            flg=0
        if flg==1: 
            tqts.append("None")
            flg=0            
        qts = tqts[1::2]
        if len(tqts)%2==1:
            qts.append(tqts[-1])   
    tgls_i=[]
    ntgls_i=[]
    st_ts=[]
    fn_ts=[]
    if 'question' in tgls:
        tgls_i = [i for i, e in enumerate(tgls) if e == 'question_seo_meta_description']   
    ntgls_i = [x+2 for x in tgls_i]
    for child in troot.iter():
        if itrtr in ntgls_i:
            ndchld=child.attrib
            if 'start_time' in ndchld.keys():
                st_t = ndchld['start_time']
                st_ts.append(st_t)
            if 'start_time' in ndchld.keys():
                fn_t = ndchld['end_time']
                fn_ts.append(fn_t)                
        itrtr=itrtr+1			
	#creating df
    dfl=len(ntgls_i)
    columnl = range(0, dfl)
    tdf = pd.DataFrame({lst[0]:idls , lst[1]:mids , lst[2]:qts , lst[3]:st_ts , lst[4]:fn_ts})
    df_t = tdf.T
	#naming files
    p_h=files2[nr-1]
    nme= str(p_h)+ '.csv'
    spath = os.path.join(cwd,nme)
    df_t.to_csv (spath, header=False)
#creating folder
spath = os.path.join(cwd,'Updated')
if not os.path.exists(spath):
    os.makedirs('Updated')
#determining API
sysn=platform.system()
src_gp = os.path.join(cwd,'Explainers')
dist_gp = spath
#copying files
if sysn == 'Windows':
    for f in files:
        src_p =src_gp+"\\"+str(f)
        dist_p =dist_gp+"\\"+str(f)
        wintxt = 'copy '+src_p+' '+dist_p
        status = subprocess.call(wintxt, shell=True)
else:
    for f in files:
        src_p =src_gp+"/"+str(f)
        dist_p =dist_gp+"/"+str(f)    
        untxt = 'cp '+src_p+' '+dist_p
        status = subprocess.call(untxt, shell=True)
#replacing tags		
for cf in files:
    cfn = dist_gp+"\\"+str(cf)
    f = open(cfn,'r', encoding="utf8")
    m0 = f.read()
    f.close()
    m1 = m0.replace("<p>","<p><s>")
    m2 = m1.replace("</p>","</s></p>")
    m3 = m2.replace("<td>","<td><s>")
    m4 = m3.replace("</td>","</s></td>")
    f = open(cfn,'w', encoding="utf8")
    f.write(m4)
    f.close()		