"""
Module to provide template of common structure of modules.

Title:

    template

Imports:

    os: Package to interact with the operating system.
    sys: Package to interact with the interpreter.
    shutil: Package to perform file operations.
    importlib: Package to import packages and modules.
    argparse: Package to interpret user parameters from terminal.
    textwrap: Package to format text.
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

# Relevant

# Custom

#dir()
#importlib.reload()

###############################################################################
# Functionality


def read_source(directory=None):
    """
    Reads and organizes source information from file

    arguments:
        directory (str): directory of source files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_compartments_curation = os.path.join(
        directory, "curation_compartments.tsv"
    )
    path_processes_curation = os.path.join(directory, "curation_processes.tsv")
    path_reactions_curation = os.path.join(directory, "curation_reactions.tsv")
    path_metabolites_curation = os.path.join(
        directory, "curation_metabolites.tsv"
    )
    path = os.path.join(directory, "enhancement")
    path_compartments = os.path.join(path, "enhancement_compartments.pickle")
    path_processes = os.path.join(path, "enhancement_processes.pickle")
    path_reactions = os.path.join(path, "enhancement_reactions.pickle")
    path_metabolites = os.path.join(path, "enhancement_metabolites.pickle")
    # Read information from file.
    with open(path_compartments, "rb") as file_source:
        compartments = pickle.load(file_source)
    with open(path_processes, "rb") as file_source:
        processes = pickle.load(file_source)
    with open(path_reactions, "rb") as file_source:
        reactions = pickle.load(file_source)
    with open(path_metabolites, "rb") as file_source:
        metabolites = pickle.load(file_source)
    compartments_curation = utility.read_file_table(
        path_file=path_compartments_curation,
        names=None,
        delimiter="\t"
    )
    processes_curation = utility.read_file_table(
        path_file=path_processes_curation,
        names=None,
        delimiter="\t"
    )
    reactions_curation = utility.read_file_table(
        path_file=path_reactions_curation,
        names=None,
        delimiter="\t"
    )
    metabolites_curation = utility.read_file_table(
        path_file=path_metabolites_curation,
        names=None,
        delimiter="\t"
    )
    # Compile and return information.
    return {
        "compartments": compartments,
        "processes": processes,
        "reactions": reactions,
        "metabolites": metabolites,
        "compartments_curation": compartments_curation,
        "processes_curation": processes_curation,
        "reactions_curation": reactions_curation,
        "metabolites_curation": metabolites_curation,
    }


def curate_compartments(
    compartments_curation=None, compartments_original=None,
    reactions_original=None
):
    """
    Curates information about specific compartments and relevant reactions.

    arguments:
        compartments_curation (list<dict<str>>): information to change about
            specific compartments
        compartments_original (dict<dict>): information about compartments
        reactions_original (dict<dict>): information about reactions

    returns:
        (dict<dict<dict>>): information about compartments and reactions

    raises:

    """

    # Copy information.
    compartments_novel = copy.deepcopy(compartments_original)
    reactions_novel = copy.deepcopy(reactions_original)
    for record in compartments_curation:
        # Interpretation.
        identifier_original = record["identifier_original"]
        identifier_novel = record["identifier_novel"]
        name_original = record["name_original"]
        name_novel = record["name_novel"]
        # Determine method to change information.
        match_identifiers = identifier_original == identifier_novel
        match_names = name_original == name_novel
        if identifier_novel is None:
            if identifier_original in compartments_novel:
                # Remove compartment.
                del compartments_novel[identifier_original]
                # Removal of a compartment justifies removal of any reactions
                # within that compartment.
                # Remove relevant reactions.
                removals = []
                for key, record_reaction in reactions_novel.items():
                    # Determine whether any of reaction's participants are in
                    # the compartment.
                    match = determine_reaction_compartment(
                        compartment=identifier_original,
                        reaction=record_reaction
                    )
                    if match:
                        # Remove
                        removals.append(key)
                for removal in removals:
                    del reactions_novel[removal]
        elif not match_names:
            # Change name.
            if identifier_original in compartments_novel:
                compartments_novel[identifier_original]["name"] = name_novel
    # Compile and return information.
    return {
        "compartments": compartments_novel,
        "reactions": reactions_novel
    }


def determine_reaction_compartment(compartment=None, reaction=None):
    """
    Determines whether any of reaction's participants are in a compartment

    arguments:
        compartment (str): identifier of a compartment
        reaction (dict): information about a reaction

    returns:
        (bool): whether any of reaction's participants are in the compartment

    raises:

    """

    participants = reaction["participants"]
    for participant in participants:
        if participant["compartment"] == compartment:
            return True
    return False


