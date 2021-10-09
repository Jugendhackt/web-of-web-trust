// The api calls to the backend server
package goscraper_lib

import (
	"net/http"
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
