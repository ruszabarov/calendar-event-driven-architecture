package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strings"
	"time"

	"github.com/google/uuid"
	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
)

func GetMeetings(w http.ResponseWriter, r *http.Request) {
	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cursor, err := collection.Find(ctx, bson.M{})
	if err != nil {
		http.Error(w, "Error fetching meetingSummaries", http.StatusInternalServerError)
		return
	}
	defer cursor.Close(ctx)

	var meetingSummaries []MeetingSummary
	if err = cursor.All(ctx, &meetingSummaries); err != nil {
		http.Error(w, "Error decoding meetingSummaries", http.StatusInternalServerError)
		return
	}

	var meetings []Meeting
	for _, meetingSummary := range meetingSummaries {
		meetings = append(meetings, ConvertSummaryToFull(meetingSummary))
	}

	responseData, err := json.Marshal(meetings)
	if err != nil {
		http.Error(w, "Error marshalling response", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_, err = w.Write(responseData)
	if err != nil {
		http.Error(w, "Error writing response", http.StatusInternalServerError)
		return
	}
}

func CreateMeeting(w http.ResponseWriter, r *http.Request) {
	var meetingSummary MeetingSummary
	err := json.NewDecoder(r.Body).Decode(&meetingSummary)
	if err != nil {
		http.Error(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	if meetingSummary.ID == "" {
		meetingSummary.ID = uuid.New().String()
	}

	if meetingSummary.Participants == nil {
		meetingSummary.Participants = []string{}
	}
	if meetingSummary.Attachments == nil {
		meetingSummary.Attachments = []string{}
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	_, err = collection.InsertOne(ctx, meetingSummary)
	if err != nil {
		http.Error(w, "Error inserting meetingSummary", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(meetingSummary)
}

func UpdateMeetingById(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	var updatedMeeting MeetingSummary
	err := json.NewDecoder(r.Body).Decode(&updatedMeeting)
	if err != nil {
		log.Println(err)
		respondWithError(w, http.StatusBadRequest, "Invalid request payload")
		return
	}

	updatedMeeting.ID = ""

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$set": bson.M{
			"title":    updatedMeeting.Title,
			"details":  updatedMeeting.Details,
			"location": updatedMeeting.Location,
			"datetime": updatedMeeting.DateTime,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err = collection.FindOneAndUpdate(ctx, bson.M{"_id": id}, update, opts).Decode(&meetingSummary)
	if err != nil {
		log.Println(err)
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, meetingSummary)
}

func DeleteMeetingById(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	result, err := collection.DeleteOne(ctx, bson.M{"_id": id})
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error deleting meeting")
		return
	}

	if result.DeletedCount == 0 {
		http.Error(w, "Meeting not found", http.StatusNotFound)
		return
	}

	respondWithJSON(w, http.StatusOK, map[string]string{"message": "meeting successfully deleted"})
}

func AddCalendarToMeeting(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	meetingId := vars["meetingId"]
	calendarId := vars["calendarId"]
	if meetingId == "" || calendarId == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'id' parameter")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$addToSet": bson.M{
			"calendars": calendarId,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err := collection.FindOneAndUpdate(ctx, bson.M{"_id": meetingId}, update, opts).Decode(&meetingSummary)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, ConvertSummaryToFull(meetingSummary))
}

func RemoveCalendarFromMeeting(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	meetingId := vars["meetingId"]
	calendarId := vars["calendarId"]
	if meetingId == "" || calendarId == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'id' parameter")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$pull": bson.M{
			"calendars": calendarId,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err := collection.FindOneAndUpdate(ctx, bson.M{"_id": meetingId}, update, opts).Decode(&meetingSummary)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, ConvertSummaryToFull(meetingSummary))
}

func AddParticipantToMeeting(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	meetingId := vars["meetingId"]
	participantId := vars["participantId"]
	if meetingId == "" || participantId == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'id' parameter")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$addToSet": bson.M{
			"participants": participantId,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err := collection.FindOneAndUpdate(ctx, bson.M{"_id": meetingId}, update, opts).Decode(&meetingSummary)
	if err != nil {
		log.Println(err)
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, ConvertSummaryToFull(meetingSummary))
}

func RemoveParticipantFromMeeting(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	meetingId := vars["meetingId"]
	participantId := vars["participantId"]
	if meetingId == "" || participantId == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'id' parameter")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$pull": bson.M{
			"participants": participantId,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err := collection.FindOneAndUpdate(ctx, bson.M{"_id": meetingId}, update, opts).Decode(&meetingSummary)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, ConvertSummaryToFull(meetingSummary))
}

func AddAttachmentToMeeting(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	meetingId := vars["meetingId"]
	attachmentId := vars["attachmentId"]

	if meetingId == "" || attachmentId == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'id' parameter")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$addToSet": bson.M{
			"attachments": attachmentId,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err := collection.FindOneAndUpdate(ctx, bson.M{"_id": meetingId}, update, opts).Decode(&meetingSummary)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, ConvertSummaryToFull(meetingSummary))
}

func RemoveAttachmentFromMeeting(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	meetingId := vars["meetingId"]
	attachmentId := vars["attachmentId"]
	if meetingId == "" || attachmentId == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'id' parameter")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	update := bson.M{
		"$pull": bson.M{
			"attachments": attachmentId,
		},
	}

	var meetingSummary MeetingSummary

	opts := options.FindOneAndUpdate().SetReturnDocument(options.After)
	err := collection.FindOneAndUpdate(ctx, bson.M{"_id": meetingId}, update, opts).Decode(&meetingSummary)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error fetching updated meeting")
		return
	}

	respondWithJSON(w, http.StatusOK, ConvertSummaryToFull(meetingSummary))
}

func GetMeetingsByIds(w http.ResponseWriter, r *http.Request) {
	idsParam := r.URL.Query().Get("ids")
	if idsParam == "" {
		respondWithError(w, http.StatusBadRequest, "Missing 'ids' query parameter")
		return
	}

	ids := strings.Split(idsParam, ",")
	if len(ids) == 0 {
		respondWithError(w, http.StatusBadRequest, "No IDs provided")
		return
	}

	collection := database.Collection("meetings")
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	filter := bson.M{
		"_id": bson.M{
			"$in": ids,
		},
	}

	cursor, err := collection.Find(ctx, filter)
	if err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error fetching meetings")
		return
	}
	defer cursor.Close(ctx)

	var meetingSummaries []MeetingSummary
	if err = cursor.All(ctx, &meetingSummaries); err != nil {
		respondWithError(w, http.StatusInternalServerError, "Error decoding meetings")
		return
	}

	var meetings []Meeting
	for _, meetingSummary := range meetingSummaries {
		meetings = append(meetings, ConvertSummaryToFull(meetingSummary))
	}

	respondWithJSON(w, http.StatusOK, meetingSummaries)
}

func ConvertSummaryToFull(meetingSummary MeetingSummary) Meeting {
	parsedDateTime, err := parseCustomDateTime(meetingSummary.DateTime)
	if err != nil {
		parsedDateTime = time.Now()
	}

	var meeting = Meeting{
		ID:           meetingSummary.ID,
		Title:        meetingSummary.Title,
		Details:      meetingSummary.Details,
		Location:     meetingSummary.Location,
		DateTime:     parsedDateTime,
		Calendars:    []Calendar{},
		Participants: []Participant{},
		Attachments:  []Attachment{},
	}

	if len(meetingSummary.Calendars) != 0 {
		meeting.Calendars = GetCalendarsByIds(meetingSummary.Calendars)
	}

	if len(meetingSummary.Participants) != 0 {
		meeting.Participants = getParticipantsByIds(meetingSummary.Participants)
	}

	if len(meetingSummary.Attachments) != 0 {
		meeting.Attachments = GetAttachmentsByIds(meetingSummary.Attachments)
	}

	return meeting
}

func respondWithError(w http.ResponseWriter, code int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(map[string]string{"error": message})
}

func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(payload)
}
