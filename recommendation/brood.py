print('brood is go!')

import time
import pandas as pd
import math
import re
from sklearn.feature_extraction.text import CountVectorizer
from firebase import firebase
pd.options.display.max_rows = 9999
pd.options.display.max_columns = 200
start_time = time.time()

username = ""

def call_me(usern):
	username = usern 

	firebase = firebase.FirebaseApplication('https://brood-dubhacks-16.firebaseio.com/', None)

	users = firebase.get('/twitter', None)
	usertweets = {}
	for user in users.keys():
	    tweets = firebase.get('/tags/' + users[user], None)
	    for key in tweets.keys():
	            tag = tweets[key]   
	    usertweets[user] = tag





	usr = list(usertweets.keys())
	twt = list(usertweets.values())
	len(twt)

	eggs = pd.DataFrame({'Tweet_Tag': twt, 'User': usr})
	#eggs = eggs[~eggs.User.isin(['@narendramodi', '@SushmaSwaraj', '@ArvindKejriwal'])]
	eggs





	# Collaborative Filtering 

	# Creating dataframe of users against the tags they like
	vectorizer = CountVectorizer(min_df=0)

	print('Total users considered are : ' + str(len(usr)))
	vectorizer.fit(twt)
	arr = vectorizer.transform(twt)
	arr = arr.toarray()

	tag = vectorizer.get_feature_names()
	egg = pd.DataFrame(index=range(len(usr)), columns=tag, data=arr, dtype=int)
	egg.insert(0, 'user', usr)
	egg_orig = egg.copy()

	#Dropping the tags which have been associated by only a single user
	for i in range(int(len(egg_orig.columns))-1):
	    if sum(egg_orig.ix[:,i+1]) == max(egg_orig.ix[:,i+1]):
	        egg.drop(egg_orig.columns[i+1],1, inplace=True)

	egg






	# Create dataframe and store cosine scores for merchants

	tag_mtx = egg.drop('user', 1)
	tag_affinity = pd.DataFrame(index=tag_mtx.columns,columns=tag_mtx.columns,dtype=int)

	# Fillin in the empty spaces with cosine similarities
	# Loop through the columns
	from scipy.spatial.distance import cosine
	for i in range(0,len(tag_affinity.columns)):
	    # Loop through the columns for each column
	    for j in range(0,len(tag_affinity.columns)):
	        # Fill in placeholder with cosine similarities
	        tag_affinity.ix[i,j] = 1-cosine(tag_mtx.ix[:,i],tag_mtx.ix[:,j])
	tag_affinity.head(10)






	# Create placeholder tags for closest neighbours to an tag
	tag_neighbours = pd.DataFrame(index=tag_affinity.columns,columns=range(1,6))
	tag_neighbourv = pd.DataFrame(index=tag_affinity.columns,columns=range(1,6))

	# Loop through our similarity dataframe and fill in neighbouring item tag
	for i in range(len(tag_affinity.columns)):
	    tag_neighbours.ix[i,:5] = tag_affinity.ix[0:,i].sort_values(ascending=False)[:5].index
	    tag_neighbourv.ix[i,:5] = tag_affinity.ix[0:,i].sort_values(ascending=False)[:5
	        ].index + " (" + ['%.2f' % elem for elem in list(tag_affinity.ix[0:,i].sort_values(ascending=False)[:5])] + ")"
	    
	tag_neighbourv.head(10)






	# Content Filtering
	bro = egg.transpose()
	bro.columns = list(bro.ix[0][:])
	bro = bro.drop(bro.index[0])

	bro.head(10)





	# Create dataframe and store cosine scores for merchants
	usr_mtx = bro
	usr_affinity = pd.DataFrame(index=usr_mtx.columns,columns=usr_mtx.columns,dtype=int)

	# Fillin in the empty spaces with cosine similarities
	# Loop through the columns
	from scipy.spatial.distance import cosine
	for i in range(0,len(usr_affinity.columns)):
	    # Loop through the columns for each column
	    for j in range(0,len(usr_affinity.columns)):
	        # Fill in placeholder with cosine similarities
	        usr_affinity.ix[i,j] = 1-cosine(usr_mtx.ix[:,i],usr_mtx.ix[:,j])
	usr_affinity






	# Create placeholder item for closest neighbours to other users
	usr_neighbours = pd.DataFrame(index=usr_affinity.columns,columns=range(0,6))
	usr_neighbourv = pd.DataFrame(index=usr_affinity.columns,columns=range(0,6))

	# Loop through our similarity dataframe and fill in neighbouring item names
	for i in range(len(usr_affinity.columns)):
	    usr_neighbourv.ix[i,:6] = usr_affinity.ix[0:,i].sort_values(ascending=False)[:6
	        ].index + " (" + ['%.2f' % elem for elem in list(usr_affinity.ix[0:,i].sort_values(ascending=False)[:6])] + ")"
	    
	usr_neighbourv.drop(0, 1, inplace=True)

	# Putting in the format required for visualization
	nm_vl = list(usr_neighbourv.ix[username,:])
	nm_vl = [x.split() for x in nm_vl]
	nm_vl = pd.DataFrame(nm_vl, columns=['user', 'value'])
	nm_vl['value'].replace(to_replace = re.compile('[()]'), value='', inplace=True, regex=True)
	nm_vl.to_csv('bro.csv', index=False)





	# Function to calculate collaborative similarity
	def getScore(history, similarities):
	   return sum(history*similarities)/sum(similarities)





	# Create a place holder matrix for similarities, and fill in the user name column
	tag_lnk = pd.DataFrame(index=egg.index,columns=egg.columns)
	tag_lnk.ix[:,:1] = egg.ix[:,:1]





	#Loop through all rows, skip the user column, and fill with similarity scores
	for i in range(0,len(tag_lnk.index)):
	    for j in range(1,len(tag_lnk.columns)):
	        user = tag_lnk.index[i]
	        tags = tag_lnk.columns[j]
	 
	        if egg.ix[i][j] > 0:
	            tag_lnk.ix[i][j] = 0
	        else:
	            tag_top_nam = tag_neighbours.ix[tags][1:5]
	            tag_top_sim = tag_affinity.ix[tags].sort_values(ascending=False)[1:5]
	            tag_usr_usg = tag_mtx.ix[user,tag_top_nam]
	            
	            tag_lnk.ix[i][j] = getScore(tag_usr_usg,tag_top_sim)






	# Create Dataframe for top 6 tags
	tags_rcmd = pd.DataFrame(index=tag_lnk.index, columns=['user','1','2','3','4','5','6'])
	tags_rcmd.ix[0:,0] = tag_lnk.ix[:,0]

	# Substituting tag names
	for i in range(len(tag_lnk.index)):
	    srtd = tag_lnk.ix[i,1:].sort_values(ascending=False).ix[0:6,]
	    tg = srtd.index.transpose() + ' ('
	    vl = ['%.2f' % elem + ')' for elem in srtd.values.transpose()]
	    tags_rcmd.ix[i,1:] = [x + y for x, y in zip(tg, vl)]

	    
	# Putting in the format required for visualization
	tg_vl = list(tags_rcmd.ix[0])
	tg_vl = [x.split() for x in tg_vl]
	tg_vl = pd.DataFrame(tg_vl, columns=['user', 'value'])
	tg_vl['value'].replace(to_replace = re.compile('[()]'), value='', inplace=True, regex=True)
	tg_vl.drop(tg_vl.index[[0]], inplace=True)
	tg_vl.to_csv('tag.csv', index=False)




	print("Brood Creation: Time taken: " + str(round(time.time() - start_time,2)) + " seconds")



	import webbrowser
	import os

	dashboard_page = 'frontend.html'

	url = 'file://'+os.getcwd()+'/'+dashboard_page
	# Open URL in a new tab, if a browser window is already open.
	webbrowser.open_new_tab(url)

	# Open URL in new window, raising the window if possible.
	webbrowser.open_new(url)
