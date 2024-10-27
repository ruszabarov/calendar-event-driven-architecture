package org.rockets.cli_app.cli.commands;

import org.rockets.cli_app.cli.common.HelpOption;
import org.rockets.cli_app.service.AttachmentService;
import org.rockets.cli_app.service.CalendarService;
import org.rockets.cli_app.service.MeetingService;
import org.rockets.cli_app.service.ParticipantService;
import picocli.CommandLine.Command;
import picocli.CommandLine.Mixin;
import picocli.CommandLine.Option;

@Command(
        name = "delete",
        description = "Deletes a record by UUID",
        subcommands = {
                DeleteCommand.DeleteMeetingCommand.class,
                DeleteCommand.DeleteCalendarCommand.class,
                DeleteCommand.DeleteParticipantCommand.class,
                DeleteCommand.DeleteAttachmentCommand.class
        }
)
public class DeleteCommand implements Runnable {

    public DeleteCommand() {
    }

    @Mixin
    private HelpOption helpOption;

    @Override
    public void run() {
        System.out.println("Use one of the subcommands to delete a specific record type (meeting, calendar, participant, attachment).");
    }

    // Subcommand for deleting meetings
    @Command(name = "meeting", description = "Delete a meeting by its UUID")
    public static class DeleteMeetingCommand implements Runnable {

        @Option(names = "--meetingId", description = "UUID of the meeting to delete", required = true)
        private String meetingId;

        @Override
        public void run() {
            try {
                MeetingService meetingService = new MeetingService();
                meetingService.deleteMeetingById(meetingId);
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
            System.out.println("Deleting meeting with UUID = " + meetingId);
        }
    }

    // Subcommand for deleting calendars
    @Command(name = "calendar", description = "Delete a calendar by its UUID")
    public static class DeleteCalendarCommand implements Runnable {

        @Option(names = "--calendarId", description = "UUID of the calendar to delete", required = true)
        private String calendarId;

        @Override
        public void run() {
            try {
                CalendarService calendarService = new CalendarService();
                calendarService.deleteCalendarById(calendarId);
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
            System.out.println("Deleting calendar with UUID = " + calendarId);
        }
    }

    // Subcommand for deleting participants
    @Command(name = "participant", description = "Delete a participant by its UUID")
    public static class DeleteParticipantCommand implements Runnable {

        @Option(names = "--participantId", description = "UUID of the participant to delete", required = true)
        private String participantId;

        @Override
        public void run() {
            try {
                ParticipantService participantService = new ParticipantService();
                participantService.deleteParticipantById(participantId);
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
            System.out.println("Deleting participant with UUID = " + participantId);
        }
    }

    // Subcommand for deleting attachments
    @Command(name = "attachment", description = "Delete an attachment by its UUID")
    public static class DeleteAttachmentCommand implements Runnable {

        @Option(names = "--attachmentId", description = "UUID of the attachment to delete", required = true)
        private String attachmentId;

        @Override
        public void run() {
            try {
                AttachmentService attachmentService = new AttachmentService();
                attachmentService.deleteAttachmentById(attachmentId);
            } catch (Exception e) {
                System.err.println("An error occurred: " + e.getMessage());
            }
            System.out.println("Deleting attachment with UUID = " + attachmentId);
        }
    }
}

