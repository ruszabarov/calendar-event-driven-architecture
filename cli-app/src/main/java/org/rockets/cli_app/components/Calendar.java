package org.rockets.cli_app.components;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Calendar {
    private final String id;
    private String title;
    private String details;
    private List<Meeting> meetings = new ArrayList<>();

    public Calendar(String calendarId) {
        this.id = calendarId;
    }

    public Calendar(String calendarId, String title, String details) {
        this(calendarId);
        this.title = title;
        this.details = details;
    }

    @JsonCreator
    public Calendar(
            @JsonProperty("id") String calendarId,
            @JsonProperty("title") String title,
            @JsonProperty("details") String details,
            @JsonProperty("meetings") List<Meeting> meetings) {
        this.id = calendarId;
        this.title = title;
        this.details = details;
        this.meetings = meetings != null ? meetings : new ArrayList<>();
    }


    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public List<Meeting> getMeetings() {
        return this.meetings;
    }

    public void setMeetings(List<Meeting> meetings) {
        this.meetings = meetings;
    }

    public void addMeeting(Meeting meeting) {
        if (meeting.getId() != null && !meetings.contains(meeting)) {
            meetings.add(meeting);
        }
    }

    public void removeMeeting(Meeting meeting) {
        if (meeting != null) {
            meetings.remove(meeting);
        }
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Calendar calendar = (Calendar) o;
        return Objects.equals(id, calendar.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "(Calendar) id: " + getId() + " | title: " + getTitle() + " | details: " + getDetails();
    }

    public String meetingsToString() {
        StringBuilder result = new StringBuilder("Meetings:\n");

        for (Meeting m : getMeetings()) {
            result.append("\t").append(m.toString()).append("\n");
        }

        return result.toString();
    }
}
