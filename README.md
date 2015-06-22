# fcb-collector [unfinished]
Various tools for retrieving user data from Facebook. Unfortunatelly this is another unfinished project which I have abondoned and still has to finish.

### Motivation:
There was a time when I wanted to retrieve all information about all users from a certain Facebook group and possibly ASAP. So I decided to create a tool which would somehow scrap this information and create a html page with concise user information so it can be browsed in convenient way.

### Implementation:
As with other simple tools, I chose **Python** as a language of choice and  began first with implementing the whole stuff using [requests ](http://docs.python-requests.org/) library (loging to Facebook etc...) which was pretty complex and time consuming. 
Shortly after that I decided to use Facebook [Graph API] (https://developers.facebook.com/docs/graph-api) which looked at the beginning awesome (once I found a way how to easily get session token) but I soon found out that there is a limit for a number of results one can get from the API (500 for group members) which didn't suffice when I needed to list all members from a group which has 11K+ members.
The third attempt involved [Selenium](http://www.seleniumhq.org/) and browser automation. It played along nicely until I foudn out that  Facebook is monitoring the requests and if it finds too many request or suspicious behaviour the user will be banned (temporarily). As I didn't have time at that time I stopped trying and let the work unfinished.
