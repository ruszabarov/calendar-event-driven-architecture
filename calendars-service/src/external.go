package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"
)

var httpClient = &http.Client{
	Timeout: time.Second * 10,
}

func GetMeetingsByIds(ids []string) []MeetingSummary {
	idsParam := strings.Join(ids, ",")

	url := fmt.Sprintf("http://krakend:8080/meetings?ids=%s", idsParam)

	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Println("Error:", err)
		return []MeetingSummary{}
	}
	defer resp.Body.Close()

	var data []MeetingSummary
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Println("Decode Error:", err)
		return []MeetingSummary{}
	}

	return data
}

func AddCalendarToMeeting(meetingId string, calendarId string) {
	url := fmt.Sprintf("http://krakend:8080/calendars/%s/addMeeting/%s", calendarId, meetingId)

	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	resp.Body.Close()

	return
}
