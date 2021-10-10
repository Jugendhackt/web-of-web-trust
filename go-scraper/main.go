package main

import (
	"encoding/json"
	"io/ioutil"
	"log"

	scrab "go-scraper/lib"
)

type Configjs struct {
	APIconf APIjs    `json:"api"`
	Netgood []string `json:"netgood"`
	Netbad  []string `json:"netbad"`
}

type APIjs struct {
	Server string `json:"server"`
	Port   int    `json:"port"`
}

func main() {
	conf, err := ioutil.ReadFile("./config.json")
	if err != nil {
		log.Fatal(err)
	}

	confjs := Configjs{}

	err = json.Unmarshal(conf, &confjs)
	if err != nil {
		log.Fatal(err)
	}

	api := scrab.InitApi(confjs.APIconf.Server, confjs.APIconf.Port)

	for _, url := range confjs.Netgood {
		links := scrab.Scraper(url)
		api.PostUpdate(url, links, true, 0)
	}

	for _, url := range confjs.Netbad {
		links := scrab.Scraper(url)
		api.PostUpdate(url, links, false, 0)
	}
}
