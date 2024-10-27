package org.rockets.cli_app.components;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class Meeting {
    private final String id;
    private String title;
    private String dateTime;
    private String location;
    private String details;
    private List<Participant> participants = new ArrayList<>();
    private List<Attachment> attachments = new ArrayList<>();
    private List<Calendar> calendars = new ArrayList<>();

    public Meeting(String id) {
        this.id = id;
    }

    @JsonCreator
    public Meeting(
            @JsonProperty("id") String id,
            @JsonProperty("title") String title,
            @JsonProperty("datetime") String dateTime,
            @JsonProperty("location") String location,
            @JsonProperty("details") String details,
            @JsonProperty("attachments") List<Attachment> attachments,
            @JsonProperty("participants") List<Participant> participants,
            @JsonProperty("calendars") List<Calendar> calendars) {
        this.id = id;
        this.title = title;
        this.dateTime = dateTime;
        this.location = location;
        this.details = details;
        this.participants = participants != null ? participants : new ArrayList<>();
        this.attachments = attachments != null ? attachments : new ArrayList<>();
        this.calendars = calendars != null ? calendars : new ArrayList<>();
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

    public String getDateTime() {
        return dateTime;
    }

    public void setDateTime(String dateTime) {
        this.dateTime = dateTime;
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

    public List<Participant> getParticipants() {
        return participants;
    }

    public void setParticipants(List<Participant> participants) {
        this.participants = participants;
    }

    public List<Attachment> getAttachments() {
        return attachments;
    }

    public void setAttachments(List<Attachment> attachments) {
        this.attachments = attachments;
    }

    public List<Calendar> getCalendars() {
        return calendars;
    }

    public void setCalendars(List<Calendar> calendars) {
        this.calendars = calendars;
    }

    public void addParticipant(Participant participant) {
        if (participant != null && participant.getId() != null && !participants.contains(participant)) {
            participants.add(participant);
        }
    }

    public void removeParticipant(Participant participant) {
        participants.remove(participant);
    }

    public void addAttachment(Attachment attachment) {
        if (attachment != null && attachment.getId() != null && !attachments.contains(attachment)) {
            attachments.add(attachment);
        }
    }

    public void removeAttachment(Attachment attachment) {
        attachments.remove(attachment);
    }

    public void addCalendar(Calendar calendar) {
        if (calendar != null && calendar.getId() != null && !calendars.contains(calendar)) {
            calendars.add(calendar);
        }
    }

    public void removeCalendar(Calendar calendar) {
        calendars.remove(calendar);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Meeting meeting = (Meeting) o;
        return Objects.equals(id, meeting.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "(Meeting) id: " + getId() + " | title: " + getTitle() + " | date: "
                + getDateTime() + " | location: " + getLocation() + " | details: " + getDetails();
    }

    public String calendarsToString() {
        StringBuilder result = new StringBuilder("Calendars:\n");

        for (Calendar c : getCalendars()) {
            result.append("\t").append(c.toString()).append("\n");
        }

        return result.toString();
    }

    public String attachmentsToString() {
        StringBuilder result = new StringBuilder("Attachments:\n");

        for (Attachment a : getAttachments()) {
            result.append("\t").append(a.toString()).append("\n");
        }

        return result.toString();
    }

    public String participantsToString() {
        StringBuilder result = new StringBuilder("Participants:\n");

        for (Participant p : getParticipants()) {
            result.append("\t").append(p.toString()).append("\n");
        }

        return result.toString();
    }
}
