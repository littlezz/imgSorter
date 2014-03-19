import os,operator,re
from PIL import Image

supportOrderBy=("proportion","width","height")

def main():
	path=".."
	os.chdir(path)
	orderBy="proportion"
	while True:
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


	
	imgInfo=autoGetInfo()

	imgInfo=ordered(imgInfo,orderBy,userWantValue)

	makeView(imgInfo)

	with open('log.txt','w') as f:
		for i in imgInfo:
			f.write(str(i))


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
	return input('Please enter the {} value you want.\n'.format(orderBy))


if __name__=="__main__":
	main()