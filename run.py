import argparse
from subprocess import call

def parse():
    parser = argparse.ArgumentParser(description='Potato Bot Runner')

    ## Sets logs to DEBUG
    parser.add_argument(
            '-d',
            '--debug',
            help='Set logs to DEBUG mode',
            action='store_true'
    )
    
    parser.add_argument(
            '-e',
            '--error',
            help='Set logs to ERROR mode',
            action='store_true'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse()

    if args.debug:
        call(['python3', 'bot.py', '1'])
    elif args.error:
        call(['python3', 'bot.py', '2'])
    else:
        call(['python3', 'bot.py', '0'])
        
