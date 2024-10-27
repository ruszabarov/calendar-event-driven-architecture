package org.rockets.cli_app.cli.parser;

import org.rockets.cli_app.cli.commands.CreateCommand;
import org.rockets.cli_app.cli.commands.DeleteCommand;
import org.rockets.cli_app.cli.commands.ListCommand;
import org.rockets.cli_app.cli.commands.UpdateCommand;
import org.rockets.cli_app.cli.common.HelpOption;
import picocli.CommandLine.Command;
import picocli.CommandLine.Mixin;
import picocli.CommandLine.Option;

@Command(
        name = "CLIManager",
        subcommands = {CreateCommand.class, ListCommand.class, UpdateCommand.class, DeleteCommand.class},
        versionProvider = VersionProvider.class,
        mixinStandardHelpOptions = true, // Enables -h and --help options
        description = "CLI for managing meetings, calendars, participants, and attachments."
)
public class CommandLineParser implements Runnable {
    @Mixin
    private HelpOption helpOption;

    @Option(names = {"-v", "--version"}, versionHelp = true, description = "Print version information and exit.")
    private boolean versionHelpRequested;

    @Override
    public void run() {
        // Logic when no specific command is provided
        if (versionHelpRequested) {
            System.out.println("CLI Version 1.0.0");
        } else {
            // This can be left empty as subcommands will handle their own logic
            System.out.println("Use a subcommand. Use --help for more information.");
        }
    }
}

