package goscraper_lib

import (
	"github.com/gocolly/colly"
)

func Scraper(seedURL string) []string {
	// Instantiate default collector
	c := colly.NewCollector(
		colly.MaxDepth(3),
	)

	links := []string{}

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
