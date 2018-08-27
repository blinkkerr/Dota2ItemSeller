from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

# Steam credentials
username = 'USERNNAME'
password = 'PASSWORD'
steamID = 'STEAMID'

# Path to browser's driver
driver = webdriver.Firefox(executable_path=r'PATH TO DRIVER')
driver.get('https://steamcommunity.com/login/home/?goto=')
usernameField = driver.find_element_by_xpath('//*[@id="steamAccountName"]')
usernameField.send_keys(username)
passwordField = driver.find_element_by_xpath('//*[@id="steamPassword"]')
passwordField.send_keys(password)
time.sleep(3)
signInBtn = driver.find_element_by_xpath('//*[@id="SteamLogin"]')
signInBtn.click()

twoFactor = input("Enter 2 factor authentication code: ")
twoFactorField = driver.find_element_by_xpath('//*[@id="twofactorcode_entry"]')
twoFactorField.send_keys(twoFactor)
twoFactorField.send_keys(Keys.ENTER)

time.sleep(15)
driver.get(driver.current_url + '/inventory/#570')
time.sleep(3)
driver.find_element_by_xpath('//*[@id="filter_tag_show"]').click()
time.sleep(3)

driver.find_element_by_xpath('//*[@id="tag_filter_570_2_misc_marketable"]').click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
time.sleep(0.2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(0.2)
driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/4);")
time.sleep(0.2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(0.2)
time.sleep(10)

lastPage = int(driver.find_element_by_xpath('//*[@id="pagecontrol_max"]').text)
checked = False

counter = 0
for page in range(1, lastPage + 1):
	itemNo = 1
	while True:
		try:
			if driver.find_element_by_xpath('//*[@id="inventory_%d_570_2"]/div[%d]/div[%d]'%(steamID, page, itemNo)).get_attribute('style') != 'display: none;':
				driver.find_element_by_xpath('//*[@id="inventory_%d_570_2"]/div[%d]/div[%d]'%(steamID, page, itemNo)).find_elements_by_tag_name('div')[0].click()
				time.sleep(1)
				
				try:
					price = driver.find_element_by_xpath('//*[@id="iteminfo%d_item_market_actions"]/div/div[2]'%(counter)).text.split(' ')[2].split('\n')[0][2:]
					driver.find_element_by_xpath('//*[@id="iteminfo%d_item_market_actions"]/a/span[2]'%(counter)).click()
					time.sleep(0.5)
					driver.find_element_by_xpath('//*[@id="market_sell_buyercurrency_input"]').send_keys(price)
					if not checked:
						driver.find_element_by_xpath('//*[@id="market_sell_dialog_accept_ssa"]').click()
						checked = True
					driver.find_element_by_xpath('//*[@id="market_sell_dialog_accept"]/span').click()
					time.sleep(0.5)
					driver.find_element_by_xpath('//*[@id="market_sell_dialog_ok"]/span').click()
					time.sleep(3)
					driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/div[2]/div/span').click()
				except Exception as e:
					print (e)
					pass
				counter = abs(counter - 1)
			itemNo += 1
			
		except Exception as e:
			print (e)
			break
	if page != lastPage:
		driver.find_element_by_xpath('//*[@id="pagebtn_next"]').click()
		time.sleep(3)
