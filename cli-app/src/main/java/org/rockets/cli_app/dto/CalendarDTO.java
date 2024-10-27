package org.rockets.cli_app.dto;

import org.rockets.cli_app.components.Meeting;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class CalendarDTO {
    private final String calendarId;
    private String title;
    private String details;
    private List<String> meetings = new ArrayList<>();

    public CalendarDTO(String calendarId) {
        this.calendarId = calendarId;
    }

    public CalendarDTO(String calendarId, String title, String details) {
        this(calendarId);
        this.title = title;
        this.details = details;
    }

    public CalendarDTO(String calendarId, String title, String details, List<String> meetings) {
        this(calendarId, title, details);
        this.meetings = meetings;
    }

    public String getCalendarId() {
        return calendarId;
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

    public List<String> getMeetings() {
        return this.meetings;
    }

    public void setMeetings(List<String> meetings) {
        this.meetings = meetings;
    }

    public void addMeeting(String meeting) {
        meetings.add(meeting);
    }

    public void removeMeeting(String meeting) {
    meetings.remove(meeting);
    }
}
