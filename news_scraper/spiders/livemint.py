import scrapy

class LivemintSpider(scrapy.Spider):
    name = 'livemint'
    allowed_domains = ['livemint.com']
    start_urls = ['https://www.livemint.com/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2
    }

    def parse(self, response):
        # Select all <a> tags for section names
        sections = response.xpath('//a[@class="sectionName"]')
        
        for section in sections:
            # Extract the text content (section name)
            section_name = section.xpath('./text()').get()

            if section_name:
                section_name = section_name.strip()

                # Construct the URL based on the section name
                section_url = response.urljoin(f'/{section_name}')

                # Make a request to the section URL and call parse_articles
                yield scrapy.Request(url=section_url, callback=self.parse_articles, meta={'category_name': section_name})

    def parse_articles(self, response):
        section_name = response.meta.get('section_name')

        # Select articles in this section
        articles = response.xpath('//h2[@class="headline"]/a')
        
        for article in articles:
            # Extract the href attribute (link)
            link = article.xpath('./@href').get()

            # Extract the text content (headline)
            headline = article.xpath('./text()').get()

            if link:
                # Make a request to the article page to get additional information
                article_url = response.urljoin(link)
                yield scrapy.Request(url=article_url, callback=self.parse_article_details, meta={
                    'section_name': section_name,
                    'headline': headline,
                    'link': article_url
                })

    def parse_article_details(self, response):
        # Extract meta data passed from the previous request
        section_name = response.meta.get('section_name')
        headline = response.meta.get('headline')
        link = response.meta.get('link')

        # Extract Author Name and Author URL
        author_name = response.xpath('//div[@class="storyPage_authorDesc__zPjwo"]//strong/text()').get()
        author_url = response.xpath('//div[@class="storyPage_authorDesc__zPjwo"]//a/@href').get()

        # Extract Published Date
        published_date = response.xpath('//div[@class="storyPage_date__JS9qJ"]//span/text()').get()

        # Extract Article Content (from multiple "storyParagraph" elements)
        article_content = response.xpath('//div[contains(@class, "storyParagraph")]//p//text()').getall()

        # Join the article content paragraphs into a single text block
        article_content = ' '.join(article_content).strip() if article_content else None

        # Yield the scraped data
        yield {
            'Section Name': section_name,
            'Article URL': link,
            'Title': headline.strip() if headline else None,
            'Author Name': author_name.strip() if author_name else None,
            'Author URL': response.urljoin(author_url) if author_url else None,
            'Article Content': article_content,
            'Published Date': published_date.strip() if published_date else None
        }
