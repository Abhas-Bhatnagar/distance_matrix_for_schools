import time
import selenium
import os
import pymysql
from selenium import webdriver
driver=selenium.webdriver.Chrome()
driver.get("https://photos.google.com/people")
elem=driver.find_element_by_id("identifierId")
elem.send_keys("xxx@gmail.com")

driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
time.sleep(2)
elem=driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
elem.send_keys("password")
time.sleep(2)
driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
time.sleep(10)
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='photo_db')
cur = conn.cursor()
sql = "SELECT * FROM `details`"
cur.execute(sql)
result=cur.fetchall()
try:
	for row in result:
		prev_count=int(row[2])
		link=row[3]
		name=row[1]
		idnum=row[0]
		driver.get("https://photos.google.com/search/"+link)
		#ime.sleep(4)
		data=driver.page_source
		data=str(data.encode('utf-8'))
		f = open("C:/Users/Abhas/Desktop/"+str(row[0])+".html",'w')
		f.write(data)
		#time.sleep(2)
		a=',[27,false,true]'
		new_count=data.count(a)
		f.close()
		#print(prev_count)
		#print(new_count)
		print(idnum)
		if int(new_count)>int(prev_count):
			#print ("found1 "+ name)
			sql="""UPDATE details SET count=%s where id=%s"""
			#print(sql)
			cur.execute(sql,(new_count,idnum))
			conn.commit()
			print("found "+ name),
except:
    cur.execute('show profiles')
    exit()
			
finally:
	cur.close()
	conn.close()