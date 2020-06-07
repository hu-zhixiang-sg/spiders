from SpiderProject.SpiderProject.spiders.SpiderFactory import SPIDER_FACTORY
from SpiderProject.SpiderProject.spiders.SpiderFactory import order_factory
from utils.utils import send_email
import sys

def main():
    try:
        SpiderClass = SPIDER_FACTORY[sys.argv[1]]
        order_factory(SpiderClass)(SpiderClass)
    except Exception as e:
        print(e.__traceback__)
        send_email(sys.argv[1])

if __name__ == '__main__':
    main()