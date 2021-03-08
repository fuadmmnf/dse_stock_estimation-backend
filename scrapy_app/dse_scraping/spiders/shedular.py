# # from scrapy.crawler import CrawlerProcess
# # from scrapy.utils.project import get_project_settings
# # from apscheduler.schedulers.twisted import TwistedScheduler

# # from Demo.spiders.baidu import des

# # process = CrawlerProcess(get_project_settings())
# # scheduler = TwistedScheduler()
# # scheduler.add_job(process.crawl, 'interval', args=[des], seconds=10)
# # scheduler.start()
# # process.start(False)


# # from twisted.internet import reactor
# # from dse_scraping.spiders.des_spider import DesSpider
# # from scrapy.crawler import CrawlerRunner

# # def run_crawl():
# #     """
# #     Run a spider within Twisted. Once it completes,
# #     wait 5 seconds and run another spider.
# #     """
# #     runner = CrawlerRunner({
# #         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
# #         })
# #     deferred = runner.crawl(DesSpider)
# #     # you can use reactor.callLater or task.deferLater to schedule a function
# #     deferred.addCallback(reactor.callLater, 5, run_crawl)
# #     return deferred

# # run_crawl()
# # reactor.run()   # you

# # from dse_scraping.spiders.des_spider import DesSpider
# # from scrapy import cmdline
# # import schedule
# # import time
# # from scrapy.crawler import CrawlerProcess


# # def run_spider_cmd():
# #     print("Running spider")
# #     cmdline.execute("scrapy crawl des".split())


# # process = CrawlerProcess({
# #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
# # })


# # schedule.every(5).seconds.do(run_spider_cmd)

# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)




# # from dse_scraping.spiders.des_spider import DesSpider
# # from scrapy import cmdline
# # from scrapy.crawler import CrawlerProcess
# # import sched, time
# # from datetime import datetime, timedelta
# # from twisted.internet import reactor
# # from scrapy.crawler import CrawlerRunner



# # def run_crawl():
# #     """
# #     Run a spider within Twisted. Once it completes,
# #     wait 5 seconds and run another spider.
# #     """
# #     runner = CrawlerRunner({
# #         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
# #         })
# #     deferred = runner.crawl(DesSpider)
# #     # you can use reactor.callLater or task.deferLater to schedule a function
# #     deferred.addCallback(reactor.callLater, 5, run_crawl)
# #     return deferred

# # # run_crawl()
# # # reactor.run()


# # s = sched.scheduler(time.time, time.sleep)
# # def print_time(a='default'):
# #     print("From print_time", time.time(), a)

# # def run_spider_cmd():
# #     print("Running spider")
# #     cmdline.execute("scrapy crawl des".split())


# # process = CrawlerProcess({
# #     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
# # })

# # x= datetime.today()
# # # y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
# # y = x + timedelta(seconds=5)

# # delta_t=y-x
# # # print ("working....")
# # secs=delta_t.total_seconds()

# # def print_some_times():
# #     # print(time.time())
# #     s.enter(secs, 1, run_crawl)
# #     # s.enter(5, 2, print_time, argument=('positional',))
# #     # s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
# #     s.run()
# #     print(time.time())

# # counter = 1
# # while(True):
# #     print(counter)
# #     counter += 1
# #     print_some_times()



# from apscheduler.schedulers.twisted import TwistedScheduler
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess

# from dse_scraping.spiders.latest_share_spider import LatestSpider
# from dse_scraping.spiders.company_list_spider import CompanySpider
# import sched, time
# from datetime import datetime, timedelta


# x = datetime.today()
# #Per day at 1 am
# # y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
# #every 10 seconds
# y = x + timedelta(seconds=10)

# delta_t=y-x
# secs=delta_t.total_seconds()

# process = CrawlerProcess(get_project_settings())
# sched = TwistedScheduler()
# sched.add_job(process.crawl, 'interval', args=[LatestSpider], seconds=secs)
# sched.add_job(process.crawl, 'interval', args=[CompanySpider], seconds=secs)
# sched.start()
# process.start(False)


# # from scrapy_app.spiders.DayEndArchiveSpider import DayEndArchiveSpider
# # from scrapy_app.spiders.DseMarketSummarySpider import DseMarketSummarySpider
# # from scrapy_app.spiders.TickerSpider import TickerSpider

# # x= datetime.today()
# # # y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
# # y = x + timedelta(seconds=5)

# # delta_t=y-x
# # # print ("working....")
# # secs=delta_t.total_seconds()

# # def schedule_method():
# #     # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# #     # runner = CrawlerRunner(get_project_settings())
# #     # runner.crawl(DesSpider)
# #     # runner.join()

# #     process = CrawlerProcess(get_project_settings())
# #     process.crawl(DesSpider)
# #     process.start()


# # sched = TwistedScheduler()
# # # sched.add_job(schedule_method, trigger='cron', second="*/5", hour="10-16")
# # # sched.add_job(schedule_method, trigger='cron', second="*/5")
# # sched.add_job(schedule_method, 'interval', seconds = 12)

# # # def schedule_archive_method():
# # #     configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# # #     runner = CrawlerRunner(get_project_settings())
# # #     runner.crawl(DseMarketSummarySpider)
# # #     runner.crawl(DayEndArchiveSpider)
# # #     runner.join()


# # # sched.add_job(schedule_archive_method, trigger='cron', hour="18")

# # sched.start()
# # reactor.run()
