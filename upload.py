#!/usr/bin/python3 -u
# '-u' is unbuffered output: https://stackoverflow.com/a/18709945/1429450

import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

if len(sys.argv) != 4:
    print("""3 args required:
    relative path of directory of
            (1) files to upload
            (2) uploaded files
            (3) rejected files""")
    sys.exit(1)

upload_dir = os.getcwd()+'/'+sys.argv[1]+'/'
uploaded_dir = os.getcwd()+'/'+sys.argv[2]+'/'
rejects_dir = os.getcwd()+'/'+sys.argv[3]+'/'

print("Specified directories:")
for i in [upload_dir, uploaded_dir, rejects_dir]:
    print(i)
    if not os.path.isdir(i):
        os.mkdir(i)
print()

def login():
    global driver
    driver = webdriver.Firefox()
    print("Logging in. ", end='')
    driver.get('http://libgen.lc/librarian.php')

    driver.add_cookie({'name':'phpbb3_9na6l_u', 'value':'1602'})
    driver.add_cookie({'name':'phpbb3_9na6l_k', 'value':'ut23g0s85weg7k5z'})
    driver.add_cookie({'name':'phpbb3_9na6l_sid', 'value':'e2d3381ffb8118e1ecb23db6ea2eefee'})

    driver.find_element_by_link_text('Login').click()
    print("Logged in.")
    driver.get('http://libgen.lc/librarian.php')

def sortKey(filename):
    return os.path.getsize(upload_dir+filename)

files = os.listdir(upload_dir)
files = sorted(files, key=sortKey) #ascending sort by size: https://stackoverflow.com/a/20253803/1429450
if len(files) == 0:
    print("No books to upload.")
    exit()

login()
for f in files:
    driver.get('http://libgen.lc/librarian.php')
    print('\nUploading: '+f)
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="pre_l"]').click()
            break
        except:
            driver.quit()
            login()
            continue
    file_input = driver.find_element_by_id('addfiletoeditionfile')
    file_input.send_keys(upload_dir + f)
    driver.find_element_by_id('upload-file').click()
    # Wait for page to load. 
    # courtesy: 𝘗𝘺𝘵𝘩𝘰𝘯 𝘛𝘦𝘴𝘵𝘪𝘯𝘨 𝘸𝘪𝘵𝘩 𝘚𝘦𝘭𝘦𝘯𝘪𝘶𝘮 EPUB ref:11.25
    # Files that take >1h skipped:
    try:
        WebDriverWait(driver,3600).until(EC.staleness_of(driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/h2/button')))
    except TimeoutException:
        print('Upload timedout. Continuing.')
        continue
    except:
        pass

    # if in DB
    try:
        print('Checking if already in DB.\t', end='')
        WebDriverWait(driver,1).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Such a file is already in database.")))
        print('Yes. Moving to uploaded dir.')
        os.rename(upload_dir+f, uploaded_dir+f)
        continue
    except TimeoutException:
        print('File not already in DB.')

    # if Bad Gateway
    try:
        print('Checking for presence of Bad Gateway.\t', end='')
        WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, "html body center h1")))
        print('Bad Gateway found. Continuing.')
        continue
    except TimeoutException:
        print('Bad Gateway not found.')

    # if ∃ title field
    try:
        print('Checking for presence of title field.\t', end='')
        title_field = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.ID, "title")))
        print('∃ title field.')
    except TimeoutException:
        print('Title field not found. Moving to rejects dir.')
        os.rename(upload_dir+f, rejects_dir+f)
        continue

    print("Entering data.")
    s = re.split(' - ', f)
    #update title field
    title_field = driver.find_element_by_id("title")
    title_field.send_keys(s[0])
    #update author field
    author = os.path.splitext(s[1])[0]
    author = re.sub(r'_$', '.', author)
    author_field = driver.find_element_by_id('author')
    author_field.clear()
    author_field.send_keys(author)
    # courtesy: 𝘗𝘺𝘵𝘩𝘰𝘯 𝘛𝘦𝘴𝘵𝘪𝘯𝘨 𝘸𝘪𝘵𝘩 𝘚𝘦𝘭𝘦𝘯𝘪𝘶𝘮 EPUB ref:7.60
    type_selector = driver.find_element_by_xpath('//*[@id="type"]')
    select_list=Select(type_selector)
    select_list.select_by_visible_text('book')
    #Register!
    driver.find_element_by_xpath('/html/body/div[2]/button').click()
    os.rename(upload_dir+f, uploaded_dir+f)

print('Driver quitting…', end='')
driver.quit()

