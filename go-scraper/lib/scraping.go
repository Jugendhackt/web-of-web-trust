package goscraper_lib

import (
	"github.com/gocolly/colly"
)

func scraper(seedURL string) []string {
	// Instantiate default collector
	c := colly.NewCollector(
		// MaxDepth is 1, so only the links on the scraped page
		// is visited, and no further links are followed
		colly.MaxDepth(1),
	)

	links := make([]string, 1024)

	// On every a element which has href attribute call callback
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		link := e.Attr("href")
		links = append(links, link)
		// Visit link found on page
		e.Request.Visit(link)
	})

	c.Visit(seedURL)
	return links
}
