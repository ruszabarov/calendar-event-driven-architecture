package org.rockets.cli_app.cli.commands;

import org.rockets.cli_app.cli.common.HelpOption;
import org.rockets.cli_app.components.Attachment;
import org.rockets.cli_app.components.Calendar;
import org.rockets.cli_app.components.Meeting;
import org.rockets.cli_app.components.Participant;
import org.rockets.cli_app.service.AttachmentService;
import org.rockets.cli_app.service.CalendarService;
import org.rockets.cli_app.service.MeetingService;
import org.rockets.cli_app.service.ParticipantService;
import picocli.CommandLine.Command;
import picocli.CommandLine.Mixin;
import picocli.CommandLine.Option;

import java.util.List;

@Command(
        name = "list",
        description = "Lists records for different types (Meetings, Calendars, Participants, Attachments)",
        subcommands = {
                ListCommand.ListMeetingCommand.class,
                ListCommand.ListCalendarCommand.class,
                ListCommand.ListParticipantCommand.class,
                ListCommand.ListAttachmentCommand.class
        }
)
public class ListCommand implements Runnable {

    public ListCommand() {
    }

    @Mixin
    private HelpOption helpOption;

    @Override
    public void run() {
        System.out.println("Use one of the subcommands to list records for a specific type.");
    }

    // Subcommand for listing meetings
    @Command(name = "meeting", description = "List meetings")
    public static class ListMeetingCommand implements Runnable {

        @Override
        public void run() {
            try {
                MeetingService mtgController = new MeetingService();

                List<Meeting> meetings = mtgController.getMeetings();
                System.out.println("Listing all meetings.");
                for (Meeting meeting : meetings) {
                    System.out.println(meeting);
                    System.out.println(meeting.calendarsToString());
                    System.out.println(meeting.participantsToString());
                    System.out.println(meeting.attachmentsToString());
                }
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
        }
    }

    // Subcommand for listing calendars
    @Command(name = "calendar", description = "List calendars, optionally filtered by UUID")
    public static class ListCalendarCommand implements Runnable {

        @Option(names = "--calendarId", description = "Optional UUID of the calendar to filter")
        private String calendarId;

        @Override
        public void run() {
            try {
                CalendarService calendarController = new CalendarService();

                List<Calendar> calendars = calendarController.getCalendars();
                System.out.println("Listing all calendars.");
                for (Calendar calendar : calendars) {
                    System.out.println(calendar);
                    System.out.println(calendar.meetingsToString());
                }

            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
        }
    }

    // Subcommand for listing participants
    @Command(name = "participant", description = "List participants, optionally filtered by UUID")
    public static class ListParticipantCommand implements Runnable {

        @Option(names = "--participantId", description = "Optional UUID of the participant to filter")
        private String participantId;

        @Override
        public void run() {
            try {
                ParticipantService participantController = new ParticipantService();

                List<Participant> participants = participantController.getParticipants();
                System.out.println("Listing all participants.");
                for (Participant participant : participants) {
                    System.out.println(participant);
                }

            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
        }
    }

    // Subcommand for listing attachments
    @Command(name = "attachment", description = "List attachments, optionally filtered by UUID")
    public static class ListAttachmentCommand implements Runnable {

        @Option(names = "--attachmentId", description = "Optional UUID of the attachment to filter")
        private String attachmentId;

        @Override
        public void run() {
            try {
                AttachmentService attachmentController = new AttachmentService();

                List<Attachment> attachments = attachmentController.getAttachments();
                System.out.println("Listing all attachments.");
                for (Attachment attachment : attachments) {
                    System.out.println(attachment);
                }

            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }

        }
    }
}

