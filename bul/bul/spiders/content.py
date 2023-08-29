import scrapy


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["bul.az"]
    start_urls = ["https://bul.az/view/426305_heyet-evi-satilir-426305.html"]

    def parse(self, response):
        yield {
            'phone': response.css('ul.list-contact-details a[href^="tel"]::text').get(),
            'whatsapp': response.css('ul.list-contact-details a[href*="whatsapp"]::text').get()

        }
