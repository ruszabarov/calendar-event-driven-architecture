package org.rockets.cli_app;

import org.rockets.cli_app.cli.parser.CommandLineParser;
import picocli.CommandLine;
import picocli.CommandLine.Command;

public class CliApplication {

    public static void main(String[] args) {
        CommandLineParser parser = new CommandLineParser();
        CommandLine commandLine = new CommandLine(parser);

        int exitCode = commandLine.execute(args);

        System.exit(exitCode);

    }
}
