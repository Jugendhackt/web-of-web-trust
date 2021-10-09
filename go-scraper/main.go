package main

import (
	scrab "go-scraper/lib"
)

func main() {
	api := scrab.InitApi("localhost", 8080)
	links := []string{"faz.net", "ard.de"}
	api.PostUpdate("bild.de", links, false, 1337)
}
