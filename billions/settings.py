# Scrapy settings for billions project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'billions'

SPIDER_MODULES = ['billions.spiders']
NEWSPIDER_MODULE = 'billions.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'billions (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
CONCURRENT_REQUESTS = 32
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 15
RETRY_ENABLED = True
RETRY_TIMES= 5

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'billions.middlewares.BillionsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'billions.middlewares.BillionsUserAgentMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.corestats.CoreStats':1,
   'billions.errorCheck.ErrorCheck': 2,
}
IMAGES_STORE = 'image'

# IMAGES_THUMBS = {
#     'home': (270, 270),
# }


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#DOWNLOAD_DELAY = 0 # delay in downloading images
#  RANDOMIZE_DOWNLOAD_DELAY  = True # delay in downloading images
ITEM_PIPELINES = {

    'billions.pipelines.BillionsImagePipeline':1,
    'billions.pipelines.BillionsReplaceImage1PathPipeline': 2,
    'billions.pipelines.BillionsNoHtmlTagPipeline': 3,
    'billions.pipelines.BillionsReplaceImage2PathPipeline': 4,
    'billions.pipelines.BillionsCaiPipeline': 4,
    'billions.pipelines.BillionImiaoPipeline': 5,
    "billions.pipelines.BillionsDBPipeline":6,
    "billions.pipelines.BillionJinghuaPipeline":7

    }

#
# LOG_ENABLED = True #是否启动日志记录，默认True
# LOG_ENCODING = 'UTF-8'
# # LOG_FILE = 'scarpy.log'#日志输出文件，如果为NONE，就打印到控制台
# LOG_LEVEL = 'ERROR'#日志级别，默认debug

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
