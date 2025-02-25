from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain_core.tools import tool
##we can use all of these 
# Element location functions
@tool
def locate_element_by_id(driver, element_id):
    return driver.find_element(By.ID, element_id)
@tool
def locate_element_by_name(driver, name):
    return driver.find_element(By.NAME, name)
@tool
def locate_element_by_class_name(driver, class_name):
    return driver.find_element(By.CLASS_NAME, class_name)
@tool
def locate_element_by_tag_name(driver, tag_name):
    return driver.find_element(By.TAG_NAME, tag_name)
@tool
def locate_element_by_xpath(driver, xpath):
    return driver.find_element(By.XPATH, xpath)
@tool
def locate_element_by_css_selector(driver, selector):
    return driver.find_element(By.CSS_SELECTOR, selector)
@tool
def locate_element_by_link_text(driver, link_text):
    return driver.find_element(By.LINK_TEXT, link_text)
@tool
def locate_element_by_partial_link_text(driver, partial_link_text):
    return driver.find_element(By.PARTIAL_LINK_TEXT, partial_link_text)

# Multiple elements location
@tool
def locate_elements_by_id(driver, element_id):
    return driver.find_elements(By.ID, element_id)
@tool
def locate_elements_by_name(driver, name):
    return driver.find_elements(By.NAME, name)
@tool
def locate_elements_by_class_name(driver, class_name):
    return driver.find_elements(By.CLASS_NAME, class_name)
@tool
def locate_elements_by_tag_name(driver, tag_name):
    return driver.find_elements(By.TAG_NAME, tag_name)
@tool
def locate_elements_by_xpath(driver, xpath):
    return driver.find_elements(By.XPATH, xpath)
@tool
def locate_elements_by_css_selector(driver, selector):
    return driver.find_elements(By.CSS_SELECTOR, selector)
@tool
def locate_elements_by_link_text(driver, link_text):
    return driver.find_elements(By.LINK_TEXT, link_text)
@tool
def locate_elements_by_partial_link_text(driver, partial_link_text):
    return driver.find_elements(By.PARTIAL_LINK_TEXT, partial_link_text)

# Element interaction functions
@tool
def click_element(driver, element):
    element.click()
@tool
def send_keys_to_element(driver, element, text):
    element.send_keys(text)
@tool
def clear_element(driver, element):
    element.clear()
@tool
def get_element_text(driver, element):
    return element.text
@tool
def get_element_attribute(driver, element, attribute):
    return element.get_attribute(attribute)

# Navigation functions
@tool
def open_url(driver, url):
    driver.get(url)
@tool
def refresh_page(driver):
    driver.refresh()
@tool
def navigate_back(driver):
    driver.back()
@tool
def navigate_forward(driver):
    driver.forward()

# Wait functions
@tool
def wait_until_element_visible(driver, by, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located((by, locator)))
@tool
def wait_until_element_clickable(driver, by, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((by, locator)))

# Frame handling functions
@tool
def switch_to_frame(driver, frame_reference):
    driver.switch_to.frame(frame_reference)
@tool
def switch_to_default_content(driver):
    driver.switch_to.default_content()

# Alert handling functions
@tool
def accept_alert(driver):
    driver.switch_to.alert.accept()
@tool
def dismiss_alert(driver):
    driver.switch_to.alert.dismiss()
@tool
def get_alert_text(driver):
    return driver.switch_to.alert.text

# Screenshot function
@tool
def take_screenshot(driver, file_path):
    driver.save_screenshot(file_path)