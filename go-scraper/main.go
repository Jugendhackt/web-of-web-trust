package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/url"
	"os/exec"
	"time"

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

	for {
		log.Println("WHILE")
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

			api.PostUpdate(domain, parsedlinks, true, time.Now().Unix())
			time.Sleep(time.Millisecond)
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
			api.PostUpdate(domain, parsedlinks, false, time.Now().Unix())
			time.Sleep(time.Millisecond)
		}

		exec.Command("python ../ruegen-scraper/ruege-scraper.py")
		time.Sleep(time.Millisecond)
	}
}
