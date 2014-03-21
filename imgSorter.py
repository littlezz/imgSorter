import os,operator,re,random
from PIL import Image

supportOrderBy=("proportion","width","height","random")

part_html_path=os.path.join(os.getcwd(),"date","html","")
print(part_html_path)
css_path=os.path.join(os.getcwd(),"date","css","")

divNumber=50

class programInfo():
	"""print info of program running"""
	def __init__(self):
		self.count=0
		self.info=[
				"There is total {} files",
				"sorting",
				"making html.",
				"done! with {} mode"
				]
	def printOut(self,info=None):
		print(self.info[self.count].format(info))
		self.count +=1

def main():
	if os.path.exists(part_html_path)==False:
		os.mkdir(part_html_path)
	path=".."
	os.chdir(path)
	orderBy="proportion"
	while True:

		if isRandomMode(orderBy):
			userWantValue=None
			break

		userInput=getInput(orderBy)
		if userInput:
			if userInput[0]=="#":
				if userInput[1:].rstrip() in supportOrderBy:
					orderBy= userInput[1:].rstrip()
				else : 
					print("Can not order by {}".format(userInput))
			else:
				try:
					userWantValue=float(userInput.rstrip())
				except ValueError:
					print("Can not use {}".format(userInput))
				else :
					break;


	putOutInfo=programInfo()

	imgInfo=autoGetInfo()
	putOutInfo.printOut(len(imgInfo))

	putOutInfo.printOut()
	imgInfo=ordered(imgInfo,orderBy,userWantValue)

	putOutInfo.printOut()


	#makeView(imgInfo)
	#make div html,50 pictures in a part_html
	header,tempOne,tempTwo,tempLink=openCssFloderFile('header.html','tempOne.html','tempTwo.html','tempLink.html')
	
	for i in range(int(len(imgInfo)/divNumber)+1):
		makeView(imgInfo[i*divNumber:(i+1)*divNumber],i,part_html_path,tempOne,tempTwo,header,tempLink)

	putOutInfo.printOut(orderBy)
	makeLinkToHtmlPart()
	

def makeLinkToHtmlPart():
	
	viewOneHtmlGoalPath=os.path.join(part_html_path,"viewOne_part0.html")
	viewTwoHtmlGoalPath=os.path.join(part_html_path,"viewTwo_part0.html")
	
	if not os.path.exists("viewOne.html"):
		os.symlink(viewOneHtmlGoalPath,"viewOne.html")

	if not os.path.exists("viewTwo.html"):
		os.symlink(viewTwoHtmlGoalPath,"viewTwo.html")
	

def autoGetInfo():
	# didn't use pickle
	#use re!
	

	def addInfo(filename,imgInfo):
		#check isdir
		if os.path.isdir(filename): return
		pwd=os.getcwd()
		try:
			im=Image.open(filename)
		except IOError:
			print("Can not load {}".format(filename))
		else:
			width,height=im.size
			tmp={'name':os.path.join(pwd,filename),'width':width,'height':height,'proportion':width/height}
			imgInfo.append(tmp)	


	imgInfo=[]
	with open('./imgSorter/date/matchRule/matchRule.txt','r',encoding="utf-8")as f:
		content=f.read()
		if content:
			matchRule=re.compile(content)
		else:
			matchRule=None

	
	for i in os.listdir():
		if (not matchRule) or (re.match(matchRule,i)):
			addInfo(i,imgInfo)

	return imgInfo
	


def ordered(imgInfo,orderBy,userWantValue):

	def orderedKeyFunc(u):
		return abs(u[orderBy]-userWantValue)

	def runRandomSort(imgInfo):
		tmpList=imgInfo[:]
		random.shuffle(tmpList)
		return tmpList

	if orderBy=="random":
		return runRandomSort(imgInfo)
	else:
		return sorted(imgInfo,key=orderedKeyFunc)

def makeView(imgInfo,part,directory,tempOne,tempTwo,header,tempLink):

	


	if imgInfo==None: return

	
	with open(directory+'viewOne_part{}.html'.format(part),'w',encoding="utf-8")as viewOne,open(directory+'viewTwo_part{}.html'.format(part),'w',encoding="utf-8") as viewTwo:

		#write header
		viewOne.write(header.format('imgSorter_One',css_path+'one.css'))
		viewTwo.write(header.format('imgSorter_Two',css_path+'two.css'))

		for i in range(len(imgInfo)):
			#write viewOne
			viewOne.write(tempOne.format(imgInfo[i]['name'],
										imgInfo[i]['name'],
										i,
										i)
			)

			#write viewTwo
			if i%2==1:
				viewTwo.write(tempTwo.format(
											imgInfo[i-1]['name'],
											imgInfo[i-1]['name'],
											imgInfo[i]['name'],
											imgInfo[i]['name'],
											i,
											i,
											)
					)
		#deal with len(imgInfo) is odd
		if len(imgInfo)%2==1:
			viewTwo.write(tempTwo.format(
											imgInfo[-1]['name'],
											imgInfo[-1]['name'],
											'',
											'',
											i,
											i,
											)
					)

	
		#write prev_next link  /body /html 
		for i,name in ((viewOne,"viewOne"),(viewTwo,"viewTwo")):
			if part==0:
				i.write(tempLink.format(name,part,name,part+1))
			else: 
				i.write(tempLink.format(name,part-1,name,part+1))
			i.write("</body></html>")

#makeView end 




def getInput(orderBy):
	 print('Please enter the {} value you want.(number!)'.format(orderBy))
	 print("such as 1.7 (16:9)")
	 return input()

def isRandomMode(orderBy):
	if orderBy=="random":
		return True
	else :
		return False

def openCssFloderFile(*arg):
		rt=[]
		for i in arg:
			with open('./imgSorter/date/temp/'+i,'r',encoding="utf-8") as f:
				rt.append(f.read())
		return rt

if __name__=="__main__":
	main()