from datetime import datetime
import os
from allure_commons.types import AttachmentType
import allure

def take_screenshot(context, step_name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/{step_name}_{timestamp}.png"
    context.driver.save_screenshot(filename)
    allure.attach.file(filename, name=step_name, attachment_type=AttachmentType.PNG)
