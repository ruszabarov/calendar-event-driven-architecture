package org.rockets.cli_app.cli.commands;

import org.rockets.Check;
import org.rockets.cli_app.cli.common.HelpOption;
import org.rockets.cli_app.components.Attachment;
import org.rockets.cli_app.components.Participant;
import org.rockets.cli_app.dto.CalendarDTO;
import org.rockets.cli_app.dto.MeetingDTO;
import org.rockets.cli_app.service.AttachmentService;
import org.rockets.cli_app.service.CalendarService;
import org.rockets.cli_app.service.MeetingService;
import org.rockets.cli_app.service.ParticipantService;
import picocli.CommandLine.Command;
import picocli.CommandLine.Mixin;
import picocli.CommandLine.Option;

import java.util.List;

@Command(
        name = "update",
        description = "Updates records based on ID",
        subcommands = {
                UpdateCommand.UpdateMeetingCommand.class,
                UpdateCommand.UpdateCalendarCommand.class,
                UpdateCommand.UpdateParticipantCommand.class,
                UpdateCommand.UpdateAttachmentCommand.class
        }
)
public class UpdateCommand implements Runnable {

    public UpdateCommand() {
    }

    @Mixin
    private HelpOption helpOption;

    @Override
    public void run() {
        System.out.println("Use one of the subcommands to update a specific type of record.");
    }

    // Subcommand for updating meetings
    @Command(name = "meeting", description = "Update meeting details")
    public static class UpdateMeetingCommand implements Runnable {

        @Option(names = "--id", description = "Meeting ID", required = true)
        private String id;

        @Option(names = "--title", description = "New meeting title")
        private String title;

        @Option(names = "--datetime", description = "New meeting date and time")
        private String dateTime;

        @Option(names = "--location", description = "New meeting location")
        private String location;

        @Option(names = "--details", description = "New meeting details")
        private String details;

        @Option(names = "--add-participantId", description = "Add a Participant ID to the meeting")
        private String addParticipantId;

        @Option(names = "--remove-participantId", description = "Remove a Participant ID from the meeting")
        private String removeParticipantId;

        @Option(names = "--add-attachmentId", description = "Add an Attachment ID to the meeting")
        private String addAttachmentId;

        @Option(names = "--remove-attachmentId", description = "Remove an Attachment ID from the meeting")
        private String removeAttachmentId;

        @Override
        public void run() {
            // Check at least one option is provided
            if (title == null && dateTime == null && location == null && details == null &&
                    addParticipantId == null && removeParticipantId == null &&
                    addAttachmentId == null && removeAttachmentId == null) {
                System.err.println("At least one update option must be specified.");
                return;
            }
            try {
                MeetingService mtgController = new MeetingService();

                MeetingDTO meeting = new MeetingDTO(id);

                if (title != null) {
                    title = Check.limitString(title, 2000);
                    meeting.setTitle(title);
                }
                if (dateTime != null) {
                    if (!Check.validateDateTime(dateTime)) {
                        System.err.println("Invalid date format");
                        return;
                    }
                    meeting.setDatetime(dateTime);
                }
                if (location != null) {
                    Check.limitString(location, 2000);
                    meeting.setLocation(location);
                }
                if (details != null) {
                    Check.limitString(details, 10000);
                    meeting.setDetails(details);
                }
                if (addParticipantId != null) {
                    mtgController.addParticipantsToMeeting(id, List.of(addParticipantId));
                }
                if (removeParticipantId != null) {
                    mtgController.removeParticipantsFromMeeting(id, List.of(removeParticipantId));
                }
                if (addAttachmentId != null) {
                    mtgController.addAttachmentsToMeeting(id, List.of(addAttachmentId));
                }
                if (removeAttachmentId != null) {
                    mtgController.removeAttachmentsFromMeeting(id, List.of(removeAttachmentId));
                }

                mtgController.updateMeetingById(id, meeting);
                System.out.println("Successfully updated meeting (" + id + ")");
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
        }
    }

    // Subcommand for updating calendars
    @Command(name = "calendar", description = "Update calendar details")
    public static class UpdateCalendarCommand implements Runnable {
        @Option(names = "--id", description = "Calendar ID", required = true)
        private String id;

        @Option(names = "--title", description = "New calendar title")
        private String title;

        @Option(names = "--details", description = "New calendar details")
        private String details;

        @Option(names = "--add-meetingId", description = "Add a Meeting ID to the calendar")
        private String addMeetingId;

        @Option(names = "--remove-meetingId", description = "Remove a Meeting ID from the calendar")
        private String removeMeetingId;

        @Override
        public void run() {
            try {
                CalendarService calendarController = new CalendarService();
                CalendarDTO calendar = new CalendarDTO(id);

                // Check if at least one update option is specified
                if (title == null && details == null && addMeetingId == null && removeMeetingId == null) {
                    System.err.println("At least one update option must be specified.");
                    return;
                }

                // Apply updates to the calendar
                if (title != null) {
                    Check.limitString(title, 2000);
                    calendar.setTitle(title);
                }
                if (details != null) {
                    Check.limitString(details, 10000);
                    calendar.setDetails(details);
                }
                if (addMeetingId != null) {
                    calendarController.addMeetingsToCalendar(id, List.of(addMeetingId));
                }
                if (removeMeetingId != null) {
                    calendarController.removeMeetingsFromCalendar(id, List.of(removeMeetingId));
                }
                calendarController.updateCalendarById(id, calendar);
                System.out.println("Successfully updated calendar (" + id + ")");

            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
        }
    }

    // Subcommand for updating participants
    @Command(name = "participant", description = "Update participant details")
    public static class UpdateParticipantCommand implements Runnable {
        @Option(names = "--id", description = "Participant ID", required = true)
        private String id;

        @Option(names = "--name", description = "New participant name")
        private String name;

        @Option(names = "--email", description = "New participant email")
        private String email;

        @Override
        public void run() {
            try {
                ParticipantService participantController = new ParticipantService();
                Participant participant = new Participant(id);

                if (name == null && email == null) {
                    System.err.println("At least one update option must be specified.");
                    return;
                }
                if (name != null) {
                    Check.limitString(name, 600);
                    participant.setName(name);
                }
                if (email != null) {
                    if (!Check.isValidEmail(email)) {
                        System.err.println("Invalid Email");
                        return;
                    }
                    participant.setEmail(email);
                }

                participantController.updateParticipantById(id, participant);
                System.out.println("Successfully updated participant (" + id + ")");
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }

        }
    }

    // Subcommand for updating attachments
    @Command(name = "attachment", description = "Update attachment details")
    public static class UpdateAttachmentCommand implements Runnable {
        @Option(names = "--id", description = "Attachment ID", required = true)
        private String id;

        @Option(names = "--url", description = "New attachment URL")
        private String url;

        @Override
        public void run() {
            try {
                AttachmentService attachmentController = new AttachmentService();
                Attachment attachment = new Attachment(id);

                if (url == null) {
                    System.err.println("At least one update option must be specified.");
                    return;
                }
                if (!Check.isValidURL(url)) {
                    System.err.println("Invalid URL");
                    return;
                }

                attachment.setUrl(url);

                attachmentController.updateAttachmentById(id, attachment);
                System.out.println("Successfully updated attachment (" + id + ")");
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
        }
    }
}
