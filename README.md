# CoronaStats_on_AppEngine
Plotly and Django running together on GCP App Engine to illustrate COVID-19 statistics in Switzerland.  

I used Plotly library to create a graph of confirmed COVID-19 cases and deaths per canton in Switzerland after I pull data from an official source via its provided API. Afterwards I simply added the link for this application in one of my public entries on my Django based web blog.  

Output is something like below with a link to official data source embedded in each canton label:  
  
![alt text](https://github.com/karakurto/CoronaStats_on_AppEngine/blob/master/Capture.PNG?raw=true)

https://knowledge-journal.oa.r.appspot.com/public_topics/corona_stats_ch/

This graph uses 1 day old data because cantons upload their data at 18.00 during workdays. This also means that there will be less cantons in the graph if you generate a graph on Sundays or Mondays before 18.00.

You can learn more about application deployment to GCP App Engine here: https://github.com/karakurto/GCP-App-Engine-Standard
