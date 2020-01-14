import urllib.request as req
from bs4 import BeautifulSoup as bs
import re
import csv


def get_bsobj(url):
	res = req.urlopen(url) #get access to the website
	html = res.read().decode('utf-8')
	return bs(html, 'html.parser')  #return the bsobj

def get_salary_raw(year):
	web_url = r"https://hoopshype.com/salaries/players/{0}-{1}".format(year, year+1)
	soup = get_bsobj(web_url)
	table_rows = soup.find_all('tr')

	lst = []
	i = 0
	for row in table_rows[1:]:
		name_raw = row.find('a').string
		salary_raw = row.find_all('td')[2].string
		lst.append([name_raw, salary_raw])
	return lst

def regulate_lst(raw_lst):
	for el in raw_lst:
		el[0] = re.search(r"[a-zA-Z '-\.]+", el[0]).group()
		el[1] = re.search(r'[0-9,]+', el[1]).group().replace(",","")
def get_salary(year):
	lst = get_salary_raw(year)
	regulate_lst(lst)
	return lst

def create_csv(path=r"E:\python\bs4\nba_salary.csv", head = ['year', 'player', 'salary']):
	with open(path,'w', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(head)

def write_csv(lst, year):
	path = r"E:\python\bs4\nba_salary.csv"
	with open(path,'a+', encoding='utf-8', newline='') as f:
		writer = csv.writer(f)
		for row in lst:
			writer.writerow([year] + row)

def _main(years):
	#1990-2019
	if not years:
		print("success!")
		return
	year_error =[]
	for year in years:
		print("year({0})".format(year))
		try:
			lst = get_salary(year)
			write_csv(lst,year)
		except Exception as e:
			print("year({}):error")
			year_error.append(year)
	_main(year_error)








