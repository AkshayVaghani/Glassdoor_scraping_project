from scrapy import Spider, Request
from glassdoor.items import GlassdoorItem
import re


class glassdoorSpider(Spider):
    name = 'glassdoor'
    allowed_urls = ['https://www.glassdoor.com/']

    # original
    #start_urls = ['https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Blockchain&sc.keyword=Blockchain&locT=&locId=&jobType=']

    # this also works, change IN code for different country
    start_urls = ['https://www.glassdoor.com/Job/us-blockchain-jobs-SRCH_IL.0,2_IN1_KO3,13.htm']

    def parse(self, response):
        # Find the total number of pages in the result so that we can decide how many urls to scrap
        # print("test")
        text = response.xpath('//*[@id="MainColSummary"]/p/text()').    extract_first()
        total = re.findall('\d+', text)
        total = int(''.join(total))
        # total
        #per_page = 30
        #number_pages = total // per_page

        # find total number of pages
        number_pages = response.xpath("//*[@id='ResultsFooter']/div[1]/text()").extract_first().strip()
        number_pages = int(number_pages.lstrip("Page 1 of "))

        print("&" * 50)
        print(number_pages)
        print("&" * 50)

        #number_pages = 1

    # list of G20 country code
    # list of country
    #countryName=['USA','UK','CANADA','FRANCE','GERMANY','ITALY','AUSTRALIA','SA','RUSSIA','SOUTH AFRICA','ARGENTINA','BRAZIL','MEXICO','INDIA','CHINA','INDONESIA','JAPAN','SOUTH KOREA','TURKEY']

        #country_code = [1, 2, 3, 86, 96, 120, 16, 207, 205, 211, 15, 36, 169, 115, 48, 113, 123, 135, 238]
        country_code = [120, 15]

    # List comprehension to construct all the urls for all G20 country blockchanin job and each countries all blockchain job listing pages
        result_urls = ['https://www.glassdoor.com/Job/us-blockchain-jobs-SRCH_IL.0,2_IN{country}_KO3,13_IP{page}.htm'.format(country=x, page=y) for x in country_code for y in range(1, number_pages + 1)]

        #print("&" * 50)
        # print(result_urls)
        #print("&" * 50)

    # Yield the requests to different search result urls,
    # using parse_result_page function to parse the response.
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        # This fucntion parses the search result page.
        # We are looking for url of the detail page.
        # get unique job ids to get on a job page
        job_ids = response.xpath("//ul[@class='jlGrid hover']/li/@data-id").extract()  # an example id: 2220873086

        # select country name
        try:
            country_name = response.xpath("//div[@class='condensed showHH']/span/text()").extract_first()
            country_name = country_name.lstrip("'Blockchain Jobs in")
        except:
            country_name = 'None'
        # Manually concatenate all the urls
        # generate url for a job list page
        detail_urls = ['https://www.glassdoor.com/job-listing/-JV_IC1146821_KO0,14_KE15,23.htm?jl=' + jobid for jobid in job_ids]

        # Yield the requests to the details pages,
        # using parse_detail_page function to parse the response.
        for url in detail_urls:
            yield Request(url=url, callback=self.parse_job_page, meta={"country_name": country_name})

    def parse_job_page(self, response):

        # parse job title
        try:
            job_title = response.xpath('//h2[@class="noMargTop margBotXs strong"]/text()').extract_first().strip()
        except:
            job_title = 'None'

        #print('=' * 50)
        # print(job_title)

        # parse company name
        try:
            company_name = response.xpath('//span[@class="strong ib"]/text()').extract_first().strip()
        except:
            company_name = "None"

        # parse city and state
        try:
            city_state = response.xpath('//span[@class="subtle ib"]/text()').extract_first()[3:]
        except:
            city_state = 'None'

        # parse job description
        #job_desc = response.xpath('//div[@class="jobDescriptionContent desc module pad noMargBot"]/text()').extract()
        try:
            job_desc = response.xpath('//div[@class="jobDescriptionContent desc"]//text()').extract()
            if len(job_desc) == 0:
                job_desc = response.xpath('//*[@id="JobDescriptionContainer"]//text()').extract()
            job_desc = ''.join(job_desc).strip()
        except:
            job_desc = 'None'

        # convert job description list to string

        # print(type(job_desc))
        # print(job_desc[0])
        # print(len(job_desc))

        # company ratings
        #company_rating = response.xpath('//div[@class="ratingNum"]/text()').extract_first()
        try:
            company_rating = response.xpath('//span[@class="compactStars margRtSm"]/text()').extract_first()[1:]
        except:
            company_rating = "None"

        # average salary
        try:
            average_salary = response.xpath('//h2[@class="salEst"]/text()').extract_first()
        except:
            average_salary = "None"

        # date posted
        try:
            post_date = response.xpath('//span[@class="minor nowrap"]/text()').extract_first()
        except:
            post_date = "None"

        # getting on overview page is tricky, first need to go on inspect elements-network and refresh page and see the overview tab. In overview tab, there is the link, This like opens new plain text page. each job has this unique link and url for this link changes base on company unique id.(Thanks Michal for explaining this insight !)
        # here, we will get unique id  by inspecting the job page info
        # using id we generate the link for overview plain text page
        company_id = response.xpath('//*[@id="EmpBasicInfo"]/@data-emp-id').extract_first()
        if company_id == None:
            company_id = response.xpath('//span[@class="hidden ratingsDetailsInfo"]/@data-employer-id').extract_first()
        if company_id == None:
            print(company_name, 'None')

        # print(company_id)
        # print('=' * 100)
        # item = GlassdoorItem()
        # item["job_title"] = job_title
        # item["company_name"] = company_name
        # item["city_state"] = city_state
        # item["job_desc"] = job_desc
        # item["company_rating"] = company_rating
        # item["average_salary"] = average_salary
        # item["post_date"] = post_date
        #item["company_id"] = company_id
        # yield item

        #company_overview_url = 'https://www.glassdoor.com/Job/overview/companyOverviewBasicInfoAjax.htm?employerId={}&title=+Overview&linkCompetitors=true'.format(company_id)

        company_overview_url = "https://www.glassdoor.com/Job/overview/companyOverviewBasicInfoAjax.htm?employerId=" + company_id + "&title=+Overview&linkCompetitors=true"
        # Occurs 41 times
        # print(company_overview_url)
        # print('*' * 100)

        # pass the country_name to next stage
        country_name = response.meta['country_name']

        yield Request(company_overview_url, callback=self.parse_overview_page, meta={"company_id": company_id, "job_title": job_title, "company_name": company_name, "city_state": city_state, "job_desc": job_desc, "company_rating": company_rating, "average_salary": average_salary, "post_date": post_date, "country_name": country_name})

    def parse_overview_page(self, response):

        country_name = response.meta['country_name']
        company_id = response.meta['company_id']
        job_title = response.meta['job_title']
        company_name = response.meta['company_name']
        city_state = response.meta['city_state']
        job_desc = response.meta['job_desc']
        company_rating = response.meta['company_rating']
        average_salary = response.meta['average_salary']
        post_date = response.meta['post_date']

        labels = response.xpath('//div[@class = "info flexbox row col-hh"]/div/label/text()').extract()
        values = response.xpath('//div[@class = "info flexbox row col-hh"]/div/span/text()').extract()
        values = list(map(str.strip, values))
        company_info = list(zip(labels, values))

        # occurs 11 times
        # print(company_info)
        # print('#' * 100)

        item = GlassdoorItem()
        item["country_name"] = country_name
        item["company_id"] = company_id
        item["job_title"] = job_title
        item["company_name"] = company_name
        item["city_state"] = city_state
        item["job_desc"] = job_desc
        item["company_rating"] = company_rating
        item["average_salary"] = average_salary
        item["post_date"] = post_date
        item["company_info"] = company_info

        # 11 times
        #print('=' * 100)
        #print("company_info", item["company_info"][0])
        yield item
