package main

import (
	"log"
	"net/http"
)

func main() {
	connectToMongoDB()

	router := initializeRouter()

	log.Fatal(http.ListenAndServe(":8080", router))

}
