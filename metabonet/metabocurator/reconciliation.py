"""
Curate metabolic model Recon 2M.2 for reconciliation to MetaNetX.

Title:
    reconciliation

Imports:
    os: This module is from The Python Standard Library. It contains
        difinitions of tools to interact with the operating system.
    sys: This module is from The Python Standard Library. It contains
        definitions of tools to interact with the interpreter.
    shutil: This module is from The Python Standard Library. It contains
        definitions of tools for file operations.
    importlib: This module is from The Python Standard library. It contains
        definitions of tools to import packages and modules.

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
    Scientific Computing and Imaging Institute
    University Of Utah
    Room 4720 Warnock Engineering Building
    72 South Central Campus Drive
    Salt Lake City, Utah 84112
    United States of America

License:

    This file is part of project Profondeur
    (https://github.com/tcameronwaller/profondeur/).

    Profondeur supports custom definition and visual exploration of metabolic
    networks.
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

# The purpose of this procedure is to improve reconciliation of information
# about metabolic sets and entities from the Recon 2M.2 model of human
# metabolism to MetaNetX's name space.
# In the process of reconciliation, MetaNetX also exerts some checks and
# changes for quality.

###############################################################################
# Installation and importation of packages and modules


# Packages and modules from the python standard library

import os
#import sys
import shutil
#import importlib
import re
import csv
import xml.etree.ElementTree as et
import copy

# Packages and modules from third parties

# Packages and modules from local source
import metabonet.utility as utility
import metabonet.metabocurator.collection as metabocurator_collection

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
    path_source = os.path.join(directory, "source")
    path_customization = os.path.join(path_source, "customization")
    path_model = os.path.join(path_source, "recon2m2.xml")
    path_compartments = os.path.join(
        path_customization, "reconciliation_compartments.tsv"
    )
    path_metabolites = os.path.join(
        path_customization, "reconciliation_metabolites.tsv"
    )
    # Read information from file.
    content = et.parse(path_model)
    curation_compartments = utility.read_file_table(
        path_file=path_compartments,
        names=None,
        delimiter="\t"
    )
    curation_metabolites = utility.read_file_table(
        path_file=path_metabolites,
        names=None,
        delimiter="\t"
    )
    # Compile and return information.
    return {
        "content": content,
        "curation_compartments": curation_compartments,
        "curation_metabolites": curation_metabolites
    }


def count_model_sets_entities(content=None):
    """
    Counts compartments, reactions, and metabolites in model.

    arguments:
        content (object): content from file in Systems Biology Markup Language
            (XML)

    raises:

    returns:
        (dict<int>): summary

    """

    # Copy and interpret content.
    reference = metabocurator_collection.copy_interpret_content_recon2m2(
        content=content
    )
    # Count compartments.
    compartments = 0
    for compartment in reference["compartments"].findall(
        "version:compartment", reference["space"]
    ):
        compartments = compartments + 1
    # Count reactions.
    reactions = 0
    for reaction in reference["reactions"].findall(
        "version:reaction", reference["space"]
    ):
        reactions = reactions + 1
    # Count metabolites.
    metabolites = 0
    for metabolite in reference["metabolites"].findall(
    "version:species", reference["space"]
    ):
        metabolites = metabolites + 1
    # Compile and return inforation.
    return {
        "compartments": compartments,
        "reactions": reactions,
        "metabolites": metabolites
    }


def change_model_boundary(content=None):
    """
    Changes annotations for a model's boundary

    This function changes annotations of a model's boundary in compartments,
    metabolites, and reactions.

    arguments:
        content (object): content from file in Systems Biology Markup Language
            (XML)

    raises:

    returns:
        (object): content with changes

    """

    # Copy and interpret content.
    reference = metabocurator_collection.copy_interpret_content_recon2m2(
        content=content
    )
    # Correct designation of model's boundary in metabolites.
    for metabolite in reference["metabolites"].findall(
        "version:species", reference["space"]
    ):
        # Determine whether metabolite's compartment is model's boundary.
        if "boundary" in metabolite.attrib["id"]:
            novel_identifier = re.sub(
                r"_[eciglmnrx]_boundary", "_b", metabolite.attrib["id"]
            )
            metabolite.attrib["id"] = novel_identifier
            novel_compartment = "b"
            metabolite.attrib["compartment"] = novel_compartment
    # Correct designation of model's boundary in reactions.
    for reaction in reference["reactions"].findall(
        "version:reaction", reference["space"]
    ):
        # Search reaction's metabolites.
        for metabolite in reaction.iter(
            "{http://www.sbml.org/sbml/level2/version4}speciesReference"
        ):
            # Determine whether metabolite's compartment is model's boundary.
            if "boundary" in metabolite.attrib["species"]:
                novel_identifier = re.sub(
                    r"_[eciglmnrx]_boundary", "_b",
                    metabolite.attrib["species"]
                )
                metabolite.attrib["species"] = novel_identifier
    # Return content with changes.
    return reference["content"]


def change_model_compartments(curation_compartments=None, content=None):
    """
    Changes annotations for a model's compartments

    This function changes annotations of a model's compartments.

    arguments:
        curation_compartments (list<dict<str>>): changes to information about
            compartments
        content (object): content from file in Systems Biology Markup Language
            (XML)

    raises:

    returns:
        (object): content with changes

    """

    # Copy and interpret content.
    reference = metabocurator_collection.copy_interpret_content_recon2m2(
        content=content
    )
    # Change content for each combination of original and novel information.
    for row in curation_compartments:
        # Detmerine whether to change compartment's name.
        if row["description_original"] != row["description_novel"]:
            # Change information in compartments.
            for compartment in reference["compartments"].findall(
                "version:compartment", reference["space"]
            ):
                if compartment.attrib["id"] == row["identifier_original"]:
                    compartment.attrib["name"] = row["description_novel"]
        # Determine whether to change compartment's identifier.
        if row["identifier_original"] != row["identifier_novel"]:
            # Construct targets to recognize original and novel identifiers.
            # Use underscore prefix to match complete identifiers.
            original_elements = ["_", row["identifier_original"]]
            original_target = "".join(original_elements)
            novel_elements = ["_", row["identifier_novel"]]
            novel_target = "".join(novel_elements)
            # Change information in metabolites.
            # Change identifiers of metabolites.
            for metabolite in reference["metabolites"].findall(
                "version:species", reference["space"]
            ):
                # Determine whether to change metabolite's identifier.
                if original_target in metabolite.attrib["id"]:
                    metabolite.attrib["id"] = metabolite.attrib["id"].replace(
                        original_target, novel_target
                    )
            # Change information in reactions' metabolites.
            # Change identifiers of reactions' metabolites.
            for reaction in reference["reactions"].findall(
                "version:reaction", reference["space"]
            ):
                # Search reaction's metabolites.
                for metabolite in reaction.iter(
                    "{http://www.sbml.org/sbml/level2/version4}"
                    "speciesReference"
                ):
                    # Determine whether to change metabolite's identifier.
                    if original_target in metabolite.attrib["species"]:
                        metabolite.attrib["species"] = (
                            metabolite.attrib["species"].replace(
                                original_target, novel_target
                            )
                        )
    # Return content with changes.
    return reference["content"]


def remove_model_metabolite_prefix(content=None):
    """
    Removes unnecessary prefixes from identifiers for model's entities

    This function removes unnecessary prefixes from identifiers for
    metabolites.

    arguments:
        content (object): content from file in Systems Biology Markup Language
            (XML)

    raises:

    returns:
        (object): content with changes

    """

    # Copy and interpret content.
    reference = metabocurator_collection.copy_interpret_content_recon2m2(
        content=content
    )
    # Remove prefixes from identifiers for metabolites.
    for metabolite in reference["metabolites"].findall(
    "version:species", reference["space"]
    ):
        # Remove prefix from metabolite's identifier.
        novel_identifier = re.sub(r"^M_", "", metabolite.attrib["id"])
        metabolite.attrib["id"] = novel_identifier
        # Search metabolite's annotation.
        for description in metabolite.iter(
        "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}description"
        ):
            # Remove prefix from metabolite's identifier.
            novel_identifier = re.sub(
                r"^#M_",
                "#",
                description.attrib[
                "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
                ]
            )
            description.attrib[
            "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"
            ] = novel_identifier
    # Remove prefixes from identifiers for reactions' metabolites.
    for reaction in reference["reactions"].findall(
    "version:reaction", reference["space"]
    ):
        # Search reaction's metabolites.
        for metabolite in reaction.iter(
        "{http://www.sbml.org/sbml/level2/version4}speciesReference"
        ):
            # Remove prefix from metabolite's identifier.
            novel_identifier = re.sub(r"^M_", "", metabolite.attrib["species"])
            metabolite.attrib["species"] = novel_identifier
    # Return content with changes.
    return reference["content"]


def change_model_metabolites(curation_metabolites=None, content=None):
    """
    Changes metabolites' identifiers

    This function changes metabolites' identifiers according to information
    about translation.

    arguments:
        curation_metabolites (list<dict<str>>): changes to information about
            metabolites
        content (object): content from file in Systems Biology Markup Language
            (XML)

    raises:

    returns:
        (object): content with changes

    """

    # Copy and interpret content.
    reference = metabocurator_collection.copy_interpret_content_recon2m2(
        content=content
    )
    # Change content for each combination of original and novel identifiers.
    for row in curation_metabolites:
        # Construct targets to recognize original and novel identifiers.
        # Use trailing underscore to match complete identifiers.
        original_elements = [row["identifier_original"], "_"]
        original_target = "".join(original_elements)
        novel_elements = [row["identifier_novel"], "_"]
        novel_target = "".join(novel_elements)
        # Change identifiers of metabolites.
        for metabolite in reference["metabolites"].findall(
            "version:species", reference["space"]
        ):
            # Determine whether to change metabolite's identifier.
            if original_target in metabolite.attrib["id"]:
                metabolite.attrib["id"] = metabolite.attrib["id"].replace(
                    original_target, novel_target
                )
        # Change identifiers of reactions' metabolites.
        for reaction in reference["reactions"].findall(
            "version:reaction", reference["space"]
        ):
            # Search reaction's metabolites.
            for metabolite in reaction.iter(
                "{http://www.sbml.org/sbml/level2/version4}speciesReference"
            ):
                # Determine whether to change metabolite's identifier.
                if original_target in metabolite.attrib["species"]:
                    metabolite.attrib["species"] = (
                        metabolite.attrib["species"].replace(
                            original_target, novel_target
                        )
                    )
    # Return content with changes.
    return reference["content"]


def write_product(directory=None, information=None):
    """
    Writes product information to file

    arguments:
        directory (str): directory for product files
        information (object): information to write to file

    raises:

    returns:

    """

    # Specify directories and files.
    path = os.path.join(directory, "reconciliation")
    utility.confirm_path_directory(path)
    path_file = os.path.join(
        path, "recon2m2_reconciliation.xml"
    )
    # Write information to file.
    information.write(path_file, xml_declaration=False)


###############################################################################
# Procedure


def execute_procedure(directory=None):
    """
    Function to execute module's main behavior.

    The purpose of this procedure is to reconcile the metabolic model to be
    compatible with MetaNetX.

    arguments:
        directory (str): path to directory for source and product files

    raises:

    returns:

    """

    # Read source information from file.
    source = read_source(directory=directory)
    # Change model's content.
    # Correct content.
    content_boundary = change_model_boundary(content=source["content"])
    content_compartments = change_model_compartments(
        curation_compartments=source["curation_compartments"],
        content=content_boundary
    )
    content_prefix = remove_model_metabolite_prefix(
        content=content_compartments
    )
    content_metabolites = change_model_metabolites(
        curation_metabolites=source["curation_metabolites"],
        content=content_prefix
    )
    #Write product information to file.
    write_product(directory=directory, information=content_metabolites)
    # Summary.
    summary = count_model_sets_entities(content=content_metabolites)
    # Report.
    print("compartments: " + str(summary["compartments"]))
    print("reactions: " + str(summary["reactions"]))
    print("metabolites: " + str(summary["metabolites"]))
