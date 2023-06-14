import scrapy


class LinkinSpiderSpider(scrapy.Spider):
    name = "linkin_spider"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python&location=United' \
              '%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='

    def start_requests(self):
        first_job_on_page = 0
        first_url=self.api_url+str(first_job_on_page)
        yield scrapy.Request(url=first_url,callback=self.parse,meta={'first_job_on_page': first_job_on_page})


    def parse(self, response):
        first_job_on_page=response.meta['first_job_on_page']

        jobs=response.css('li')
        num_job = len(jobs)
        print('--------------------------------------')
        print(first_job_on_page)
        print(num_job)
        for job in jobs:
            try:
                job_url=job.css('a.base-card__full-link::attr(href)').get().strip()
                job_title=job.css('h3.base-search-card__title::text').get().strip()
                company_title=job.css('a.hidden-nested-link::text').get().strip()
                job_location=job.css('span.job-search-card__location::text').get().strip()
                job_date=job.xpath('div/div/div/time/text()').get().strip()
            except Exception as e:
                job_url = 'empty'
                job_title ='empty'
                company_title = 'empty'
                job_location = 'empty'
                job_date = 'empty'

            yield {
                'job_title':job_title,
                'job url':job_url,
                'company_title':company_title,
                'job_location':job_location,
                # 'job_benefits':job_benefits,
                'job_date':job_date}
        if num_job>0:
            first_job_on_page=int(first_job_on_page)+25
            next_url=self.api_url+str(first_job_on_page)
            yield scrapy.Request(url=next_url,callback=self.parse,meta={'first_job_on_page': first_job_on_page})
