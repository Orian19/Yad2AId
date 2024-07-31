import azure.functions as func

app = func.FunctionApp()

# Ensure this import is present to register the function
from .refresh_apts_urls import timer_trigger
