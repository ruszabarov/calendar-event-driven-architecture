package org.rockets.cli_app.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.rockets.cli_app.components.Calendar;
import org.rockets.cli_app.dto.CalendarDTO;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Objects;

public class CalendarService {

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String baseUrl = "http://localhost:8080";

    public CalendarService() {
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }

    public List<Calendar> getCalendars() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/calendars"))
                .GET()
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
        List<Calendar> apiResponse = objectMapper.readValue(response.body(), new TypeReference<>() {
        });


        return Objects.requireNonNull(apiResponse);
    }

    public Calendar createCalendar(CalendarDTO calendar) throws Exception {
        String requestBody = objectMapper.writeValueAsString(calendar);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/calendars"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        Calendar apiResponse = objectMapper.readValue(response.body(), new TypeReference<Calendar>() {
        });

        return Objects.requireNonNull(apiResponse);
    }

    public void updateCalendarById(String id, CalendarDTO calendar) throws Exception {
        String requestBody = objectMapper.writeValueAsString(calendar);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/calendars/" + id))
                .header("Content-Type", "application/json")
                .method("PUT", HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                .build();

        httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    }

    public void deleteCalendarById(String id) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/calendars/" + id))
                .DELETE()
                .build();

        httpClient.send(request, HttpResponse.BodyHandlers.ofString());
    }

    public Calendar addMeetingsToCalendar(String calendarId, List<String> meetingIds) throws Exception {
        String requestBody = objectMapper.writeValueAsString(meetingIds);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/calendars/" + calendarId + "/addMeetings"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        Calendar apiResponse = objectMapper.readValue(response.body(), new TypeReference<Calendar>() {
        });

        return Objects.requireNonNull(apiResponse);
    }

    public Calendar removeMeetingsFromCalendar(String calendarId, List<String> meetingIds) throws Exception {
        String requestBody = objectMapper.writeValueAsString(meetingIds);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(baseUrl + "/calendars/" + calendarId + "/removeMeetings"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        Calendar apiResponse = objectMapper.readValue(response.body(), new TypeReference<Calendar>() {
        });

        return Objects.requireNonNull(apiResponse);
    }
}