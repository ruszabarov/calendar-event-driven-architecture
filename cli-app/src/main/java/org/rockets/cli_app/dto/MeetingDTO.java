package org.rockets.cli_app.dto;

import org.rockets.cli_app.components.Calendar;

import java.util.ArrayList;
import java.util.List;

public class MeetingDTO {
    private final String meetingId;
    private String title;
    private String datetime;
    private String location;
    private String details;
    private List<String> participants = new ArrayList<>();
    private List<String> attachments = new ArrayList<>();

    private List<Calendar> calendars = new ArrayList<>();

    public MeetingDTO(String uuid) {
        this.meetingId = uuid;
    }

    public MeetingDTO(String meetingId, String title, String dateTime, String location, String details) {
        this(meetingId);
        this.title = title;
        this.datetime = dateTime;
        this.location = location;
        this.details = details;
    }

    public MeetingDTO(String meetingId, String title, String dateTime, String location, String details, List<String> participants) {
        this(meetingId, title, dateTime, location, details);
        this.participants = participants;
    }

    public String getMeetingId() {
        return meetingId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDatetime() {
        return datetime;
    }

    public void setDatetime(String datetime) {
        this.datetime = datetime;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public List<String> getParticipants() {
        return participants;
    }

    public void setParticipants(List<String> participants) {
        this.participants = participants;
    }

    public List<String> getAttachments() {
        return attachments;
    }

    public void setAttachments(List<String> attachments) {
        this.attachments = attachments;
    }

    public void addParticipant(String participant) {
        participants.add(participant);
    }

    public void removeParticipant(String participant) {
        participants.remove(participant);
    }

    public void addAttachment(String attachment) {
        attachments.add(attachment);
    }

    public void removeAttachment(String attachment) {
        attachments.remove(attachment);
    }

    public List<Calendar> getCalendars() {
        return this.calendars;
    }

    public void setCalendars(List<Calendar> calendars) {
        this.calendars = calendars;
    }

    public void addCalendar(Calendar calendar) {
        if (!this.calendars.contains(calendar)) {
            this.calendars.add(calendar);
        }
    }

    public void removeCalendar(Calendar calendar) {
        if (calendar != null) {
            this.calendars.remove(calendar);
        }
    }

}