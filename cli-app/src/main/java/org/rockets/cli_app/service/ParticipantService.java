package org.rockets.cli_app.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.rockets.cli_app.components.Participant;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Objects;

public class ParticipantService {

    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String baseUrl = "http://localhost:8080";

    public ParticipantService() {
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }

    public List<Participant> getParticipants() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/participants"))
                    .GET()
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            List<Participant> apiResponse = objectMapper.readValue(response.body(), new TypeReference<>() {
            });

            return Objects.requireNonNull(apiResponse);
        } catch (Exception e) {
            throw new RuntimeException("Error fetching participants", e);
        }
    }

    public Participant createParticipant(Participant participant) {
        try {
            String requestBody = objectMapper.writeValueAsString(participant);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/participants"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            Participant apiResponse = objectMapper.readValue(response.body(), new TypeReference<>() {
            });

            return Objects.requireNonNull(apiResponse);
        } catch (Exception e) {
            throw new RuntimeException("Error creating participant", e);
        }
    }

    public void updateParticipantById(String id, Participant participant) {
        try {
            String requestBody = objectMapper.writeValueAsString(participant);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/participants/" + id))
                    .header("Content-Type", "application/json")
                    .method("PUT", HttpRequest.BodyPublishers.ofString(requestBody, StandardCharsets.UTF_8))
                    .build();

            httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (Exception e) {
            throw new RuntimeException("Error updating participant", e);
        }
    }

    public void deleteParticipantById(String id) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(baseUrl + "/participants/" + id))
                    .DELETE()
                    .build();

            httpClient.send(request, HttpResponse.BodyHandlers.discarding());
        } catch (Exception e) {
            throw new RuntimeException("Error deleting participant", e);
        }
    }
}
