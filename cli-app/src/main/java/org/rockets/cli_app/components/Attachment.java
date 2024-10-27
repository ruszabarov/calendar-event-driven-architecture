package org.rockets.cli_app.components;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Attachment {
    private final String id;
    private String url;

    public Attachment(String id) {
        this.id = id;
    }

    @JsonCreator
    public Attachment(@JsonProperty("id") String id, @JsonProperty("url") String url) {
        this(id);
        this.url = url;
    }

    public String getId() {
        return id;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Attachment attachment = (Attachment) o;
        return Objects.equals(id, attachment.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "(Attachment) id: " + getId() + " | url: " + getUrl();
    }
}
