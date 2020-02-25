from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

firefox = webdriver.Firefox()
firefox.get('http://foo.bar')
element_to_hover_over = firefox.find_element_by_id("baz")

hover = ActionChains(firefox).move_to_element(element_to_hover_over)
hover.perform()