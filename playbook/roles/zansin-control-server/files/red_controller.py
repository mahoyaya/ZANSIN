"""
Implement a controller for the red modules (attack tool, crawler, judge) like the ZANSIN command.
"""
import os
import threading
import configparser
from datetime import datetime, timedelta
from docopt import docopt

from crawler.crawler_controller import crawler_execution


# Display banner.
def show_banner():
    banner = """
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
██████╗ ███████╗██████╗        ██████╗ ██████╗ ███╗   ██╗████████╗██████╗  ██████╗ ██╗     ██╗     ███████╗██████╗ 
██╔══██╗██╔════╝██╔══██╗      ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔═══██╗██║     ██║     ██╔════╝██╔══██╗
██████╔╝█████╗  ██║  ██║█████╗██║     ██║   ██║██╔██╗ ██║   ██║   ██████╔╝██║   ██║██║     ██║     █████╗  ██████╔╝
██╔══██╗██╔══╝  ██║  ██║╚════╝██║     ██║   ██║██║╚██╗██║   ██║   ██╔══██╗██║   ██║██║     ██║     ██╔══╝  ██╔══██╗
██║  ██║███████╗██████╔╝      ╚██████╗╚██████╔╝██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗███████╗███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═════╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""" + 'by ' + os.path.basename(__file__)
    print(banner)


# Define command option.
__doc__ = """{f}
usage:
    {f} -n <name> -s <servername>
    {f} -h | --help
options:
    -n <name>        : Leaner name (e.g., Taro Zansin).
    -s <servername>  : Target hostname (e.g., 192.168.0.5).
    -h --help Show this help message and exit.
""".format(f=__file__)


# Calling the Crawler.
def module_crawler(learner_name, start_time, end_time):
    crawler_execution(learner_name, start_time, end_time)


# Calling the Attack tool.
def module_attack_tool():
    print('attack tool')


# Calling the Judge.r
def module_judge():
    print('Judge!!')


def get_training_time(training_hours: int = 4) -> str:
    if not isinstance(training_hours, int):
        raise Exception('The format of the training time is incorrect.')

    training_start_date = datetime.now()
    training_end_date = training_start_date + timedelta(hours=training_hours)
    return training_start_date, training_end_date


# Main.
if __name__ == '__main__':
    file_name = os.path.basename(__file__)
    full_path = os.path.dirname(os.path.abspath(__file__))

    try:
        # Get command argument.
        args = docopt(__doc__)
        opt_leaner = args['-n']
        opt_hostname = args['-s']

        # Read config.ini.
        config = configparser.ConfigParser()
        config.read(os.path.join(full_path, 'config.ini'), encoding='utf-8')

        # Show banner.
        show_banner()

        # Get training time.
        start_time, end_time = get_training_time(int(config['Common']['training_hours']))

        # Define modules and arguments for threading.
        thread_crawler = threading.Thread(target=module_crawler, args=(opt_leaner, start_time, end_time))
        thread_attack_tool = threading.Thread(target=module_attack_tool)

        # Execute threads.
        thread_crawler.start()
        thread_attack_tool.start()

        # Join each thread.
        thread_crawler.join()
        thread_attack_tool.join()

        # Execute Judge.
        module_judge()
    except Exception as e:
        print(e.args)
