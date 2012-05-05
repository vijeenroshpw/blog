from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
form = '''<form name="bform" method="post" action="/process">
		<center> 
		Title
		<input type="text" name="subject"><br/>
		
		Content:<br/>
		<textarea name="content" rows=20 cols=50></textarea><br/>
		<input type="submit" value="POST">
	        <div><font color="red">%(error)s</font></div>
		</center>          
	</form>
       '''

def escape_html(s):
	slist = list(s)
    
    	for i in range(0,len(slist)):
		if slist[i] == '"':
            		slist[i] = "&quot;"
        	elif slist[i] =="<":
            		slist[i] = "&lt;"
        	elif slist[i] == ">":
            		slist[i] = "&gt;"
        	elif slist[i] == "&":
            		slist[i] = "&amp;"
        	else :
            		pass
    	return "".join(slist)

# Database Model
class postings(db.Model):
	pid = db.IntegerProperty()	
	title = db.StringProperty()
	content = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add = True)

class new(webapp.RequestHandler):
	def write_form(self,error=""):
		return form%{"error":error}
	def get(self):
		self.response.out.write('''
			<html>
				<head>
					<title> New Blog Entry </title>
				</head>
				<body bgcolor="lightblue">
					<h2 align="center"> New Blog Post </h2>
				''' + self.write_form() + '''
				</body>
			</html>         ''')

class process(webapp.RequestHandler):
	def write_form(self,error = ""):
		return form%{"error":error}
	
	def post(self):
		subj = self.request.get("subject")
		cont = self.request.get("content")
		if not (subj and cont):
			self.response.out.write('''
			<html>
				<head>
					<title> New Blog Entry </title>
				</head>
				<body bgcolor="lightblue">
					<h2 align="center"> New Blog Post </h2>
				''' + self.write_form("Requires both Title and Content") + '''
				</body>
			</html>         ''')
		else:
			length = db.GqlQuery("select * from postings").count() + 1			
			postings(pid = length,title = subj,content = cont).put()     #tucks the data into database				
			self.redirect("/posts/"+str(length))
class ShowPost(webapp.RequestHandler):
	def get(self):
		postid = int(self.request.uri.split('/')[4])
		post = db.GqlQuery("select * from postings where pid = :1",postid)[0]
		self.response.out.write('''
			<html>
				<head>
					<title> Isolated Post View </title>
					<style type="text/css">
						body {
							margin-left:250px;
							width:800px;						
						}
					</style>				
				</head>
				<body bgcolor="lightblue">
					<h2 align = "center" > ''' + escape_html(post.title) + '''</h2><span id = 'time'>''' + str(post.date.year)+"-"+str(post.date.month) + "-"+str(post.date.day)+  '''</span><hr/><p>''' + escape_html(post.content) + '''</p> </body> </html>''')
 

class MainPage(webapp.RequestHandler):
	def get(self):
		posts = db.GqlQuery("select * from postings order by date desc")
		posts_html = ""
		for post in posts:
			posts_html = posts_html + "<font size='30px'>" + escape_html(post.title) + "</font><span class='time'>"+str(post.date.year)+"-"+str(post.date.month) + "-"+str(post.date.day) + "</span><hr/><p>" + escape_html(post.content) + "</p><br/><br/>"
		self.response.out.write(''' 
			<html>
				<head> 
					<title> Vijeens Technical Blog </title>
					<style type="text/css">
						.time {
							position:absolute;
							margin-top:30px;							
							left:900px;
						}
						body{
							margin-left:250px;
							width:750px;						
						}					
						#about {
							position:absolute;
							border:solid black 2px;
							margin-left:780px;
							width:300px;
							top:150px;
							height:450px;
						}					
					</style>				
				</head>
				<body bgcolor='lightblue'>
					<h1 align="center" > My Technical Blog </h1>
					<div id="about" > <h2 align="center"><u> About Me</u></h2> 
					<h4 align="center"> Vijeenrosh P.W </h4>
					<h4 align="center"> IRC Nickname : vijeenroshpw </h4>					
					<h4 align="center"> Govt. Engineering College Thrissur </h4>
					<h4> Interested in:</h4>
						<ul>
							<li> Mathematics </li>	
							<li> Programming </li>
							<li> Networking </li>
							<li> Hardware</li>
							<li> Machine Learning </li>
							<li> Web application Engineering </li>
						</ul>

					<center> <a href='http://www.github.com/vijeenroshpw'>My github</a><br/>
						 
					<a href='http://www.BlackJackVijeen.blogspot.com'> My Blogspot Blog </a><br/>
					 <a href='http://twitter.com/#!/VijeenroshPW' > Twitter Handle </a><br/>
					 <a href='http://www.facebook.com/vijeenrosh.vijeen' > Facebook Handle </a><br/></center> 
					</div>
					<br/>
				''' + posts_html + ''' 
				<br/><hr/>
				<font size="3px" > Developed by VIJEENROSH P.W , Govt.Engineering college Thrissur </font>				
				</body>
			</html> ''')

								
app = webapp.WSGIApplication([('/newpost',new),('/',MainPage),("/process",process),("/posts/.*",ShowPost)],debug=True)

def main():
	run_wsgi_app(app)

if __name__=="__main__":
	main()

