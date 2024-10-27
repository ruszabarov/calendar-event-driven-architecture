package org.rockets.cli_app.components;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Participant {
    private final String id;
    private String name;
    private String email;

    public Participant(String id) {
        this.id = id;
    }

    @JsonCreator
    public Participant(@JsonProperty("id") String id, @JsonProperty("name") String name, @JsonProperty("email") String email) {
        this(id);
        this.name = name;
        this.email = email;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Participant participant = (Participant) o;
        return Objects.equals(id, participant.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "(Participant) id: " + getId() + " | name: " + getName() + " | email: " + getEmail();
    }
}
