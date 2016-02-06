import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from twilio.rest import TwilioRestClient #Twilio API for text messaging

#Opens Firefox
browser = webdriver.Firefox()
browser.implicitly_wait(20) # seconds

#Navigates to ASU Class Catalog
browser.get('https://webapp4.asu.edu/catalog/Home.ext')

#Selects ASU Campus radio button
campusRadio = browser.find_element_by_id('typeSelectionC') 
campusRadio.click()
browser.implicitly_wait(20) # seconds

#Inserts subject into text field
subject = browser.find_element_by_id('subjectEntry')
subject.send_keys("***INSERT SUBJECT HERE***")
number = browser.find_element_by_id('catalogNbr')

#Inserts class number into text field
number.send_keys("***INSERT CATALOG NUMBER HERE***")
browser.find_element_by_id('search').click()
browser.implicitly_wait(20) # seconds

#Selects "All Classes" from drop down to view non-open classes.
browser.find_element_by_xpath("//select[@id='searchType']/option[text()='All classes']").click()
goButton = browser.find_element_by_id('Go')
goButton.click()
browser.implicitly_wait(20) # seconds

#Clicks into the class by the class number hyperlink
browser.find_element_by_xpath("//a[contains(text(),'INSERT CLASS NUMBER HERE')]").click()

#Loops until there is an open seat
numSeats = 0
while int(numSeats) == 0:
    try:
        browser.implicitly_wait(20) # seconds
        numSeats = browser.find_element_by_xpath("//td[@class='class-values'][last()]//td").text

        #If a seat is open, texts the student through Twilio's API with a link to add the class.
        if int(numSeats) > 0:
            print('A seat is available')
            account_sid = "***INSERT TWILIO ACCOUNT SID HERE***"
            auth_token  = "***INSERT TWILIO AUTH TOKEN HERE***"
            client = TwilioRestClient(account_sid, auth_token)
            client.messages.create(
                to="***INSERT YOUR CELL NUMBER HERE***", 
                from_="***INSERT TEST NUMBER GIVEN BY TWILIO***", 
                body="Seats are open at https://go.oasis.asu.edu/addclass/?STRM=2161&ACAD_CAREER=UGRD", 
            )
        else: #If there are no seats, refresh the page in 1 minute.
            print('No seats at ' + time.strftime("%I:%M:%S") + ' refreshing in 1 minute...' )

        time.sleep(60)
        browser.refresh()
    except: #Refreshes if it arrives at an unexpected page (404, etc).
        print('Unexpected error at ' + time.strftime("%I:%M:%S") + ' refreshing...')
        browser.refresh()
    
