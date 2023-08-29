import scrapy


class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["bul.az"]
    start_urls = ["https://bul.az/dasinmaz-emlak?page=1"]

    def parse(self, response):
        # Extract all href attributes from anchor elements within div.media-product
        hrefs = response.css('div.media-product a.image-box::attr(href)').getall()

        for href in hrefs:
            yield {
                'href': href
            }

        # Find the next page link
        next_page_relative = response.css('ul.list-pagination a.fa-caret-right::attr(href)').get()
        if next_page_relative:
            next_page = response.urljoin(next_page_relative)
            yield scrapy.Request(url=next_page, callback=self.parse)
