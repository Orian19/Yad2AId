import logging
import azure.functions as func
from utils.refresh_apts_urls import refresh_apts_urls

app = func.FunctionApp()

# @app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
@app.schedule(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    refresh_apts_urls()
    logging.info('Python timer trigger function executed.')