def curate_processes(
    processes_curation=None, processes_original=None, reactions_original=None
):
    """
    Curates information about specific processes and relevant reactions.

    arguments:
        processes_curation (list<dict<str>>): information to change about
            specific processes
        processes_original (dict<dict>): information about processes
        reactions_original (dict<dict>): information about reactions

    returns:
        (dict<dict<dict>>): information about processes and reactions

    raises:

    """

    # Copy information.
    processes_novel = copy.deepcopy(processes_original)
    reactions_novel = copy.deepcopy(reactions_original)
    for record in processes_curation:
        # Interpretation.
        identifier_original = record["identifier_original"]
        identifier_novel = record["identifier_novel"]
        name_original = record["name_original"]
        name_novel = record["name_novel"]
        # Determine method to change information.
        match_identifiers = identifier_original == identifier_novel
        match_names = name_original == name_novel
        if identifier_novel is None:
            if identifier_original in processes_novel:
                # Remove process.
                del processes_novel[identifier_original]
                # Removal of a process does not justify removal of any
                # reactions that participate in that process.
        else:
            if not match_identifiers:
                # Change identifier.
                # Remove original.
                if identifier_original in processes_novel:
                    del processes_novel[identifier_original]
                # Replace with novel.
                if identifier_novel in processes_novel:
                    for reaction in reactions_novel.values():
                        processes = reaction["processes"]
                        if identifier_original in processes:
                            for index, process in enumerate(processes):
                                if process == identifier_original:
                                    processes[index] = identifier_novel
                            # Collect unique values.
                            processes_unique = utility
                                .collect_unique_elements(processes)
                            reaction["processes"] = processes_unique
            if not match_names:
                # Change name.
                if identifier_novel in processes_novel:
                    processes_novel[identifier_novel]["name"] = name_novel
    # Compile and return information
    return {
        "processes": processes_novel,
        "reactions": reactions_novel
    }


def curate_metabolites(
    metabolites_curation=None, metabolites_original=None, reactions_original=None
):
    """
    Curates information about specific metabolites and relevant reactions.

    arguments:
        metabolites_curation (list<dict<str>>): information to change about
            specific metabolites
        metabolites_original (dict<dict>): information about metabolites
        reactions_original (dict<dict>): information about reactions

    returns:
        (dict<dict<dict>>): information about metabolites and reactions

    raises:

    """

    # Copy information.
    metabolites_novel = copy.deepcopy(metabolites_original)
    reactions_novel = copy.deepcopy(reactions_original)
    for record in metabolites_curation:
        # Interpretation.
        identifier_original = record["identifier_original"]
        identifier_novel = record["identifier_novel"]
        name_original = record["name_original"]
        name_novel = record["name_novel"]
        # Determine method to change information.
        match_identifiers = identifier_original == identifier_novel
        match_names = name_original == name_novel
        if identifier_novel is None:
            if identifier_original in metabolites_novel:
                # Remove metabolite.
                del metabolites_novel[identifier_original]
                # Remove metabolite from relevant reactions.
                for reaction in reactions_novel.values():
                    participants = reaction["participants"]
                    for index, party in enumerate(participants):
                        if party["metabolite"] == identifier_original:
                            del participants[index]
        else:
            if not match_identifiers:
                # Change identifier.
                # Remove original.
                if identifier_original in metabolites_novel:
                    del metabolites_novel[identifier_original]
                # Replace with novel.
                if identifier_novel in metabolites_novel:
                    # Replace metabolite in relevant reactions.
                    for reaction in reactions_novel.values():
                        participants = reaction["participants"]
                        for party in participants:
                            if party["metabolite"] == identifier_original:
                                party["metabolite"] = identifier_novel
            if not match_names:
                # Change name.
                if identifier_novel in metabolites_novel:
                    metabolites_novel[identifier_novel]["name"] = name_novel
    # Compile and return information.
    return {
        "metabolites": metabolites_novel,
        "reactions": reactions_novel
    }


def curate_reactions(reactions_curation=None, reactions_original=None):
    """
    Curates information about specific reactions.

    arguments:
        reactions_curation (list<dict<str>>): information to change about
            specific reactions
        reactions_original (dict<dict>): information about reactions

    returns:
        (dict<dict>): information about reactions

    raises:

    """

    # Copy information.
    reactions_novel = copy.deepcopy(reactions_original)
    for record in changer_reactions:
        # Interpretation.
        identifier_original = record["identifier_original"]
        identifier_novel = record["identifier_novel"]
        name_original = record["name_original"]
        name_novel = record["name_novel"]
        # Determine method to change information.
        match_identifiers = identifier_original == identifier_novel
        match_names = name_original == name_novel
        if identifier_novel is None:
            if identifier_original in reactions_novel:
                # Remove reaction.
                del reactions_novel[identifier_original]
        elif not match_names:
            # Change name.
            if identifier_original in reactions_novel:
                reactions_novel[identifier_original]["name"] = name_novel
    # Return information
    return reactions_novel


###############################################################################
# Procedure


def execute_procedure(directory=None):
    """
    Function to execute module's main behavior.

    The purpose of this procedure is to curate information about metabolic
    entities and sets.

    arguments:
        directory (str): path to directory for source and product files

    raises:

    returns:

    """

    # Read source information from file.
    source = read_source(directory=origin)
    # Change procedures allow custom changes to metabolites and reactions
    # Curate information about compartments.
    compartments_reactions = curate_compartments(
        compartments_curation=source["compartments_curation"],
        compartments_original=source["compartments"],
        reactions_original=source["reactions"]
    )
    # Curate information about processes.
    processes_reactions = curate_processes(
        processes_curation=source["processes_curation"],
        processes_original=source["processes"],
        reactions_original=compartments_reactions["reactions"]
    )
    # Curate information about metabolites.
    metabolites_reactions = curate_metabolites(
        metabolites_curation=source["metabolites_curation"],
        metabolites_original=source["metabolites"],
        reactions_original=processes_reactions["reactions"]
    )
    # Curate information about reactions.
    reactions = curate_reactions(
        reactions_curation=source["reactions_curation"],
        reactions_original=metabolites_reactions["reactions"]
    )
    # Compile information.
    information = {
        "compartments": compartments_reactions["compartments"],
        "processes": processes_reactions["processes"],
        "metabolites": metabolites_reactions["metabolites"],
        "reactions": reactions
    }
