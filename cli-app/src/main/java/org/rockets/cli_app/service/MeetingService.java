package org.rockets.cli_app.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.rockets.cli_app.components.Meeting;
import org.rockets.cli_app.dto.MeetingDTO;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.Objects;

public class MeetingService {

    private final HttpClient httpClient = HttpClient.newHttpClient();
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final String baseUrl = "http://localhost:8080";

    public List<Meeting> getMeetings() throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings"))
                .GET()
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        List<Meeting> apiResponse = objectMapper.readValue(response.body(), objectMapper.getTypeFactory().constructParametricType(List.class, Meeting.class));
        return Objects.requireNonNull(apiResponse);
    }

    public Meeting createMeeting(MeetingDTO meetingDTO) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(meetingDTO)))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        Meeting apiResponse = objectMapper.readValue(response.body(), objectMapper.getTypeFactory().constructParametricType(List.class, Meeting.class));
        return Objects.requireNonNull(apiResponse);
    }

    public void updateMeetingById(String id, MeetingDTO meeting) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings/" + id))
                .header("Content-Type", "application/json")
                .method("PUT", HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(meeting)))
                .build();

        httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    }

    public void deleteMeetingById(String id) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings/" + id))
                .DELETE()
                .build();

        httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    }

    public Meeting addParticipantsToMeeting(String meetingId, List<String> participantIds) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings/" + meetingId + "/addMeetings"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(participantIds)))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        Meeting apiResponse = objectMapper.readValue(response.body(), objectMapper.getTypeFactory().constructParametricType(List.class, Meeting.class));
        return Objects.requireNonNull(apiResponse);
    }

    public Meeting removeParticipantsFromMeeting(String meetingId, List<String> participantIds) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings/" + meetingId + "/removeMeetings"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(participantIds)))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        Meeting apiResponse = objectMapper.readValue(response.body(), objectMapper.getTypeFactory().constructParametricType(List.class, Meeting.class));
        return Objects.requireNonNull(apiResponse);
    }

    public Meeting addAttachmentsToMeeting(String meetingId, List<String> attachmentIds) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings/" + meetingId + "/addAttachments"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(attachmentIds)))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        Meeting apiResponse = objectMapper.readValue(response.body(), objectMapper.getTypeFactory().constructParametricType(List.class, Meeting.class));
        return Objects.requireNonNull(apiResponse);
    }

    public Meeting removeAttachmentsFromMeeting(String meetingId, List<String> attachmentIds) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/meetings/" + meetingId + "/removeAttachments"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(objectMapper.writeValueAsString(attachmentIds)))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        Meeting apiResponse = objectMapper.readValue(response.body(), objectMapper.getTypeFactory().constructParametricType(List.class, Meeting.class));
        return Objects.requireNonNull(apiResponse);
    }
}