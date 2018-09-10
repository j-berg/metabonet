"""
Module to accept parameters from user and execute procedures.

Title:

    interface

Imports:

    os: Package to interact with the operating system.
    sys: Package to interact with the interpreter.
    shutil: Package to perform file operations.
    importlib: Package to import packages and modules.
    csv: Package to organize information in text.
    copy: Package to copy objects.
    pickle: Package to preserve information.
    numpy: Package to calculate with arrays of numbers.
    pandas: Package to organize collections of variables.

Classes:

    This module does not contain any classes.

Exceptions:

    This module does not contain any exceptions.

Functions:

    ...

Author:

    Thomas Cameron Waller
    tcameronwaller@gmail.com
    Department of Biochemistry
    University of Utah
    Room 5520C, Emma Eccles Jones Medical Research Building
    15 North Medical Drive East
    Salt Lake City, Utah 84112
    United States of America

License:

    This file is part of project metabonet
    (https://github.com/tcameronwaller/metabonet/).

    MetaboNet supports custom definition of metabolic networks.
    Copyright (C) 2018 Thomas Cameron Waller

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program.
    If not, see <http://www.gnu.org/licenses/>.
"""

###############################################################################
# Notes

###############################################################################
# Installation and importation

# Standard
import argparse
import textwrap

# Relevant

# Custom

import reconciliation
import extrication
import provision
import extraction
import enhancement
import curation
import conversion
import clean

#dir()
#importlib.reload()

###############################################################################
# Functionality

def define_parse_arguments():
    """
    Defines and parses arguments from terminal.

    arguments:

    raises:

    returns:
        (object): arguments from terminal

    """

    # Define arguments.
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            --------------------------------------------------

            Curate model of metabolism for definition of networks.

            --------------------------------------------------
        """),
        epilog=textwrap.dedent("""\

            --------------------------------------------------

            reconciliation procedure

            source
            1. model of human metabolism in
               Systems Biology Markup Language (SBML) format
            2. curation information about metabolites in
               text table with tab delimiters

            product
            ...

            --------------------------------------------------

            adaptation procedure

            source
            ...

            product
            ...

            --------------------------------------------------
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-d", "--directory", dest="directory", type=str, required=True,
        help="Path to directory for source and product files."
    )
    procedure = parser.add_mutually_exclusive_group(required=True)
    procedure.add_argument(
        "-r", "--reconciliation", dest="reconciliation", action="store_true",
        help="Reconcile information from model to MetaNetX."
    )
    procedure.add_argument(
        "-a", "--adaptation", dest="adaptation", action="store_true",
        help="Execute entire adaptation procedure."
    )
    procedure.add_argument(
        "-t", "--extrication", dest="extrication", action="store_true",
        help="Collect information from Human Metabolome Database."
    )
    procedure.add_argument(
        "-p", "--provision", dest="provision", action="store_true",
        help=(
        "Match information from Human Metabolome Database to specific " +
        "metabolites."
        )
    )
    procedure.add_argument(
        "-e", "--extraction", dest="extraction", action="store_true",
        help="Extract information from MetaNetX."
    )
    procedure.add_argument(
        "-m", "--enhancement", dest="enhancement", action="store_true",
        help="Enhance information."
    )
    procedure.add_argument(
        "-c", "--curation", dest="curation", action="store_true",
        help="Curate information."
    )
    procedure.add_argument(
        "-v", "--conversion", dest="conversion", action="store_true",
        help="Convert information to formats for export."
    )
    parser.add_argument(
        "-x", "--clean", dest="clean", action="store_true", required=False,
        help="Clean intermediate files."
    )
    # Parse arguments.
    return parser.parse_args()


###############################################################################
# Procedure


def execute_procedure():
    """
    Function to execute module's main behavior.

    arguments:

    raises:

    returns:

    """

    # Parse arguments from terminal.
    arguments = define_parse_arguments()
    # Execute procedure.
    if arguments.reconciliation:
        # Report status.
        print("... executing reconciliation procedure ...")
        # Execute reconciliation procedure.
        reconciliation.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.adaptation:
        # Report status.
        print("... executing entire adaptation procedure ...")
        # Execute extraction procedure.
        # Report status.
        print("... executing extraction procedure ...")
        extraction.execute_procedure(
            directory=arguments.directory
        )
        # Execute extrication procedure.
        # Report status.
        print("... executing extrication procedure ...")
        extrication.execute_procedure(
            directory=arguments.directory
        )
        # Execute enhancement procedure.
        # Report status.
        print("... executing enhancement procedure ...")
        enhancement.execute_procedure(
            directory=arguments.directory
        )
        # Execute curation procedure.
        # Report status.
        print("... executing curation procedure ...")
        curation.execute_procedure(
            directory=arguments.directory
        )
        # Execute conversion procedure.
        # Report status.
        print("... executing conversion procedure ...")
        conversion.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.extraction:
        # Report status.
        print("... executing extraction procedure ...")
        # Execute extraction procedure.
        extraction.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.extrication:
        # Report status.
        print("... executing extrication procedure ...")
        # Execute extrication procedure.
        extrication.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.provision:
        # Report status.
        print("... executing provision procedure ...")
        # Execute provision procedure.
        provision.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.enhancement:
        # Report status.
        print("... executing enhancement procedure ...")
        # Execute enhancement procedure.
        enhancement.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.curation:
        # Report status.
        print("... executing curation procedure ...")
        # Execute curation procedure.
        curation.execute_procedure(
            directory=arguments.directory
        )
    elif arguments.conversion:
        # Report status.
        print("... executing conversion procedure ...")
        # Execute conversion procedure.
        conversion.execute_procedure(
            directory=arguments.directory
        )
    if arguments.clean:
        # Report status.
        print("... executing clean procedure ...")
        # Execute clean procedure.
        clean.execute_procedure(
            directory=arguments.directory
        )


if (__name__ == "__main__"):
    execute_procedure()