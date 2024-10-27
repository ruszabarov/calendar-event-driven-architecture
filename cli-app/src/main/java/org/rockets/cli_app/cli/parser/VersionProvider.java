package org.rockets.cli_app.cli.parser;

import static picocli.CommandLine.IVersionProvider;

public class VersionProvider implements IVersionProvider {

    @Override
    public String[] getVersion() {
        Package javaPackage = VersionProvider.class.getPackage();
        return new String[]{javaPackage.getImplementationTitle() + " v" + javaPackage.getImplementationVersion()};
    }
}
