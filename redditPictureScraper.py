from bs4 import BeautifulSoup
import requests
import os

# gets website as user input
# url = input("Enter a website to extract the URL's from:")
r = requests.get("http://www.reddit.com/r/pics")
s = requests.get("http://www.reddit.com/r/humanporn")

# creates two soups of html from r/pics and r/humanporn
dataPics = r.text
dataHP = s.text
soupPics = BeautifulSoup(dataPics)
soupHP = BeautifulSoup(dataHP)

if os.path.isfile("top_pictures.txt"):
	with open('top_pictures.txt', 'w+') as textfile:

		# finds all elements needed to grab pictures
		rPicsLinks = soupPics.find_all('a', attrs={'class' : 'thumbnail'})
		rHpLinks = soupHP.find_all('a', attrs={'class' : 'thumbnail'})

		# finds top five pictures from r/Pics
		uvPics = soupPics.find_all('div', attrs={'class' : 'thing'})
		topFivePics = []
		for i in range(0, len(uvPics)):
			topFivePics.append(int(uvPics[i]['data-ups']) - int(uvPics[i]['data-downs']))

		topFivePics.sort()
		topFivePics.reverse()
		# trims list from end, down to the first five elements
		for i in range(len(topFivePics) - 1, 4, -1):
			del topFivePics[i]

		# finds top five pictures from r/humanporn
		uvHP = soupHP.find_all('div', attrs={'class' : 'thing'})
		topFiveHP = []
		for i in range(0, len(uvHP)):
			topFiveHP.append(int(uvHP[i]['data-ups']) - int(uvHP[i]['data-downs']))

		topFiveHP.sort()
		topFiveHP.reverse()
		# trims list from end, down to the first five elements
		for i in range(len(topFiveHP) - 1, 4, -1):
			del topFiveHP[i]

		textfile.write("Top 5 Pictures from reddit.com/r/pics: \n")

		# searches through the list of pics to grab the matching pic to each top upvote count
		for i in range(0, len(rPicsLinks)):
			for j in range(0, len(topFivePics)):
				if int(uvPics[i]['data-ups']) - int(uvPics[i]['data-downs']) == topFivePics[j]:
					# dumps pic link and upvote count into file
					textfile.write(str(j+1) + ') ')
					textfile.write(rPicsLinks[i].get('href')+'\n')
					textfile.write("    Upvotes: " + str(topFivePics[j]) + '\n')
					break

		textfile.write("\nTop 5 Pictures from reddit.com/r/humanporn: \n")

		# searches through the list of pics to grab the matching pic to each top upvote count
		for i in range(0, len(rHpLinks)):
			for j in range(0, len(topFiveHP)):
				if int(uvHP[i]['data-ups']) - int(uvHP[i]['data-downs']) == topFiveHP[j]:
					# dumps pic link and upvote count into file
					textfile.write(str(i+1) + ') ')
					textfile.write(rHpLinks[i].get('href')+'\n')
					textfile.write("    Upvotes: " + str(topFivePics[j]) + '\n')
					break

		# prints file contentsto console
		textfile.seek(0)
		for line in textfile:
			print(line)

## try to only get the ones with more than 2000 upvotes: