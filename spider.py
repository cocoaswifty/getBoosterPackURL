# -*- coding: utf-8 -*-
import mechanize
import scrapy

current_count = 0

def get_html(url):
	br = mechanize.Browser()  # 建立 Browser 物件
	br.set_handle_robots(False)  # 不理會網站的 robots.txt

	# 打開一些除錯用的設定，幫忙在開發過程中 debug：
	br.set_debug_http(True)
	br.set_debug_responses(True)
	br.set_debug_redirects(True)

	# Add User-Agent 代理設定
	br.addheaders = [("User-Agent",
	                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")]

	# Browse to login page  執行 open() 可以瀏覽一個 URL，回傳值是一個 response 物件
	# 不過不特別接回傳值也沒關係，可以用 br.response() 拿到同樣的 response 物件：
	br.open(url)
	return br.response().get_data()


def print_progress(max_count):
	rate = 0.5	#rate of the progress bar, controls the length of the progress bar
	global current_count
	current_count += 1
	progress = int((current_count/float(max_count))*100)

	i = 0
	j = 0
	complete_array = ''
	undone_array = ''

	while i < progress*rate:
		i += 1
		complete_array+='█'

	while j < (100-progress)*rate:
		j += 1

		undone_array+=' '

	print 'progress: {}%'.format(progress)+'|'+complete_array+undone_array+'|'




datas = [line.strip() for line in open("gamePageURL", 'r')]

for url in datas:
	print_progress(len(datas))

	web_file = get_html(url)

	text_file = open('temp', "w")
	text_file.write(web_file)
	text_file.close()

	web_file_response = scrapy.Selector(text=web_file)  # str轉成response

	tables = web_file_response.xpath('//*[@id="content-area"]/div/div[6]/div[2]/div[1]/div/a')  # 抓取每一個表格

	url_list = tables[0].xpath('@href').extract()

	string = url_list[0].encode('ascii','ignore')

	text_file = open('boosterPackURL', "a")
	text_file.write(string + '\n')
	text_file.close()

