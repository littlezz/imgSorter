import os,operator,re,random
from PIL import Image

supportOrderBy=("proportion","width","height","random")


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
	makeView(imgInfo)

	putOutInfo.printOut(orderBy)



def autoGetInfo():
	# didn't use pickle
	#use re!
	

	def addInfo(filename,imgInfo):
		#check isdir
		if os.path.isdir(filename): return

		try:
			im=Image.open(filename)
		except IOError:
			print("Can not load {}".format(filename))
		else:
			width,height=im.size
			tmp={'name':filename,'width':width,'height':height,'proportion':width/height}
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
		tmpList=[]
		for i in imgInfo:
			tmpList.append(random.choice(imgInfo))
		return tmpList

	if orderBy=="random":
		return runRandomSort(imgInfo)
	else:
		return sorted(imgInfo,key=orderedKeyFunc)

def makeView(imgInfo):

	def openCssFloderFile(*arg):
		rt=[]
		for i in arg:
			with open('./imgSorter/date/temp/'+i,'r',encoding="utf-8") as f:
				rt.append(f.read())
		return rt



	header,tempOne,tempTwo=openCssFloderFile('header.html','tempOne.html','tempTwo.html')

	
	with open('viewOne.html','w',encoding="utf-8")as viewOne,open('viewTwo.html','w',encoding="utf-8") as viewTwo:

		#write header
		viewOne.write(header.format('imgSorter_One','one.css'))
		viewTwo.write(header.format('imgSorter_Two','two.css'))

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

if __name__=="__main__":
	main()