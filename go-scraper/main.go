package main

import (
	"log"

	scrab "go-scraper/lib"
)

func main() {
	links := scrab.Scraper("https://www.wikipedia.de")
	for link := range links {
		log.Println(links[link])
	}
}
