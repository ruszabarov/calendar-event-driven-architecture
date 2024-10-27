package main

import (
	"time"
)

type Calendar struct {
	ID      string `json:"id" bson:"_id,omitempty"`
	Title   string `json:"title" bson:"title"`
	Details string `json:"details" bson:"details"`
}

type Meeting struct {
	ID           string        `json:"id" bson:"_id,omitempty"`
	Title        string        `json:"title" bson:"title"`
	Details      string        `json:"details" bson:"details"`
	DateTime     time.Time     `json:"datetime" bson:"datetime"`
	Location     string        `json:"location" bson:"location"`
	Calendars    []Calendar    `json:"calendars" bson:"calendars"`
	Participants []Participant `json:"participants" bson:"participants"`
	Attachments  []Attachment  `json:"attachments" bson:"attachments"`
}

type MeetingSummary struct {
	ID           string   `json:"id" bson:"_id,omitempty"`
	Title        string   `json:"title" bson:"title"`
	Details      string   `json:"details" bson:"details"`
	DateTime     string   `json:"datetime" bson:"datetime"`
	Location     string   `json:"location" bson:"location"`
	Calendars    []string `json:"calendars" bson:"calendars"`
	Participants []string `json:"participants" bson:"participants"`
	Attachments  []string `json:"attachments" bson:"attachments"`
}

type Participant struct {
	ID    string `json:"id" bson:"_id,omitempty"`
	Name  string `json:"name" bson:"name"`
	Email string `json:"email" bson:"email"`
}

type Attachment struct {
	ID  string `json:"id" bson:"_id,omitempty"`
	URL string `json:"url" bson:"url"`
}
