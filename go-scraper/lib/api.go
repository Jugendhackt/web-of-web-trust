// The api calls to the backend server
package goscraper_lib

import (
	"encoding/json"
	"fmt"
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

// this structs are responsible for the update JSON send to the API
type updateJSON struct {
	Domain updateJSONnested `json:"domain"`
}

type updateJSONnested struct {
	Domain  string   `json:"domain"`
	Links   []string `json:"links"`
	Network bool     `json:"network"`
	Updated int      `json:"last_updated"`
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

// GetSpecs runs the /specs api call with a GET request
func (api *API) GetSpecs() string {
	res, err := api.client.Get(api.server + ":" + strconv.Itoa(api.port) + "/spec")

	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	b, err := io.ReadAll(res.Body)

	if err != nil {
		log.Fatal(err)
	}

	return string(b)
}

// PostUpdate runs the /update api call with a POST request
func (api *API) PostUpdate(domain string, links []string, network bool, updated int) string {
	str := updateJSON{
		updateJSONnested{
			Domain:  domain,
			Links:   links,
			Network: network,
			Updated: updated,
		},
	}

	js, err := json.Marshal(str)

	if err != nil {
		log.Fatal(err)
	}
	/*
		res, err := api.client.Post(api.server+":"+strconv.Itoa(api.port), "application/json", bytes.NewBuffer(js))

		if err != nil {
			log.Fatal(err)
		}
		defer res.Body.Close()

		b, err := io.ReadAll(res.Body)

		if err != nil {
			log.Fatal(err)
		}
	*/
	fmt.Println(string(js))
	return ""
}
