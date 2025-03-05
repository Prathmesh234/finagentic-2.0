from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import List, Optional, Union, Dict, Any
from selenium.webdriver.remote.webelement import WebElement
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class Computer_Use_Agent_plugin:
    def __init__(self):
        self.driver = None
    @kernel_function(description="Initialize Microsoft Edge WebDriver with optional configurations.")
    def initialize_edge_driver(self, url: str = "https://www.bing.com/"):
        """Initialize Microsoft Edge WebDriver with optional configurations.
        
        Args:
            headless: Whether to run the browser in headless mode (without GUI). Default is False.
            user_agent: Custom user agent string to use. Default is None.
            download_dir: Directory path where downloads should be saved. Default is None.
            
        Returns:
            Configured Edge WebDriver instance.
        """
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        self.driver.get(url)
        
        print(f"Microsoft Edge opened and navigated to {url}")
        return "Browser initialized successfully"

    @kernel_function(description="Find a web element using its ID attribute.")
    def locate_element_by_id(self, element_id: str) -> WebElement:
        """Find a web element using its ID attribute.
        
        Args:
            driver: The WebDriver instance.
            element_id: The ID attribute value to search for.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.ID, element_id)

    @kernel_function(description="Find a web element using its name attribute.")
    def locate_element_by_name(self, name: str) -> WebElement:
        """Find a web element using its name attribute.
        
        Args:
            driver: The WebDriver instance.
            name: The name attribute value to search for.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.NAME, name)

    @kernel_function(description="Find a web element using its CSS class name.")
    def locate_element_by_class_name(self, class_name: str) -> WebElement:
        """Find a web element using its CSS class name.
        
        Args:
            driver: The WebDriver instance.
            class_name: The CSS class name to search for.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.CLASS_NAME, class_name)

    @kernel_function(description="Find a web element using its HTML tag name.")
    def locate_element_by_tag_name(self, tag_name: str) -> WebElement:
        """Find a web element using its HTML tag name.
        
        Args:
            driver: The WebDriver instance.
            tag_name: The HTML tag name to search for.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.TAG_NAME, tag_name)

    @kernel_function(description="Find a web element using an XPath expression.")
    def locate_element_by_xpath(self, xpath: str) -> WebElement:
        """Find a web element using an XPath expression.
        
        Args:
            driver: The WebDriver instance.
            xpath: The XPath expression to locate the element.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.XPATH, xpath)

    @kernel_function(description="Find a web element using a CSS selector.")
    def locate_element_by_css_selector(self, selector: str) -> WebElement:
        """Find a web element using a CSS selector.
        
        Args:
            driver: The WebDriver instance.
            selector: The CSS selector to locate the element.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    @kernel_function(description="Find a link element using its exact text.")
    def locate_element_by_link_text(self, link_text: str) -> WebElement:
        """Find a link element using its exact text.
        
        Args:
            driver: The WebDriver instance.
            link_text: The exact text of the link.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.LINK_TEXT, link_text)

    @kernel_function(description="Find a link element using partial text matching.")
    def locate_element_by_partial_link_text(self, partial_link_text: str) -> WebElement:
        """Find a link element using partial text matching.
        
        Args:
            driver: The WebDriver instance.
            partial_link_text: The partial text of the link.
            
        Returns:
            The first matching element.
        """
        return self.driver.find_element(By.PARTIAL_LINK_TEXT, partial_link_text)

    # Multiple elements location
    @kernel_function(description="Find all web elements with the specified ID attribute.")
    def locate_elements_by_id(self, element_id: str) -> List[WebElement]:
        """Find all web elements with the specified ID attribute.
        
        Args:
            driver: The WebDriver instance.
            element_id: The ID attribute value to search for.
            
        Returns:
            All matching elements.
        """
        return self.driver.find_elements(By.ID, element_id)

    @kernel_function(description="Find all web elements with the specified name attribute.")
    def locate_elements_by_name(self, name: str) -> List[WebElement]:
        """Find all web elements with the specified name attribute.
        
        Args:
            driver: The WebDriver instance.
            name: The name attribute value to search for.
            
        Returns:
            All matching elements.
        """
        return self.driver.find_elements(By.NAME, name)

    @kernel_function(description="Find all web elements with the specified CSS class name.")
    def locate_elements_by_class_name(self, class_name: str) -> List[WebElement]:
        """Find all web elements with the specified CSS class name.
        
        Args:
            driver: The WebDriver instance.
            class_name: The CSS class name to search for.
            
        Returns:
            All matching elements.
        """
        return self.driver.find_elements(By.CLASS_NAME, class_name)

    @kernel_function(description="Find all web elements with the specified HTML tag name.")
    def locate_elements_by_tag_name(self, tag_name: str) -> List[WebElement]:
        """Find all web elements with the specified HTML tag name.
        
        Args:
            driver: The WebDriver instance.
            tag_name: The HTML tag name to search for.
            
        Returns:
            All matching elements.
        """
        return self.driver.find_elements(By.TAG_NAME, tag_name)

    @kernel_function(description="Find all web elements matching the XPath expression.")
    def locate_elements_by_xpath(self, xpath: str) -> List[WebElement]:
        """Find all web elements matching the XPath expression.
        
        Args:
            driver: The WebDriver instance.
            xpath: The XPath expression to locate elements.
            
        Returns:
            All matching elements.
        """
        return self.driver.find_elements(By.XPATH, xpath)

    @kernel_function(description="Find all web elements matching the CSS selector.")
    def locate_elements_by_css_selector(self, selector: str) -> List[WebElement]:
        """Find all web elements matching the CSS selector.
        
        Args:
            driver: The WebDriver instance.
            selector: The CSS selector to locate elements.
            
        Returns:
            All matching elements.
        """
        return  self.driver.find_elements(By.CSS_SELECTOR, selector)

    @kernel_function(description="Find all link elements with the exact text.")
    def locate_elements_by_link_text(self, driver: webdriver.Edge, link_text: str) -> List[WebElement]:
        """Find all link elements with the exact text.
        
        Args:
            driver: The WebDriver instance.
            link_text: The exact text of the links.
            
        Returns:
            All matching elements.
        """
        return driver.find_elements(By.LINK_TEXT, link_text)

    @kernel_function(description="Find all link elements with the specified partial text.")
    def locate_elements_by_partial_link_text(self, partial_link_text: str) -> List[WebElement]:
        """Find all link elements with the specified partial text.
        
        Args:
            driver: The WebDriver instance.
            partial_link_text: The partial text of the links.
            
        Returns:
            All matching elements.
        """
        return self.driver.find_elements(By.PARTIAL_LINK_TEXT, partial_link_text)

    # Element interaction functions
    @kernel_function(description="Click on a web element.")
    def click_element(self, element: WebElement):
        """Click on a web element.
        
        Args:
            driver: The WebDriver instance.
            element: The element to click on.
        """
        element.click()

    @kernel_function(description="Type text into a web element.")
    def send_keys_to_element(self, element: WebElement, text: str):
        """Type text into a web element.
        
        Args:
            driver: The WebDriver instance.
            element: The element to type into.
            text: The text to type.
        """
        element.send_keys(text)

    @kernel_function(description="Clear the content of a web element (usually form fields).")
    def clear_element(self, element: WebElement):
        """Clear the content of a web element (usually form fields).
        
        Args:
            driver: The WebDriver instance.
            element: The element to clear.
        """
        element.clear()

    @kernel_function(description="Retrieve the visible text of a web element.")
    def get_element_text(self, element: WebElement) -> str:
        """Retrieve the visible text of a web element.
        
        Args:
            driver: The WebDriver instance.
            element: The element to get text from.
            
        Returns:
            The visible text of the element.
        """
        return element.text

    @kernel_function(description="Retrieve the value of a specific attribute from a web element.")
    def get_element_attribute(self, element: WebElement, attribute: str) -> str:
        """Retrieve the value of a specific attribute from a web element.
        
        Args:
            driver: The WebDriver instance.
            element: The element to get the attribute from.
            attribute: The name of the attribute.
            
        Returns:
            The value of the specified attribute.
        """
        return element.get_attribute(attribute)

    # Navigation functions
    @kernel_function(description="Navigate to a specific URL.")
    def open_url(self, url: str):
        """Navigate to a specific URL.
        
        Args:
            driver: The WebDriver instance.
            url: The URL to navigate to.
        """
        self.driver.get(url)

    @kernel_function(description="Reload the current page.")
    def refresh_page(self):
        """Reload the current page.
        
        Args:
            driver: The WebDriver instance.
        """
        self.driver.refresh()

    @kernel_function(description="Navigate to the previous page in browsing history.")
    def navigate_back(self):
        """Navigate to the previous page in browsing history.
        
        Args:
            driver: The WebDriver instance.
        """
        self.driver.back()

    @kernel_function(description="Navigate to the next page in browsing history.")
    def navigate_forward(self):
        """Navigate to the next page in browsing history.
        
        Args:
            driver: The WebDriver instance.
        """
        self.driver.forward()

    # Wait functions
    @kernel_function(description="Wait until an element is visible on the page before proceeding.")
    def wait_until_element_visible(self, by: By, locator: str, timeout: int = 10) -> WebElement:
        """Wait until an element is visible on the page before proceeding.
        
        Args:
            driver: The WebDriver instance.
            by: The method to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string that identifies the element.
            timeout: Maximum time to wait in seconds.
            
        Returns:
            The visible element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, locator)))

    @kernel_function(description="Wait until an element is clickable before proceeding.")
    def wait_until_element_clickable(self, by: By, locator: str, timeout: int = 10) -> WebElement:
        """Wait until an element is clickable before proceeding.
        
        Args:
            driver: The WebDriver instance.
            by: The method to locate the element (e.g., By.ID, By.XPATH).
            locator: The locator string that identifies the element.
            timeout: Maximum time to wait in seconds.
            
        Returns:
            The clickable element.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, locator)))

    # Frame handling functions
    @kernel_function(description="Switch the focus to a specific iframe element.")
    def switch_to_frame(self, frame_reference: Union[int, str, WebElement]):
        """Switch the focus to a specific iframe element.
        
        Args:
            driver: The WebDriver instance.
            frame_reference: Frame identifier (index, name, WebElement).
        """
        self.driver.switch_to.frame(frame_reference)

    @kernel_function(description="Switch the focus back to the main document.")
    def switch_to_default_content(self):
        """Switch the focus back to the main document.
        
        Args:
            driver: The WebDriver instance.
        """
        self.driver.switch_to.default_content()

    # Alert handling functions
    @kernel_function(description="Click 'OK' or 'Accept' on a JavaScript alert dialog.")
    def accept_alert(self):
        """Click 'OK' or 'Accept' on a JavaScript alert dialog.
        
        Args:
            driver: The WebDriver instance.
        """
        self.driver.switch_to.alert.accept()

    @kernel_function(description="Click 'Cancel' or 'Dismiss' on a JavaScript alert dialog.")
    def dismiss_alert(self):
        """Click 'Cancel' or 'Dismiss' on a JavaScript alert dialog.
        
        Args:
            driver: The WebDriver instance.
        """
        self.driver.switch_to.alert.dismiss()

    @kernel_function(description="Retrieve the text displayed in a JavaScript alert dialog.")
    def get_alert_text(self) -> str:
        """Retrieve the text displayed in a JavaScript alert dialog.
        
        Args:
            driver: The WebDriver instance.
            
        Returns:
            The text of the alert.
        """
        return self.driver.switch_to.alert.text

    # Screenshot function
    @kernel_function(description="Capture a screenshot of the current page and save it to a file.")
    def take_screenshot(self, file_path: str):
        """Capture a screenshot of the current page and save it to a file.
        
        Args:
            driver: The WebDriver instance.
            file_path: Path where the screenshot will be saved.
        """
        self.driver.save_screenshot(file_path)

    @kernel_function(description="Select an option from a dropdown by its visible text.")
    def select_by_visible_text(self,element: WebElement, text: str):
        """Select an option from a dropdown by its visible text.
        
        Args:
            driver: The WebDriver instance.
            element: The select element.
            text: The visible text of the option to select.
        """
        Select(element).select_by_visible_text(text)

    @kernel_function(description="Select an option from a dropdown by its value attribute.")
    def select_by_value(self, element: WebElement, value: str):
        """Select an option from a dropdown by its value attribute.
        
        Args:
            driver: The WebDriver instance.
            element: The select element.
            value: The value attribute of the option to select.
        """
        Select(element).select_by_value(value)

    @kernel_function(description="Select an option from a dropdown by its index position.")
    def select_by_index(self,element: WebElement, index: int):
        """Select an option from a dropdown by its index position.
        
        Args:
            driver: The WebDriver instance.
            element: The select element.
            index: The index position of the option to select.
        """
        Select(element).select_by_index(index)

    @kernel_function(description="Get the text of the currently selected option in a dropdown.")
    def get_selected_option_text(self,element: WebElement) -> str:
        """Get the text of the currently selected option in a dropdown.
        
        Args:
            driver: The WebDriver instance.
            element: The select element.
            
        Returns:
            The text of the currently selected option.
        """
        return Select(element).first_selected_option.text

    @kernel_function(description="Get all options from a dropdown as text.")
    def get_all_options(self, element: WebElement) -> List[str]:
        """Get all options from a dropdown as text.
        
        Args:
            driver: The WebDriver instance.
            element: The select element.
            
        Returns:
            The text of all available options.
        """
        return [option.text for option in Select(element).options]