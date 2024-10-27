package main

import (
	"github.com/gorilla/mux"
)

func initializeRouter() *mux.Router {
	router := mux.NewRouter()

	router.HandleFunc("/meetings", GetMeetingsByIds).Methods("GET").Queries("ids", "{ids}")
	router.HandleFunc("/meetings", GetMeetings).Methods("GET")
	router.HandleFunc("/meetings", CreateMeeting).Methods("POST")
	router.HandleFunc("/meetings/{id}", UpdateMeetingById).Methods("PUT")
	router.HandleFunc("/meetings/{id}", DeleteMeetingById).Methods("DELETE")
	router.HandleFunc("/meetings/{meetingId}/addCalendar/{calendarId}", AddCalendarToMeeting).Methods("GET")
	router.HandleFunc("/meetings/{meetingId}/removeCalendar/{calendarId}", RemoveCalendarFromMeeting).Methods("GET")
	router.HandleFunc("/meetings/{meetingId}/addParticipant/{participantId}", AddParticipantToMeeting).Methods("GET")
	router.HandleFunc("/meetings/{meetingId}/removeParticipant/{participantId}", RemoveParticipantFromMeeting).Methods("GET")
	router.HandleFunc("/meetings/{meetingId}/addAttachment/{attachmentId}", AddAttachmentToMeeting).Methods("GET")
	router.HandleFunc("/meetings/{meetingId}/removeAttachment/{attachmentId}", RemoveAttachmentFromMeeting).Methods("GET")

	return router
}
