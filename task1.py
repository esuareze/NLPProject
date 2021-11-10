import requests
import pickle
from bs4 import BeautifulSoup

from time import sleep


printeau = False
def filter_search_results_box(tag):
	if(tag.has_attr('class')):
		return tag['class']==["search-result__xsl-body","items-results","rlist--inline"]
	else:
		return False
def filter_search_results_from_box(tag):
	if tag.name == "li":
		if(tag.has_attr('class')):
			return tag['class']==["search__item","issue-item-container"]
	return False
def filter_search_result_num(tag):
	if tag.name == 'span':
		if(tag.has_attr('class')):
			return tag['class']==["hitsLength",]
	return False
def filter_link_span(tag):
	if tag.name == 'span':
		if(tag.has_attr('class')):
			return tag['class']==["hlFld-Title",] or tag['class']==["hlFld-ContentGroupTitle",]
		
	return False
def get_num_results_and_30_links(bs):
	global printeau
	num_results = bs.find(filter_search_result_num).text.replace(" ","").replace(",","")
	results_box = bs.find_all(filter_search_results_box).pop()
	results = results_box.find_all(filter_search_results_from_box)[:30]
	links = []
	for r in results:
		link_span = r.find(filter_link_span)
		if link_span is not None:
			link = "https://dl.acm.org"+link_span.find('a')['href']
			links.append(link)
		elif not printeau:
			printeau = True
			f = open("lmaoekisde","w")
			print(r, file = f)
			f.close()
	print(f"lenaasdf  {len(links)}")
	return num_results, links
def filter_abstract_div(tag):
	if tag.name == 'div':
		if(tag.has_attr('class')):
			return tag['class']==["abstractSection","abstractInFull"] or tag['class'] == ["abstractSection"]
	return False
def get_abstract(bs):
	global currentLink
	abstract_div = bs.find(filter_abstract_div)
	if abstract_div is None:
		print(currentLink)
		return ""
	return abstract_div.find('p').text
def get_title(bs):
	global currentLink
	title_h1 = bs.find(filter_article_title)
	if title_h1 is None:
		title_div = bs.find(filter_article_title_other)
		if title_div is None:
			print(currentLink)
		return title_div.find('span').text
	else:
		return title_h1.text
		
def filter_article_title(tag):
	if tag.name == 'h1':
		if(tag.has_attr('class')):
			if tag['class']==["citation__title",]:
				return True
	return False
def filter_article_title_other(tag):
	if tag.name == 'div':
		if(tag.has_attr('class')):
			if tag['class']==["left-bordered-title",]:
				return True
	return False
def filter_author_tag(tag):
	if tag.name == 'div':
		if(tag.has_attr('class')):
			return tag['class']==["tags-widget__content"]
	return False
	
def get_author_tags(bs):
	author_tag_div = bs.find(filter_author_tag)
	if author_tag_div is None:
		return []
	author_tag_list = author_tag_div.find('ul')
	tags = author_tag_list.find_all('li')
	tag_texts = []
	for t in tags:
		tag_texts.append(t.find('a').text)
	return tag_texts
def filter_tree(tag):
	if tag.name == 'div':
		if(tag.has_attr('class')):
			return tag['class']==["citation", "article__section", "article__index-terms"]
	return False
def get_ccs_classes(bs):
	tree_div = bs.find(filter_tree)

	if tree_div is not None:
		result = []
		temp = tree_div.find('ol')
		if temp is None:
			return []
		ol = temp.find('li').find('ol')

		lis = ol.find_all('li')
		if lis is None:
			return []
		for li in lis:
			result.append(li.find('div').find('p').find('a').text)

		return result
	else:
		return []
currentLink = ""
def main():
	global currentLink
	afterMonth = 12
	beforeMonth = 1
	afterYear = 2019
	beforeYear = 2020
	nums_results = []
	monthInd = 0
	articlesData = []
	while monthInd<=6:
		with open(f"month{monthInd}m{afterMonth}y{afterYear}","rb") as fh:
			monthList = pickle.load(fh)
		articlesData+=monthList
		print(f"mes {monthInd} importado")
		afterMonth=beforeMonth
		afterYear=beforeYear
		beforeMonth+=1
		if beforeMonth == 13:
			beforeMonth = 1
			beforeYear+=1
		monthInd+=1
	while (beforeMonth<=10 or beforeYear<2021):
		url = f"https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&text1=COVID-19&AfterMonth={afterMonth}&AfterYear={afterYear}&BeforeMonth={beforeMonth}&BeforeYear={beforeYear}&startPage=0&pageSize=50"

		request = requests.get(url)
		monthlyList = []
		html = request.text
		bs = BeautifulSoup(html, features = 'html.parser')
		num_results, result_links = get_num_results_and_30_links(bs)
		nums_results.append(num_results)
		
		for link in result_links:
			request = requests.get(link)
			
			currentLink = link
			linkbs = BeautifulSoup(request.text, features = 'html.parser')
			article_dict = {}
			article_dict['monthInd'] = monthInd
			article_dict['title'] = get_title(linkbs)
			article_dict['abstract'] = get_abstract(linkbs)
			article_dict['authorTags'] = get_author_tags(linkbs)
			article_dict['ccsClass'] = get_ccs_classes(linkbs)

			articlesData.append(article_dict)
			monthlyList.append(article_dict)
			sleep(30)
		with open(f"month{monthInd}m{afterMonth}y{afterYear}","wb") as fh:
			pickle.dump(monthlyList, fh)
		print(f"mes {monthInd} terminado")
		afterMonth=beforeMonth
		afterYear=beforeYear
		beforeMonth+=1
		if beforeMonth == 13:
			beforeMonth = 1
			beforeYear+=1
		monthInd+=1
		
	with open('articlesData.data', 'wb') as fh:
		pickle.dump(articlesData, fh)
	with open('QuickData/num_results', 'w') as f:
		printable_num_results = ",".join(nums_results)
		print(printable_nums_results, file=f)
if __name__ == '__main__':
	main()