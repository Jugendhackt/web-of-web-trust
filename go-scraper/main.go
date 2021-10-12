package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/url"
	"os/exec"
	"os"
	"strconv"

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

	// Check environment for config
	envHost, envHostOK := os.LookupEnv("API_HOST")

	if envHostOK {
		confjs.APIconf.Server = envHost
	}

	envPort, envPortOk := os.LookupEnv("API_PORT")

	if envPortOk {
		port, err := strconv.Atoi(envPort)

		if err != nil {
			log.Fatal(err)
		} else {
			confjs.APIconf.Port = port
		}
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
}
