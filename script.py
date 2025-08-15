import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_person(drv):
    person = {}
    person['name'] = drv.find_element(By.XPATH, '//section[@data-sentry-component="TeamMembers"]/article/div/hgroup/h3').text
    person['job'] = drv.find_element(By.XPATH, '//section[@data-sentry-component="TeamMembers"]/article/div/hgroup/span').text
    return person

driver = webdriver.Firefox()
time.sleep(5)
baseurl = 'https://www.partyslate.com'

urls = []
for i in range(1, 6):
    driver.get(f"{baseurl}/find-vendors/event-planner/area/miami?page={i}")
    time.sleep(10)
    for c in driver.find_elements(By.XPATH, '//h3[contains(@class, "Header-Header-module__title")]/a'):
        urls.append(c.get_attribute('href'))

#with open('companies.txt', 'w', encoding='UTF-8') as f:
#    for a in urls:
#        f.write(f"{a}\n")

#with open('companies.txt', 'r', encoding='UTF-8') as f:
#    for a in f.readlines():
#        urls.append(a.strip())

companies = []
for u in urls[:]:
    company = {'url': u}
    driver.get(u)
    time.sleep(5)
    company['title'] = driver.find_element(By.XPATH, '//h1[@data-sentry-element="Heading"]').text
    print(company['title'])
    contacts = driver.find_elements(By.XPATH, '//section[@data-sentry-component="ContactDetails"]//a')
    if len(contacts) > 0:
        company['site'] = contacts[-1].get_attribute('href').split('target=')[-1].replace('%2F', '/').replace('%3A', ':')
        media = []
        for m in contacts[:-1]:
            media.append(m.get_attribute('href'))
        company['media'] = media
    else:
        company['site'] = ''
        company['media'] = []
    team = []    
    if len(driver.find_elements(By.XPATH, '//section[@data-sentry-component="TeamMembers"]')) > 0:
        team.append(get_person(driver))
        pages = driver.find_elements(By.XPATH, '//div[@data-sentry-component="renderPagination"]/span')
        if len(pages) > 0:
            button = driver.find_element(By.XPATH, '//section[@data-sentry-component="TeamMembers"]/div/div/div/button[2]')
            for i in range(1, int(pages[0].text.split('/')[-1])):
                print(f'...person {i+1}')
                button.click()
                time.sleep(1)
                team.append(get_person(driver))
    company['team'] = team
    companies.append(company)

with open('companies.csv', 'a', encoding='UTF-8') as f2:
    f2.write('Agency name;Website;Social media;Contact person;Job title\n')
    for comp in companies:
        sm = ' '.join(comp['media'])
        for tm in comp['team']:
            f2.write(f"{comp['title']};{comp['site']};{sm};{tm['name']};{tm['job']}\n")
        if len(comp['team']) == 0:
            f2.write(f"{comp['title']};{comp['site']};{sm};;\n")

driver.quit()
