import scrapy


class CombinedSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["bul.az"]
    start_urls = ["https://bul.az/dasinmaz-emlak?page=1"]

    def parse(self, response):
        # Extract links using LinksSpider
        links = response.css('div.media-product a.image-box::attr(href)').getall()

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_content, meta={"href": link})

        # Find the next page link
        next_page_relative = response.css('ul.list-pagination a.fa-caret-right::attr(href)').get()
        if next_page_relative:
            next_page = response.urljoin(next_page_relative)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_content(self, response):
        yield {
            'link': response.request.meta['href'],
            'phone': response.css('ul.list-contact-details a[href^="tel"]::text').get(),
            'whatsapp': response.css('ul.list-contact-details a[href*="whatsapp"]::text').get()
        }
