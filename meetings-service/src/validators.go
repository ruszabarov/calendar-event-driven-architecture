package main

import (
	"regexp"
	"time"
)

func isValidEmail(email string) bool {
	emailRegex := `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
	re := regexp.MustCompile(emailRegex)
	return re.MatchString(email)
}

func parseCustomDateTime(datetimeStr string) (time.Time, error) {
	const layout = "2006-01-02 03:04 PM" // Layout for the custom format
	return time.Parse(layout, datetimeStr)
}
