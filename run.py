import time
from functions import *

updater = "updater.py"

def run_core():
    from core.main import main #NOQA
    main()

if __name__=="__main__":
    if not is_process_open(updater):
        run_script_in_terminal(updater)
    time.sleep(2)
    run_core()