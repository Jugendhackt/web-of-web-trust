package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/url"
	"os/exec"

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

	for _, raw := range confjs.Netgood {
		links := scrab.Scraper(raw)

		parsedlinks := []string{}
		parsedurl, err := url.Parse(raw)
		if err != nil {
			log.Fatal(err)
		}
		domain := parsedurl.Host

		for _, unp := range links {
			pr, err := url.Parse(unp)
			if err != nil {
				log.Fatal(err)
			}
			parsedlinks = append(parsedlinks, pr.Host)
		}

		api.PostUpdate(domain, parsedlinks, true, 0)
	}

	for _, raw := range confjs.Netbad {
		links := scrab.Scraper(raw)

		parsedlinks := []string{}
		parsedurl, err := url.Parse(raw)
		if err != nil {
			log.Fatal(err)
		}
		domain := parsedurl.Host

		for _, unp := range links {
			pr, err := url.Parse(unp)
			if err != nil {
				log.Fatal(err)
			}
			parsedlinks = append(parsedlinks, pr.Host)
		}
		api.PostUpdate(domain, parsedlinks, false, 0)
	}

	exec.Command("python ../ruegen-scraper/ruege-scraper.py")
}
