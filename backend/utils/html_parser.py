from bs4 import BeautifulSoup

def parse_html_structure(html_content: str):
    """
    Parse HTML content to extract form fields, buttons, and inputs
    used for generating selectors in Selenium test scripts.
    """
    soup = BeautifulSoup(html_content, "lxml")
    
    ui_elements = []
    supported_tags = ["input", "button", "select", "textarea", "a"]

    for element in soup.find_all(supported_tags):
        elem_info = {
            "tag": element.name,
            "id": element.get("id"),
            "name": element.get("name"),
            "type": element.get("type"),
            "text": element.get_text(strip=True),
            "class": " ".join(element.get("class")) if element.get("class") else None
        }
        ui_elements.append(elem_info)

    return ui_elements
