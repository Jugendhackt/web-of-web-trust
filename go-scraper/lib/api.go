// The api calls to the backend server
package goscraper_lib

import (
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
