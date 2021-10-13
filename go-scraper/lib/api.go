// The api calls to the backend server
package goscraper_lib

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"strconv"
)

// API struct holds all necessary information
type API struct {
	server string
	port   int
	client *http.Client
}

// this struct is responsible for the update JSON send to the API
type updateJSON struct {
	Domain  string   `json:"domain"`
	Links   []string `json:"links"`
	Network bool     `json:"network"`
	Updated int64    `json:"last_updated"`
}

// InitAPI initialises and returns a new API struct
func InitApi(server string, port int) *API {
	api := API{
		server: server,
		port:   port,
		client: http.DefaultClient,
	}
	return &api
}

// GetSpecs runs the /openapi.json api call with a GET request
func (api *API) GetSpecs() string {
	res, err := api.client.Get(api.server + ":" + strconv.Itoa(api.port) + "/openapi.json")

	if err != nil {
		log.Println(err)
	}
	defer res.Body.Close()

	b, err := io.ReadAll(res.Body)

	if err != nil {
		log.Println(err)
	}

	return string(b)
}

// PostUpdate runs the /update api call with a POST request
func (api *API) PostUpdate(domain string, links []string, network bool, updated int64) string {
	str := updateJSON{
		Domain:  domain,
		Links:   links,
		Network: network,
		Updated: updated,
	}

	if len(links) > 100 {
		str.Links = links[:99]
		log.Println("Called\r")
		go api.PostUpdate(domain, links[99:], network, updated)
	}
	js, err := json.Marshal(str)

	if err != nil {
		log.Println(err)
	}
	res, err := api.client.Post(api.server+":"+strconv.Itoa(api.port)+"/domain/update/", "application/json", bytes.NewBuffer(js))

	if err != nil {
		log.Println(err)
	}

	defer res.Body.Close()

	b, err := io.ReadAll(res.Body)

	if err != nil {
		log.Println(err)
	}
	return string(b)
}
