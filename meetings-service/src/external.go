package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"
)

var httpClient = &http.Client{
	Timeout: time.Second * 10,
}

func GetCalendarsByIds(ids []string) []Calendar {
	idsParam := strings.Join(ids, ",")

	log.Println(idsParam)

	url := fmt.Sprintf("http://krakend:8080/calendars?ids=%s", idsParam)

	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Println("Error:", err)
		return []Calendar{}
	}
	defer resp.Body.Close()

	var data []Calendar
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Println("Decode Error:", err)
		return []Calendar{}
	}

	return data
}

func getParticipantsByIds(ids []string) []Participant {
	idsParam := strings.Join(ids, ",")

	url := fmt.Sprintf("http://krakend:8080/participants?ids=%s", idsParam)

	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Println("Error:", err)
		return []Participant{}
	}
	defer resp.Body.Close()

	var data []Participant
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Println("Decode Error:", err)
		return []Participant{}
	}

	return data
}

func GetAttachmentsByIds(ids []string) []Attachment {
	idsParam := strings.Join(ids, ",")

	url := fmt.Sprintf("http://krakend:8080/attachments?ids=%s", idsParam)

	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Println("Error:", err)
		return []Attachment{}
	}
	defer resp.Body.Close()

	var data []Attachment
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Println("Decode Error:", err)
		return []Attachment{}
	}

	return data
}
