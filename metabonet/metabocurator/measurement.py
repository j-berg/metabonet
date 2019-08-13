"""
Extract information about metabolic sets and entities from MetaNetX.

Title:
    provision

Imports:
    os: This module from The Python Standard Library contains definitions of
        tools to interact with the operating system.
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

# The purpose of this procedure is to enhance information about metabolic sets
# and entities.

###############################################################################
# Installation and importation of packages and modules


# Packages and modules from the python standard library

import os
#import sys
import shutil
#import importlib
import csv
import copy
import pickle
import math
import textwrap
import statistics

# Packages and modules from third parties

#import numpy
#import pandas

import scipy.stats

# Packages and modules from local source

import metabonet.utility as utility

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
    path_measurement = os.path.join(path_source, "measurement")
    # Read information from file.
    # Compile information.
    reference = read_source_reference(directory=directory)

    study_one = read_source_study(
        path=path_measurement,
        directory="metabolomics-workbench_pr000305_st000390"
    )
    study_two = read_source_study(
        path=path_measurement,
        directory="metabolomics-workbench_pr000058_st000061"
    )
    study_three_four = read_source_study(
        path=path_measurement,
        directory="metabolomics-workbench_pr000322_st000412"
    )
    study_five = read_source_study(
        path=path_measurement,
        directory="metabolomics-workbench_pr000599_st000842"
    )
    # Compile and return information.
    return {
        "reference": reference,
        "study_one": study_one,
        "study_two": study_two,
        "study_three_four": study_three_four,
        "study_five": study_five
    }


def read_source_reference(directory=None):
    """
    Reads and organizes source information from file.

    arguments:
        directory (str): directory of source files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_extraction = os.path.join(directory, "extraction")
    path_hmdb = os.path.join(path_extraction, "hmdb_summary.pickle")
    path_model = os.path.join(directory, "model")
    path_metabolites = os.path.join(path_model, "metabolites.pickle")
    # Read information from file.
    with open(path_hmdb, "rb") as file_source:
        hmdb = pickle.load(file_source)
    with open(path_metabolites, "rb") as file_source:
        metabolites = pickle.load(file_source)
    # Compile and return information.
    return {
        "hmdb": hmdb,
        "metabolites": metabolites
    }


def read_source_study_zero(directory=None):
    """
    Reads and organizes source information from file.

    arguments:
        directory (str): directory of source files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_measurement = os.path.join(directory, "metabolomic_measurements")
    path_study_zero = os.path.join(
        path_measurement, "karl_physiological-reports_2017"
    )
    path_measurements = os.path.join(
        path_study_zero, "measurements.tsv"
    )
    # Read information from file.
    measurements = utility.read_file_table(
        path_file=path_measurements,
        names=["set", "subset", "name", "hmdb", "fold", "p_value", "q_value"],
        delimiter="\t"
    )
    # Compile and return information.
    return {
        "measurements": measurements
    }


def read_source_study(path=None, directory=None):
    """
    Reads and organizes source information from file.

    arguments:
        path (str): path to directory
        directory (str): directory of source files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_study = os.path.join(path, directory)
    path_samples = os.path.join(path_study, "samples.tsv")
    path_analytes = os.path.join(path_study, "analytes.tsv")
    path_measurements = os.path.join(path_study, "measurements.tsv")
    path_signals = os.path.join(path_study, "signals.tsv")
    #path_translations = os.path.join(path_study, "translations.tsv")
    # Read information from file.
    samples = utility.read_file_table(
        path_file=path_samples,
        names=None,
        delimiter="\t"
    )
    analytes = utility.read_file_table(
        path_file=path_analytes,
        names=None,
        delimiter="\t"
    )
    measurements = utility.read_file_table(
        path_file=path_measurements,
        names=None,
        delimiter="\t"
    )
    signals = utility.read_file_table(
        path_file=path_signals,
        names=None,
        delimiter="\t"
    )
    if False:
        translations = utility.read_file_table(
            path_file=path_translations,
            names=None,
            delimiter="\t"
        )
    # Compile and return information.
    return {
        "samples": samples,
        "analytes": analytes,
        "measurements": measurements,
        "signals": signals,
        #"translations": translations
    }


# Study zero.


def curate_measurements_study_zero(measurements=None):
    """
    Extracts information about measurements.

    arguments:
        measurements (list<dict>): information from source about measurements

    raises:

    returns:
        (list<dict>): information about measurements

    """

    # Extract relevant information about measurements.
    measurements = extract_measurements_study_one(
        records=source["measurements"]
    )
    # Match measurements to identifiers for Human Metabolome Database (HMDB).
    measurements_hmdb = enhance_measurements_hmdb_references(
        measurements_original=copy.deepcopy(measurements),
        summary_hmdb=source["summary_hmdb"]
    )
    # Match measurements to metabolites.
    measurements_metabolites = match_measurements_to_metabolites(
        reference="hmdb",
        measurements_original=copy.deepcopy(measurements_hmdb),
        metabolites=source["metabolites"]
    )
    # Filter measurements for those that map to metabolites.
    measurements_match = filter_measurements_metabolites(
        measurements_original=copy.deepcopy(measurements_metabolites)
    )
    # Calculate base-2 logarithm of fold change.
    measurements_log = calculate_measurements_log(
        measurements_original=measurements_match
    )
    # Filter analytes for those whose differences have p-values < 0.05.
    measurements_significance = filter_measurements_significance(
        p_value_threshold=0.05,
        measurements_original=measurements_log
    )
    # Convert measurement information to table in text format.
    measurements_text = convert_measurements_text(
        measurements=measurements_significance
    )
    # Compile and return information.
    return {
        "measurements": measurements_significance,
        "measurements_text": measurements_text
    }


def extract_measurements_study_zero(records=None):
    """
    Extracts information about measurements.

    arguments:
        records (list<dict>): information from source about measurements

    raises:

    returns:
        (list<dict>): information about measurements

    """

    measurements = []
    for record in records[2:739]:
        name_original = record["name"]
        name_novel = name_original.replace("*", "")
        measurement = {
            "name": name_novel,
            "hmdb": record["hmdb"],
            "fold": float(record["fold"]),
            "p_value": float(record["p_value"])
        }
        measurements.append(measurement)
    return measurements


# Curation.


def curate_study(
    pair=None,
    normalization=None,
    group_numerator=None,
    group_denominator=None,
    samples=None,
    analytes=None,
    measurements=None,
    signals=None,
    hmdb=None,
    metabolites=None
):
    """
    Curates information about metabolomic measurements from a study.

    arguments:
        pair (bool): whether samples have dependent pairs
        normalization (bool): whether to normalize measurements
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample
        hmdb (dict<dict>): information about metabolites from Human Metabolome
            Database (HMDB)
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (dict): information about measurements for analytes

    """

    # Curate analytes.
    summary_analytes = curate_study_analytes(
        pair=pair,
        group_numerator=group_numerator,
        group_denominator=group_denominator,
        samples=samples,
        analytes=analytes,
        measurements=measurements,
        signals=signals,
        hmdb=hmdb,
        metabolites=metabolites
    )
    # Curate and analyze measurements.
    summary_measurements = curate_study_measurements(
        summary=summary_analytes,
        pair=pair,
        normalization=normalization,
        group_numerator=group_numerator,
        group_denominator=group_denominator,
        samples=samples,
        analytes=analytes,
        measurements=measurements,
        signals=signals,
        hmdb=hmdb,
        metabolites=metabolites
    )
    # Filter for anlaytes that match metabolites.
    summary_match = filter_analytes_metabolites(
        summary=copy.deepcopy(summary_measurements)
    )
    # Prepare report of matches of analytes to metabolites.
    report_match = prepare_report_analyte_metabolite_match(
        summary=summary_measurements,
        metabolites=metabolites
    )
    # Convert measurement information to table in text format.
    summary_text = convert_summary_text(summary=summary_match)
    # Convert information for analysis in MetaboAnalyst.
    summary_metaboanalyst = prepare_report_metaboanalyst(
        pair=pair,
        normalization=normalization,
        summary=copy.deepcopy(summary_measurements),
        group_one=group_numerator,
        group_two=group_denominator,
        samples=samples,
        measurements=measurements,
        signals=signals
    )
    # Report.
    print("analytes, measurements after curation...")
    report = prepare_curation_report(summary=summary_measurements)
    print(report)
    # Compile and return information.
    return {
        "pair": pair,
        "summary": summary_match,
        "summary_text": summary_text,
        "summary_metaboanalyst": summary_metaboanalyst["unpair"],
        "summary_metaboanalyst_pair": summary_metaboanalyst["pair"],
        "report_match": report_match
    }


def curate_study_analytes(
    pair=None,
    group_numerator=None,
    group_denominator=None,
    samples=None,
    analytes=None,
    measurements=None,
    signals=None,
    hmdb=None,
    metabolites=None
):
    """
    Curates information about metabolomic measurements from a study.

    arguments:
        pair (bool): whether samples have dependent pairs
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample
        hmdb (dict<dict>): information about metabolites from Human Metabolome
            Database (HMDB)
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Derive summary from analytes.
    summary = extract_analytes_summary(
        analytes=analytes
    )
    # Filter analytes by coverage of measurements for samples.
    summary_coverage = filter_analytes_coverage(
        pair=pair,
        summary=summary,
        group_one=group_numerator,
        group_two=group_denominator,
        samples=samples,
        measurements=measurements
    )
    # Enhance analyte references.
    # Only enhance references to PubChem if none already exist.
    summary_reference = enhance_analytes_references(
        summary=summary_coverage,
        hmdb=hmdb
    )
    # Filter analytes by references to PubChem.
    summary_reference_coverage = filter_analytes_reference(
        summary=summary_reference
    )
    # Match analytes to metabolites.
    # Match by PubChem identifiers.
    summary_metabolite = match_analytes_to_metabolites(
        reference="pubchem",
        summary=copy.deepcopy(summary_reference_coverage),
        metabolites=metabolites
    )
    # Enhance analyte names.
    summary_name = enhance_analytes_names(
        summary=summary_metabolite,
        metabolites=metabolites
    )
    # Return information.
    return summary_name


def curate_study_measurements(
    summary=None,
    pair=None,
    normalization=None,
    group_numerator=None,
    group_denominator=None,
    samples=None,
    analytes=None,
    measurements=None,
    signals=None,
    hmdb=None,
    metabolites=None
):
    """
    Curates information about metabolomic measurements from a study.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        pair (bool): whether samples have dependent pairs
        normalization (bool): whether to normalize measurements
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample
        hmdb (dict<dict>): information about metabolites from Human Metabolome
            Database (HMDB)
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Normalize analyte's measurements by total signal for each sample.
    if normalization:
        measurements_normalization = normalize_measurements_samples_signals(
            summary=summary,
            group_one=group_numerator,
            group_two=group_denominator,
            samples=samples,
            measurements=measurements,
            signals=signals
        )
    else:
        measurements_normalization = measurements
    # Determine priority analytes.
    summary_priority = determine_priority_redundant_analytes(
        group_control=group_denominator,
        samples=samples,
        summary=summary,
        measurements=measurements_normalization
    )
    # Determine fold changes.
    if pair:
        summary_fold_log = calculate_analytes_folds_logarithms_pairs(
            summary=summary_priority,
            group_numerator=group_numerator,
            group_denominator=group_denominator,
            samples=samples,
            measurements=measurements_normalization
        )
    else:
        summary_fold = calculate_analytes_folds(
            summary=summary_priority,
            group_numerator=group_numerator,
            group_denominator=group_denominator,
            samples=samples,
            measurements=measurements_normalization
        )
        # Determine logarithms-base-2 of fold changes.
        summary_fold_log = calculate_folds_logarithms(
            records=summary_fold
        )
    # Determine p-values.
    # Compare pairs of samples in both groups.
    # Apply pair t-test for dependent sample populations.
    if pair:
        summary_probability = calculate_analytes_p_values_pairs(
            summary=summary_fold_log,
            group_one=group_numerator,
            group_two=group_denominator,
            samples=samples,
            measurements=measurements_normalization
        )
    else:
        summary_probability = calculate_analytes_p_values(
            summary=summary_fold_log,
            group_one=group_numerator,
            group_two=group_denominator,
            samples=samples,
            measurements=measurements_normalization
        )
    # Determine base-10 logarithms of p-values.
    summary_probability_log = calculate_p_values_logarithms(
        records=summary_probability
    )
    # Determine significance (arbitrary p-value threshold).
    summary_significance = determine_measurements_significance(
        records=summary_probability_log,
        threshold_p=0.05
    )
    # Return information.
    return summary_significance


# Curation of analytes.


def extract_analytes_summary(analytes=None):
    """
    Extracts information about analytes.

    arguments:
        analytes (list<dict<str>>): information about analytes from a study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    summary = []
    for analyte in analytes:
        identifier = analyte["identifier"]
        name = analyte["name"]
        metabolomics_workbench = analyte["reference_metabolomics_workbench"]
        if analyte["reference_pubchem"] == "-":
            pubchem = ""
        else:
            pubchem = analyte["reference_pubchem"]
        references = {
            "metabolomics_workbench": metabolomics_workbench,
            "pubchem": pubchem
        }
        record = {
            "identifier": identifier,
            "name": name,
            "references": references
        }
        summary.append(record)
    return summary


def filter_analytes_coverage(
    pair=None,
    summary=None,
    group_one=None,
    group_two=None,
    samples=None,
    measurements=None
):
    """
    Filters analytes by coverage of measurements for samples.

    arguments:
        pair (bool): whether samples have dependent pairs
        summary (list<dict<str>>): information about measurements for analytes
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    if pair:
        # Filter analytes with adequate coverage of pairs of samples.
        # Determine pairs of samples.
        pairs_samples = determine_pairs_samples(
            group_one=group_one,
            group_two=group_two,
            samples=samples
        )
        summary_novel = []
        for record in summary:
            analyte = record["identifier"]
            # Determine whether valid measurements exist for multiple pairs of
            # samples in each group.
            coverage = determine_analyte_coverage_pairs(
                analyte=analyte,
                group_one=group_one,
                group_two=group_two,
                pairs_samples=pairs_samples,
                measurements=measurements
            )
            if coverage:
                summary_novel.append(record)
        return summary_novel
    else:
        # Filter analytes with adequate coverage of samples.
        # Determine all relevant samples.
        groups_samples = determine_groups_samples(
            group_one=group_one,
            group_two=group_two,
            samples=samples
        )
        summary_novel = []
        for record in summary:
            analyte = record["identifier"]
            # Determine whether valid measurements exist for multiple samples
            # in each group.
            coverage = determine_analyte_coverage(
                analyte=analyte,
                group_one=group_one,
                group_two=group_two,
                groups_samples=groups_samples,
                measurements=measurements
            )
            if coverage:
                summary_novel.append(record)
        return summary_novel


def determine_analyte_coverage(
    analyte=None,
    group_one=None,
    group_two=None,
    groups_samples=None,
    measurements=None
):
    """
    Determines whether an analyte has coverage of measurements for samples.

    arguments:
        analyte (str): identifier of an analyte
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        groups_samples (dict<list<str>>): samples from both groups
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (bool): whether the analyte has coverage of measurements for samples

    """

    # Find measurements for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=analyte,
        measurements=measurements
    )
    # Collect valid measurements for samples in each group.
    coverages_one = []
    for sample in groups_samples[group_one]:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            coverages_one.append(True)
        else:
            coverages_one.append(False)
    coverages_two = []
    for sample in groups_samples[group_two]:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            coverages_two.append(True)
        else:
            coverages_two.append(False)
    # Filter for samples with coverage.
    coverages_one_true = list(filter(lambda value: value, coverages_one))
    coverages_two_true = list(filter(lambda value: value, coverages_two))
    return ((len(coverages_one_true) > 1) and (len(coverages_two_true) > 1))


def determine_analyte_coverage_pairs(
    analyte=None,
    group_one=None,
    group_two=None,
    pairs_samples=None,
    measurements=None
):
    """
    Determines whether an analyte has coverage of measurements for samples.

    arguments:
        analyte (str): identifier of an analyte
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        pairs_samples (dict): pairs of samples from both groups
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (bool): whether the analyte has coverage of measurements for samples

    """

    # Find measurements for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=analyte,
        measurements=measurements
    )
    # Collect values of measurements for analyte in samples.
    coverages = []
    for pair in pairs_samples.values():
        sample_one = pair[group_one]
        sample_two = pair[group_two]
        if (determine_measurements_validity(
            samples=[sample_one, sample_two],
            measurements=measurements_analyte
        )):
            coverages.append(True)
        else:
            coverages.append(False)
    # Filter for samples with coverage.
    coverages_true = list(filter(lambda value: value, coverages))
    return len(coverages_true) > 1


def enhance_analytes_references(
    summary=None, hmdb=None
):
    """
    Enhances analytes' references to PubChem.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        hmdb (dict<dict>): information about metabolites from Human Metabolome
            Database (HMDB)

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Enhance references to PubChem.
    summary_novel = []
    for record in summary:
        # Enhance references to PubChem.
        # Give priority to PubChem identifier from Metabolomics Workbench by
        # placing it first in the list.
        if len(str(record["references"]["pubchem"])) > 0:
            references_pubchem = [record["references"]["pubchem"]]
        else:
            references_pubchem = []
        if not (len(references_pubchem) > 0):
            # Analyte does not have any references to PubChem.
            # Find references to HMDB from analyte's names.
            name_one = record["identifier"]
            name_two = record["name"]
            identifiers_hmdb = utility.match_hmdb_entries_by_identifiers_names(
                identifiers=[],
                names=[name_one, name_two],
                summary_hmdb=hmdb
            )
            # Extract references to PubChem from HMDB.
            if len(identifiers_hmdb) > 0:
                # Extract references from entries in HMDB
                for key in identifiers_hmdb:
                    hmdb_entry = hmdb[key]
                    hmdb_pubchem = hmdb_entry["reference_pubchem"]
                    if (hmdb_pubchem is not None) and (len(hmdb_pubchem) > 0):
                        references_pubchem.append(hmdb_pubchem)
                references_pubchem = utility.collect_unique_elements(
                    references_pubchem
                )
        # Include references.
        record["references"]["pubchem"] = references_pubchem
        summary_novel.append(record)
    return summary_novel


def match_analytes_to_metabolites(
    reference=None,
    summary=None,
    metabolites=None
):
    """
    Matches measurements to metabolites.

    arguments:
        reference (str): name of attribute to use for match
        summary (list<dict<str>>): information about measurements for analytes
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    summary_novel = []
    for record in summary:
        references_record = record["references"][reference]
        # Find metabolites that match the record's reference.
        metabolites_matches = []
        for metabolite in metabolites.values():
            references_metabolite = metabolite["references"][reference]
            # Determine whether any references match.
            matches = utility.filter_common_elements(
                list_one=references_record,
                list_two=references_metabolite
            )
            if len(matches) > 0:
                metabolites_matches.append(metabolite["identifier"])
        record["references"]["metabolite"] = metabolites_matches
        summary_novel.append(record)
    return summary_novel


def filter_analytes_reference(
    summary=None
):
    """
    Filters analytes by coverage of references.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    summary_novel = []
    for record in summary:
        references = record["references"]
        pubchem = references["pubchem"]
        if len(pubchem) > 0:
            summary_novel.append(record)
    return summary_novel


def enhance_analytes_names(
    summary=None, metabolites=None
):
    """
    Enhances analytes' names.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    summary_novel = []
    for record in summary:
        name_original = record["name"]
        record["name_original"] = name_original
        # Determine whether record has a reference to a metabolite.
        if len(record["references"]["metabolite"]) > 0:
            identifier_metabolite = record["references"]["metabolite"][0]
            metabolite = metabolites[identifier_metabolite]
            name = metabolite["name"]
            record["name"] = name
        summary_novel.append(record)
    return summary_novel


def determine_priority_redundant_analytes(
    group_control=None,
    samples=None,
    summary=None,
    measurements=None
):
    """
    Determines whether any analytes are redundant and determines priority
    analytes.



    arguments:
        group_control (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        summary (list<dict<str>>): information about measurements for analytes
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Collect unique entities.
    # Each entity can have representation by multiple analytes.
    entities = collect_entities_analytes(summary=summary)
    # Prioritize a single analyte for each entity.
    analytes_priority = determine_entities_priority_analytes(
        entities=entities,
        group_control=group_control,
        samples=samples,
        measurements=measurements
    )
    # Filter analytes to include only a single priority analyte for each
    # entity.
    summary_unique = filter_analytes_priority(
        analytes=analytes_priority,
        summary=summary
    )
    return summary_unique


def collect_entities_analytes(summary=None):
    """
    Collects unique entities and their analytes.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    raises:

    returns:
        (dict): information about entities and their analytes

    """

    entities = {}
    for record in summary:
        # Prioritize the first identifier for PubChem.
        identifier = record["references"]["pubchem"][0]
        name = record["name"]
        analyte_identifier = record["identifier"]
        if identifier not in entities.keys():
            entry = {
                "identifier": identifier,
                "name": name,
                "analytes": [analyte_identifier]
            }
            entities[identifier] = entry
        else:
            entities[identifier]["analytes"].append(analyte_identifier)
    return entities


def filter_redundant_entities(entities=None):
    """
    Filters entities with redundant analytes.

    arguments:
        entities (dict): information about entities and their analytes

    raises:

    returns:
        (dict): information about entities and their analytes

    """

    entities_redundancy = {}
    for entity in entities.values():
        identifier = entity["identifier"]
        analytes = entity["analytes"]
        if len(analytes) > 1:
            entities_redundancy[identifier] = entity
    return entities_redundancy


def determine_entities_priority_analytes(
    entities=None,
    group_control=None,
    samples=None,
    measurements=None
):
    """
    Determines a single priority analyte for each entity.

    arguments:
        entities (dict): information about entities and their analytes
        group_control (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<str>): identifiers of analytes

    """

    # Determine samples in each group.
    groups_samples = determine_groups_samples(
        group_one=group_control,
        group_two="null",
        samples=samples
    )
    group_samples = groups_samples[group_control]
    analytes_priority = []
    for entity in entities.values():
        analytes = entity["analytes"]
        if len(analytes) == 1:
            analytes_priority.append(analytes[0])
        else:
            analyte_priority = determine_entity_priority_analyte(
                analytes=analytes,
                group_samples=group_samples,
                measurements=measurements
            )
            analytes_priority.append(analyte_priority)
    return analytes_priority


def determine_entity_priority_analyte(
    analytes=None,
    group_samples=None,
    measurements=None
):
    """
    Determines the single priority analyte for an entity.

    If multiple analytes represent a single chemical entity redundantly, then
    prioritize the analyte whose measurements have the least dispersion.

    arguments:
        analytes (list<str>): identifiers of analytes
        group_samples (list<str>): identifiers of samples in a group
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (str): identifier of an analyte

    """

    # Collect measurements for each of entity's redundant analytes.
    analytes_dispersions = calculate_analytes_measurements_dispersions(
        analytes=analytes,
        group_samples=group_samples,
        measurements=measurements
    )
    # Prioritize analytes by minimal variance of measurements.
    analytes_rank = sorted(
        analytes_dispersions,
        key=lambda record: record["dispersion"],
        reverse=False
    )
    # Select priority analyte.
    return analytes_rank[0]["analyte"]


def calculate_analytes_measurements_dispersions(
    analytes=None,
    group_samples=None,
    measurements=None
):
    """
    Calculates the dispersions of measurement values for each analyte.

    The index of dispersion, coefficient of dispersion, or relative variance is
    the quotient of division of the variance by the mean.

    arguments:
        analytes (list<str>): identifiers of analytes
        group_samples (list<str>): identifiers of samples in a group
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict>): information about analytes

    """

    analytes_dispersions = []
    for analyte in analytes:
        # Find measurements for analyte.
        measurements_analyte = find_analyte_measurements(
            identifier=analyte,
            measurements=measurements
        )
        # Collect values of measurements for analyte in control group samples.
        values = []
        for sample in group_samples:
            if (determine_measurements_validity(
                samples=[sample],
                measurements=measurements_analyte
            )):
                value = float(measurements_analyte[sample])
                values.append(value)
        # Calculate variance of values.
        variance = statistics.variance(values)
        mean = statistics.mean(values)
        dispersion = variance / mean
        # Compile information.
        record = {
            "analyte": analyte,
            "values": values,
            "dispersion": dispersion
        }
        analytes_dispersions.append(record)
    return analytes_dispersions


def filter_analytes_priority(
    analytes=None,
    summary=None
):
    """
    Determines a single priority analyte for each entity.

    arguments:
        analytes (list<str>): identifiers of analytes
        summary (list<dict<str>>): information about measurements for analytes

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    summary_novel = []
    for record in summary:
        analyte = record["identifier"]
        if analyte in analytes:
            summary_novel.append(record)
    return summary_novel


# Curation of measurements.


# Normalization of measurements.


def normalize_measurements_samples_signals(
    summary=None,
    group_one=None,
    group_two=None,
    samples=None,
    measurements=None,
    signals=None
):
    """
    Normalizes measurements by total signal for each sample.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample

    raises:

    returns:
        (list<dict<str>>): information about measurements from a study

    """

    # Determine all relevant samples.
    groups_samples = determine_groups_samples(
        group_one=group_one,
        group_two=group_two,
        samples=samples
    )
    samples_relevant = groups_samples[group_one]
    samples_relevant.extend(groups_samples[group_two])
    # Calculate normalization factors for each sample.
    samples_factors = calculate_normalization_factors(
        report=False,
        samples=samples_relevant,
        signals=signals
    )
    # Normalize measurements.
    # Multiply each measurement by the normalization factor for its sample.
    measurements_normalization = normalize_measurements(
        samples_factors=samples_factors,
        measurements=measurements
    )
    # Return information.
    return measurements_normalization


def calculate_normalization_factors(
    report=None,
    samples=None,
    signals=None
):
    """
    Calculates normalization factors for each sample.

    arguments:
        report (bool): whether to print a report
        samples (list<str>): identifiers of samples
        signals (list<dict<str>>): information about total signals for each
            sample

    raises:

    returns:
        (dict<float>): normalization factors for each sample

    """

    # Calculate total signals for all relevant samples.
    samples_totals = {}
    for sample in samples:
        # Collect all valid signals for the sample.
        signals_sample = []
        for signal in signals:
            # Determine whether signal is valid.
            if (determine_measurements_validity(
                samples=[sample],
                measurements=signal
            )):
                signal_sample = float(signal[sample])
                signals_sample.append(signal_sample)
        if len(signals_sample) > 0:
            # Valid signals exist for the sample.
            # Calculate total signal for sample.
            total = math.fsum(signals_sample)
            samples_totals[sample] = total
    # Determine maximal total signal for all samples.
    maximum = max(samples_totals.values())
    # Calculate normalization factors for all relevant samples.
    samples_factors = {}
    samples_report = []
    for sample in samples_totals.keys():
        # Calculate normalization factor.
        total = samples_totals[sample]
        divisor = (total / maximum)
        factor = 1 / divisor
        samples_factors[sample] = factor
        # Prepare report.
        record = {
            "sample": sample,
            "total": total,
            "maximum": maximum,
            "divisor": divisor,
            "factor": factor
        }
        samples_report.append(record)
    if report:
        print("sample normalization report")
        print(samples_report)
    # Return information.
    return samples_factors


def normalize_measurements(
    samples_factors=None,
    measurements=None
):
    """
    Normalizes measurements.

    arguments:
        samples_factors (dict<float>): normalization factors for each sample
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): normalization factors for each sample

    """

    # Iterate on measurements.
    measurements_normalization = []
    for measurement in measurements:
        # Iterate on samples.
        for sample in samples_factors.keys():
            # Determine whether a valid measurement exists for the sample.
            if (determine_measurements_validity(
                samples=[sample],
                measurements=measurement
            )):
                value_raw = float(measurement[sample])
                factor = samples_factors[sample]
                value_normalization = (value_raw * factor)
                measurement[sample] = value_normalization
        measurements_normalization.append(measurement)
    # Return information.
    return measurements_normalization


# Analysis of measurements.


def calculate_analytes_folds(
    summary=None,
    group_numerator=None,
    group_denominator=None,
    samples=None,
    measurements=None
):
    """
    Determines the mean fold changes for each analyte between experimental
    groups.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Determine samples in each group.
    groups_samples = determine_groups_samples(
        group_one=group_numerator,
        group_two=group_denominator,
        samples=samples
    )
    # Determine mean fold changes for each analyte.
    summary_novel = []
    for record in summary:
        identifier = record["identifier"]
        fold = calculate_analyte_fold(
            identifier=identifier,
            group_numerator=group_numerator,
            group_denominator=group_denominator,
            groups_samples=groups_samples,
            measurements=measurements
        )
        record["fold"] = fold
        summary_novel.append(record)
    return summary_novel


def determine_groups_samples(
    group_one=None,
    group_two=None,
    samples=None
):
    """
    Determines the samples for each group for the same patient.

    arguments:
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study

    raises:

    returns:
        (dict): samples from both groups

    """

    groups = [group_one, group_two]
    groups_samples = {
        group_one: [],
        group_two: []
    }
    for sample in samples:
        identifier = sample["identifier"]
        group = sample["group"]
        # Determine whether the sample belongs to a relevant group.
        if group in groups:
            groups_samples[group].append(identifier)
    return groups_samples


def calculate_analyte_fold(
    identifier=None,
    group_numerator=None,
    group_denominator=None,
    groups_samples=None,
    measurements=None
):
    """
    Determines the mean fold change between experimental groups for an analyte.

    arguments:
        identifier (str): identifier of an analyte
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        groups_samples (dict<list<str>>): samples from both groups
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (float): fold change

    """

    # Find measurements for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=identifier,
        measurements=measurements
    )
    # Determine fold changes for analyte's measurements.
    numerator_values = []
    for sample in groups_samples[group_numerator]:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            value = float(measurements_analyte[sample])
            numerator_values.append(value)
    denominator_values = []
    for sample in groups_samples[group_denominator]:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            value = float(measurements_analyte[sample])
            denominator_values.append(value)
    numerator_mean = statistics.mean(numerator_values)
    denominator_mean = statistics.mean(denominator_values)
    fold = numerator_mean / denominator_mean
    return fold


def calculate_analytes_folds_logarithms_pairs(
    summary=None,
    group_numerator=None,
    group_denominator=None,
    samples=None,
    measurements=None
):
    """
    Determines the mean fold changes for each analyte between experimental
    groups.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Determine pairs of samples.
    pairs_samples = determine_pairs_samples(
        group_one=group_numerator,
        group_two=group_denominator,
        samples=samples
    )
    # Determine mean fold changes for each analyte.
    summary_novel = []
    for record in summary:
        identifier = record["identifier"]
        fold, fold_log = calculate_analyte_fold_logarithm_pairs(
            identifier=identifier,
            group_numerator=group_numerator,
            group_denominator=group_denominator,
            pairs_samples=pairs_samples,
            measurements=measurements
        )
        record["fold"] = fold
        record["fold_log"] = fold_log
        summary_novel.append(record)
    return summary_novel


def determine_pairs_samples(
    group_one=None,
    group_two=None,
    samples=None
):
    """
    Determines the samples for each group for the same patient.

    arguments:
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study

    raises:

    returns:
        (dict): samples from each group for each pair

    """

    groups = [group_one, group_two]
    pairs_samples = {}
    for sample_cis in samples:
        identifier_cis = sample_cis["identifier"]
        pair_cis = str(sample_cis["pair"])
        group_cis = sample_cis["group"]
        # Determine whether the sample belongs to a relevant group.
        if group_cis in groups:
            # Determine whether the sample belongs to a novel pair.
            if pair_cis not in pairs_samples.keys():
                # Find sample in same pair and other group.
                for sample_trans in samples:
                    identifier_trans = sample_trans["identifier"]
                    pair_trans = str(sample_trans["pair"])
                    group_trans = sample_trans["group"]
                    pair = (pair_trans == pair_cis)
                    group = (
                        (group_trans in groups) and (group_trans != group_cis)
                    )
                    if (pair and group):
                        # Found the other sample for the same patient.
                        break
                pairs_samples[pair_cis] = {
                    "pair": pair_cis,
                    group_cis: identifier_cis,
                    group_trans: identifier_trans
                }
    return pairs_samples


def calculate_analyte_fold_logarithm_pairs(
    identifier=None,
    group_numerator=None,
    group_denominator=None,
    pairs_samples=None,
    measurements=None
):
    """
    Determines the mean fold change between experimental groups for an analyte.

    arguments:
        identifier (str): identifier of an analyte
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        pairs_samples (dict): pairs of samples from both groups
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (float, float): mean fold change, mean logarithm fold change

    """

    # Find measurements for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=identifier,
        measurements=measurements
    )
    # Determine fold changes for analyte's measurements.
    folds = []
    for pair in pairs_samples.values():
        sample_numerator = pair[group_numerator]
        sample_denominator = pair[group_denominator]
        if (determine_measurements_validity(
            samples=[sample_numerator, sample_denominator],
            measurements=measurements_analyte
        )):
            numerator = float(measurements_analyte[sample_numerator])
            denominator = float(measurements_analyte[sample_denominator])
            if (numerator > 0 and denominator > 0):
                fold = numerator / denominator
                folds.append(fold)
    # Calculate mean of folds.
    fold_mean = statistics.mean(folds)
    # Calculate mean of logarithms of folds.
    # As logarithms are not distributive, it is necessary to calculate
    # logarithms before calculation of the mean.
    # This calculation can make the logarithm fold seem inconsistent with the
    # mean fold.
    folds_log = []
    for fold in folds:
        fold_log = math.log(fold, 2)
        folds_log.append(fold_log)
    fold_log_mean = statistics.mean(folds_log)
    # Return information.
    return fold_mean, fold_log_mean


def find_analyte_measurements(identifier=None, measurements=None):
    """
    Finds information about measurements for an analyte.

    arguments:
        identifier (str): identifier of an analyte
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (dict<str>): measurements for an analyte

    """

    def match(record):
        analyte_comparison = utility.convert_string_low_alpha_num(
            record["analyte"]
        )
        identifier_comparison = utility.convert_string_low_alpha_num(
            identifier
        )
        return analyte_comparison == identifier_comparison
    measurements_analyte = utility.find(
        match=match,
        sequence=measurements
    )
    if measurements_analyte is None:
        print("error finding measurements for analyte: " + identifier)
    return measurements_analyte


def find_analyte_record(identifier=None, analytes=None):
    """
    Finds information about an analyte.

    arguments:
        identifier (str): identifier of an analyte
        analytes (list<dict<str>>): information about analytes

    raises:

    returns:
        (dict<str>): information about an analyte

    """

    def match(record):
        analyte_comparison = utility.convert_string_low_alpha_num(
            record["identifier"]
        )
        identifier_comparison = utility.convert_string_low_alpha_num(
            identifier
        )
        return analyte_comparison == identifier_comparison
    analyte = utility.find(
        match=match,
        sequence=analytes
    )
    if analyte is None:
        print("error finding analyte: " + identifier)
    return analyte


def calculate_folds_logarithms(records=None):
    """
    Calculates base-2 logarithms of fold changes in records.

    arguments:
        records (list<dict>): information about measurements of analytes

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    records_novel = []
    for record in records:
        fold = record["fold"]
        record["fold_log"] = math.log(fold, 2)
        records_novel.append(record)
    return records_novel


def calculate_analytes_p_values(
    summary=None,
    group_one=None,
    group_two=None,
    samples=None,
    measurements=None
):
    """
    Determines the mean fold changes for each analyte between experimental
    groups.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Determine samples in each group.
    groups_samples = determine_groups_samples(
        group_one=group_one,
        group_two=group_two,
        samples=samples
    )
    # Determine p-value for each analyte.
    summary_novel = []
    for record in summary:
        identifier = record["identifier"]
        p_value = calculate_analyte_p_value(
            identifier=identifier,
            group_one=group_one,
            group_two=group_two,
            groups_samples=groups_samples,
            measurements=measurements
        )
        record["p_value"] = p_value
        summary_novel.append(record)
    return summary_novel


def calculate_analyte_p_value(
    identifier=None,
    group_one=None,
    group_two=None,
    groups_samples=None,
    measurements=None
):
    """
    Determines the p-value between experimental groups for an analyte.

    arguments:
        identifier (str): identifier of an analyte
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        groups_samples (dict<list<str>>): samples from both groups
        measurements (list<dict<str>>): information measurements from a study

    raises:

    returns:
        (float): p-value

    """

    # Find measurements for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=identifier,
        measurements=measurements
    )
    # Collect measurements for samples from both groups.
    one_values = []
    for sample in groups_samples[group_one]:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            value = float(measurements_analyte[sample])
            one_values.append(value)
    two_values = []
    for sample in groups_samples[group_two]:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            value = float(measurements_analyte[sample])
            two_values.append(value)
    # Determine p-value.
    t_statistic, p_value = scipy.stats.ttest_ind(one_values, two_values)
    return p_value


def calculate_analytes_p_values_pairs(
    summary=None,
    group_one=None,
    group_two=None,
    samples=None,
    measurements=None
):
    """
    Determines the mean fold changes for each analyte between experimental
    groups.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Determine pairs of samples.
    pairs_samples = determine_pairs_samples(
        group_one=group_one,
        group_two=group_two,
        samples=samples
    )
    # Determine p-value for each analyte.
    summary_novel = []
    for record in summary:
        identifier = record["identifier"]
        p_value = calculate_analyte_p_value_pairs(
            identifier=identifier,
            group_one=group_one,
            group_two=group_two,
            pairs_samples=pairs_samples,
            measurements=measurements
        )
        record["p_value"] = p_value
        summary_novel.append(record)
    return summary_novel


def calculate_analyte_p_value_pairs(
    identifier=None,
    group_one=None,
    group_two=None,
    pairs_samples=None,
    measurements=None
):
    """
    Determines the p-value between experimental groups for an analyte.

    arguments:
        identifier (str): identifier of an analyte
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        pairs_samples (dict): pairs of samples from both groups
        measurements (list<dict<str>>): information measurements from a study

    raises:

    returns:
        (float): p-value

    """

    # Find measurements for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=identifier,
        measurements=measurements
    )
    # Collect measurements for pairs of samples from both groups.
    groups_measurements = {
        group_one: [],
        group_two: []
    }
    for pair in pairs_samples.values():
        sample_one = pair[group_one]
        sample_two = pair[group_two]
        if (determine_measurements_validity(
            samples=[sample_one, sample_two],
            measurements=measurements_analyte
        )):
            groups_measurements[group_one].append(
                float(measurements_analyte[sample_one])
            )
            groups_measurements[group_two].append(
                float(measurements_analyte[sample_two])
            )
    # Determine p-values.
    t_statistic, p_value = scipy.stats.ttest_rel(
        groups_measurements[group_one], groups_measurements[group_two]
    )
    return p_value


def calculate_p_values_logarithms(records=None):
    """
    Calculates base-10 logarithms of p-values in records.

    arguments:
        records (list<dict>): information about measurements of analytes

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    records_novel = []
    for record in records:
        p_value = record["p_value"]
        record["p_value_log"] = math.log(p_value, 10)
        records_novel.append(record)
    return records_novel


def determine_measurements_significance(
    records=None,
    threshold_p=None
):
    """
    Calculates base-10 logarithms of p-values in records.

    arguments:
        records (list<dict>): information about measurements of analytes
        threshold_p (float): threshold by p-value

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    records_novel = []
    for record in records:
        p_value = record["p_value"]
        if p_value < threshold_p:
            significance = True
        else:
            significance = False
        record["significance"] = significance
        records_novel.append(record)
    return records_novel


def filter_analytes_metabolites(
    summary=None
):
    """
    Filter analytes for those that map to metabolites.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    summary_novel = []
    for record in summary:
        metabolites = record["references"]["metabolite"]
        if len(metabolites) > 0:
            summary_novel.append(record)
    return summary_novel


def convert_summary_text(summary=None):
    """
    Converts information about measurements to text format.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    returns:
        (list<dict<str>>): information about measurements for analytes

    raises:

    """

    records_text = []
    for record in summary:
        significance = record["significance"]
        if significance:
            significance_text = "True"
        else:
            significance_text = "False"
        record_text = {
            "identifier": record["identifier"],
            "name_original": record["name_original"],
            "name": record["name"],
            "reference_pubchem": ";".join(record["references"]["pubchem"]),
            "reference_metabolite": (
                ";".join(record["references"]["metabolite"])
            ),
            "fold": record["fold"],
            "fold_log": record["fold_log"],
            "p_value": record["p_value"],
            "p_value_log": record["p_value_log"],
            "significance": significance_text
        }
        records_text.append(record_text)
    return records_text


def filter_measurements_significance(
    p_value_threshold=None,
    measurements_original=None
):
    """
    Filter measurements by a threshold for significance.

    arguments:
        p_value_threshold (float): p value threshold for significance
        measurements_original (list<dict>): information about measurements

    raises:

    returns:
        (list<dict>): information about measurements

    """

    measurements_novel = []
    for measurement in measurements_original:
        p_value = measurement["p_value"]
        if p_value < p_value_threshold:
            measurements_novel.append(measurement)
    return measurements_novel


def prepare_report_metaboanalyst(
    pair=None,
    normalization=None,
    summary=None,
    group_one=None,
    group_two=None,
    samples=None,
    measurements=None,
    signals=None
):
    """
    Prepares a report for analysis in MetaboAnalyst.

    arguments:
        pair (bool): whether samples have dependent pairs
        normalization (bool): whether to normalize measurements
        summary (list<dict<str>>): information about measurements for analytes
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Prepare metabolomic measurements for MetaboAnalyst.
    summary_unpair = prepare_summary_metaboanalyst(
        pair=False,
        normalization=normalization,
        summary=summary,
        group_one=group_one,
        group_two=group_two,
        samples=samples,
        measurements=measurements,
        signals=signals
    )
    if pair:
        summary_pair = prepare_summary_metaboanalyst(
            pair=True,
            normalization=normalization,
            summary=summary,
            group_one=group_one,
            group_two=group_two,
            samples=samples,
            measurements=measurements,
            signals=signals
        )
    else:
        summary_pair = None
    # Compile and return information.
    return {
        "unpair": summary_unpair,
        "pair": summary_pair
    }


def prepare_summary_metaboanalyst(
    pair=None,
    normalization=None,
    summary=None,
    group_one=None,
    group_two=None,
    samples=None,
    measurements=None,
    signals=None
):
    """
    Prepares a report for analysis in MetaboAnalyst.

    arguments:
        pair (bool): whether samples have dependent pairs
        normalization (bool): whether to normalize measurements
        summary (list<dict<str>>): information about measurements for analytes
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample

    raises:

    returns:
        (list<dict<str>>): information about measurements for analytes

    """

    # Collect identifiers of analytes that satisfy criteria for inclusion in
    # analysis.
    analytes_identifiers = utility.collect_value_from_records(
        key="identifier",
        records=summary
    )
    # Collect records in report.
    records = []
    # Prepare record of labels to designate pairs and groups of samples.
    samples_labels = determine_samples_labels(
        pair=pair,
        group_one=group_one,
        group_two=group_two,
        samples=samples
    )
    record_label = copy.deepcopy(samples_labels)
    record_label["sample"] = "label"
    records.append(record_label)
    # Normalize analyte's measurements by total signal for each sample.
    if normalization:
        measurements_normalization = normalize_measurements_samples_signals(
            summary=summary,
            group_one=group_one,
            group_two=group_two,
            samples=samples,
            measurements=measurements,
            signals=signals
        )
    else:
        measurements_normalization = measurements
    # Prepare records to match measurements to samples.
    for measurement in measurements_normalization:
        # Determine whether the measurement's analyte satisfies criteria for
        # inclusion in analysis.
        analyte_identifier = measurement["analyte"]
        if analyte_identifier in analytes_identifiers:
            # Determine analyte's name.
            analyte = find_analyte_record(
                identifier=analyte_identifier,
                analytes=summary
            )
            # Use PubChem identifier for analyte identifier.
            record_measurement = {
                #"sample": analyte["name"],
                "sample": analyte["references"]["pubchem"][0]
            }
            # Iterate on relevant samples.
            for sample in samples_labels.keys():
                # Determine whether a valid measurement exists for the sample.
                if (determine_measurements_validity(
                    samples=[sample],
                    measurements=measurement
                )):
                    record_measurement[sample] = str(measurement[sample])
                else:
                    record_measurement[sample] = str(0)
            records.append(record_measurement)
    # Return information.
    return records


def determine_samples_labels(
    pair=None,
    group_one=None,
    group_two=None,
    samples=None
):
    """
    Prepares a report for analysis in MetaboAnalyst.

    arguments:
        pair (bool): whether samples have dependent pairs
        group_one (str): name of experimental group
        group_two (str): name of experimental group
        samples (list<dict<str>>): information about samples from a study

    raises:

    returns:
        (dict<str>): labels for pairs and groups of samples

    """

    samples_labels = {}
    if pair:
        # Determine pairs of samples.
        pairs_samples = determine_pairs_samples(
            group_one=group_one,
            group_two=group_two,
            samples=samples
        )
        # Collect pairs of samples.
        for pair_samples in pairs_samples.values():
            pair = int(pair_samples["pair"])
            sample_one = pair_samples[group_one]
            sample_two = pair_samples[group_two]
            samples_labels[sample_one] = str(int(1 * pair))
            samples_labels[sample_two] = str(int(-1 * pair))
    else:
        # Determine all relevant samples.
        groups_samples = determine_groups_samples(
            group_one=group_one,
            group_two=group_two,
            samples=samples
        )
        # Collect groups of samples.
        for sample_one in groups_samples[group_one]:
            samples_labels[sample_one] = group_one
        for sample_two in groups_samples[group_two]:
            samples_labels[sample_two] = group_two
    return samples_labels


def determine_measurements_validity(
    samples=None,
    measurements=None
):
    """
    Determines whether valid measurements exist for samples.

    Valid measurements have a non-empty value that is great than zero.

    arguments:
        samples (list<str>): identifiers of samples
        measurements (dict<str>): information about measurements for an analyte

    raises:

    returns:
        (bool): whether valid measurements exist for samples

    """

    checks = []
    for sample in samples:
        check_existence = (
            sample in measurements.keys() and
            len(str(measurements[sample])) > 0
        )
        if check_existence:
            check_validity = (float(measurements[sample]) > 0)
            if check_validity:
                checks.append(True)
            else:
                checks.append(False)
        else:
            checks.append(False)
    return all(checks)


def prepare_report_analyte_metabolite_match(
    summary=None,
    metabolites=None
):
    """
    Prepares a report of matches of analytes to metabolites.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict<str>>): information about matches of analytes to metabolites

    """

    report = []
    for record_summary in summary:
        identifier_analyte = record_summary["identifier"]
        name_analyte = record_summary["name_original"]
        pubchem = record_summary["references"]["pubchem"]
        metabolites_analyte = record_summary["references"]["metabolite"]
        match = (len(metabolites_analyte) > 0)
        if match:
            match_value = "True"
            identifier_metabolite = metabolites_analyte[0]
            name_metabolite = metabolites[identifier_metabolite]["name"]
        else:
            match_value = "False"
            identifier_metabolite = "null"
            name_metabolite = "null"
        record = {
            "identifier_analyte": identifier_analyte,
            "name_analyte": name_analyte,
            "match": match_value,
            "identifier_metabolite": identifier_metabolite,
            "name_metabolite": name_metabolite,
            "reference_pubchem": pubchem
        }
        report.append(record)
    return report


# Match and translate samples' identifiers for measurements and signals.


def match_samples_measurements_signals(
    analyte=None,
    samples=None,
    analytes=None,
    measurements=None,
    signals=None,
    directory=None
):
    """
    Matches sample identifiers between measurements and signals.

    This curation procedure (metabocurator's measurement module) uses "named
    metabolite data" for measurements and "all metabolite data" for signals to
    normalize measurements.

    In Metabolomics Workbench, some studies do not have same sample identifiers
    for the "named metabolite data" as they do for the "all metabolite data".
    This function is useful to match these sample identifiers.

    arguments:
        analyte (str): identifier of an analyte to use to match samples
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample
        directory (str): path to directory for source and product files

    raises:

    returns:
        (list<dict<str>>): information about measurements and signals for all
            samples

    """

    # Sort samples by measurement values for a few analytes.
    # Compare sort sequences to match samples.
    # Common analytes include "alanine", "citric acid", and "asparagine".

    # Find measurements and signals for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=analyte,
        measurements=measurements
    )
    signals_analyte = find_analyte_measurements(
        identifier=analyte,
        measurements=signals
    )
    # Determine identifiers of samples.
    titles_measurements = list(measurements_analyte.keys())
    samples_measurements = list(filter(
        lambda value: value != "analyte",
        titles_measurements
    ))
    titles_signals = list(signals_analyte.keys())
    samples_signals = list(filter(
        lambda value: value != "analyte",
        titles_signals
    ))
    # Report sample identifiers.
    if False:
        print("measurements' samples: " + str(len(samples_measurements)))
        print(samples_measurements)
        print("signals' samples: " + str(len(samples_signals)))
        print(samples_signals)
    # Collect analyte measurements and signals for each sample.
    records_measurements = []
    for sample in samples_measurements:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=measurements_analyte
        )):
            value = float(measurements_analyte[sample])
        else:
            value = 0
        record = {
            "sample": sample,
            "value": value
        }
        records_measurements.append(record)
    records_signals = []
    for sample in samples_signals:
        if (determine_measurements_validity(
            samples=[sample],
            measurements=signals_analyte
        )):
            value = float(signals_analyte[sample])
        else:
            value = 0
        record = {
            "sample": sample,
            "value": value
        }
        records_signals.append(record)
    # Sort records by values.
    records_measurements.sort(
        key=lambda record: record["value"],
        reverse=False
    )
    records_signals.sort(
        key=lambda record: record["value"],
        reverse=False
    )
    # Specify directories and files.
    path = os.path.join(directory, "measurement_temporary")
    utility.confirm_path_directory(path)
    path_measurements = os.path.join(path, "measurements.tsv")
    path_signals = os.path.join(path, "signals.tsv")
    # Write information to file.
    utility.write_file_table(
        information=records_measurements,
        path_file=path_measurements,
        names=records_measurements[0].keys(),
        delimiter="\t"
    )
    utility.write_file_table(
        information=records_signals,
        path_file=path_signals,
        names=records_signals[0].keys(),
        delimiter="\t"
    )
    pass


def translate_samples_identifiers(
    translations=None,
    signals=None,
    directory=None
):
    """
    Translates samples' identifiers in signals to match measurements.

    arguments:
        translations (list<dict<str>>): identifiers of samples for measurements
            and signals
        signals (list<dict<str>>): information about total signals for each
            sample
        directory (str): path to directory for source and product files

    raises:

    returns:
        (list<dict<str>>): identifiers of samples for signals

    """

    # Collect translations.
    translations_reference = {}
    for translation in translations:
        identifier_measurement = translation["measurement"]
        identifier_signal = translation["signal"]
        translations_reference[identifier_signal] = identifier_measurement
    # Translate samples' identifiers in signals.
    signals_translation = []
    for signal in signals:
        record = {}
        record["analyte"] = signal["analyte"]
        titles = list(signal.keys())
        samples = list(filter(lambda value: value != "analyte", titles))
        for sample in samples:
            if sample in translations_reference.keys():
                sample_translation = translations_reference[sample]
            else:
                sample_translation = sample
            record[sample_translation] = signal[sample]
        signals_translation.append(record)
    # Specify directories and files.
    path = os.path.join(directory, "measurement_temporary")
    utility.confirm_path_directory(path)
    path_signals = os.path.join(path, "signals.tsv")
    # Write information to file.
    utility.write_file_table(
        information=signals_translation,
        path_file=path_signals,
        names=signals_translation[0].keys(),
        delimiter="\t"
    )
    pass


def compare_samples_measurements_signals(
    analyte=None,
    measurements=None,
    signals=None
):
    """
    Compares values of measurements and signals for samples.

    arguments:
        analyte (str): identifier of an analyte to use to match samples
        measurements (list<dict<str>>): information about measurements from a
            study
        signals (list<dict<str>>): information about total signals for each
            sample

    raises:

    returns:

    """

    # Find measurements and signals for analyte.
    measurements_analyte = find_analyte_measurements(
        identifier=analyte,
        measurements=measurements
    )
    signals_analyte = find_analyte_measurements(
        identifier=analyte,
        measurements=signals
    )
    # Determine identifiers of samples.
    titles_measurements = list(measurements_analyte.keys())
    samples_measurements = list(filter(
        lambda value: value != "analyte",
        titles_measurements
    ))
    titles_signals = list(signals_analyte.keys())
    samples_signals = list(filter(
        lambda value: value != "analyte",
        titles_signals
    ))
    # Report samples' values of measurement and signal.
    for sample in samples_measurements:
        if sample in measurements_analyte.keys():
            measurement = measurements_analyte[sample]
        else:
            measurement = "null"
        if sample in signals_analyte.keys():
            signal = signals_analyte[sample]
        else:
            signal = "null"
        print("----------")
        print("measurement: " + measurement)
        print("signal:      " + signal)
    tests = []
    for sample in samples_measurements:
        if sample in measurements_analyte.keys():
            measurement = round(float(measurements_analyte[sample]), 0)
        else:
            measurement = 0
        if sample in signals_analyte.keys():
            signal = float(signals_analyte[sample])
        else:
            signal = 0
        test = (measurement == signal)
        tests.append(test)
    print("all equal? : " + str(all(tests)))

    pass


def prepare_curation_report(
    summary=None
):
    """
    Prepares a summary report on curation of metabolic sets and entities.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    returns:
        (str): report of summary information

    raises:

    """

    # Count measurements.
    count_analytes = len(summary)
    # Count measurements with references to Human Metabolome Database (HMDB).
    count_hmdb = count_records_with_references(
        references=["hmdb"],
        records=summary
    )
    proportion_hmdb = count_hmdb / count_analytes
    percentage_hmdb = round((proportion_hmdb * 100), 2)
    # Count measurements with references to Human Metabolome Database (HMDB).
    count_pubchem = count_records_with_references(
        references=["pubchem"],
        records=summary
    )
    proportion_pubchem = count_pubchem / count_analytes
    percentage_pubchem = round((proportion_pubchem * 100), 2)
    # Count measurements with references to Human Metabolome Database (HMDB).
    count_metab = count_records_with_references(
        references=["metabolite"],
        records=summary
    )
    proportion_metabolite = count_metab / count_analytes
    percent_metabolite = round((proportion_metabolite * 100), 2)
    # Determine minimal and maximal base-2 logarithm fold changes.
    minimum, maximum = determine_fold_logarithm_extremes(summary=summary)
    # Determine minimal base-10 logarithm p-value.
    minimum_p_value_log = determine_p_value_logarithm_minimum(summary=summary)
    # Compile information.
    report = textwrap.dedent("""\

        --------------------------------------------------
        curation report

        analytes: {count_analytes}

        measurements with metabolite: {count_metab} ({percent_metabolite} %)
        measurements with PubChem: {count_pubchem} ({percentage_pubchem} %)
        measurements with HMDB: {count_hmdb} ({percentage_hmdb} %)

        minimal log-2 fold change: {minimum}
        maximal log-2 fold change: {maximum}
        minimal log-10 p-value: {minimum_p_value_log}

        --------------------------------------------------
    """).format(
        count_analytes=count_analytes,
        count_hmdb=count_hmdb,
        percentage_hmdb=percentage_hmdb,
        count_pubchem=count_pubchem,
        percentage_pubchem=percentage_pubchem,
        count_metab=count_metab,
        percent_metabolite=percent_metabolite,
        minimum=minimum,
        maximum=maximum,
        minimum_p_value_log=minimum_p_value_log
    )
    # Return information.
    return report


def count_records_with_references(references=None, records=None):
    """
    Counts entities with any of specific references.

    arguments:
        references (list<str>): identifiers of references
        records (list<dict>): information in records

    returns:
        (int): count of records with specific reference

    raises:

    """

    count = 0
    for record in records:
        matches = []
        for reference in references:
            if reference in record["references"].keys():
                if len(record["references"][reference]) > 0:
                    matches.append(True)
        if any(matches):
            count += 1
    return count


def determine_fold_logarithm_extremes(
    summary=None
):
    """
    Determines minimal and maximal values of base-2 logarithms of fold changes.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    raises:

    returns:
        (tuple<float, float>): minimal and maximal values of base-2 logarithms
            of fold changes

    """

    values = utility.collect_value_from_records(
        key="fold_log", records=summary
    )
    maximum = max(values)
    minimum = min(values)
    return (minimum, maximum)


def determine_p_value_logarithm_minimum(
    summary=None
):
    """
    Determines minimal value of base-10 logarithm of p-values.

    arguments:
        summary (list<dict<str>>): information about measurements for analytes

    raises:

    returns:
        (float): minimal value of base-10 logarithm of p-value

    """

    values = utility.collect_value_from_records(
        key="p_value_log", records=summary
    )
    minimum = min(values)
    return minimum


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
    # Write information to file.
    path = os.path.join(directory, "measurement")
    utility.confirm_path_directory(path)
    write_product_study(study="study_one", path=path, information=information)
    write_product_study(study="study_two", path=path, information=information)
    write_product_study(
        study="study_three", path=path, information=information
    )
    write_product_study(study="study_four", path=path, information=information)
    write_product_study(study="study_five", path=path, information=information)
    pass


def write_product_study(study=None, path=None, information=None):
    """
    Writes product information to file

    arguments:
        study (str): name of study
        path (str): path to directory
        information (object): information to write to file

    raises:

    returns:

    """

    # Specify directories and files.
    path_pickle = os.path.join(path, (study + ".pickle"))
    path_text = os.path.join(path, (study + ".tsv"))
    path_metaboanalyst = os.path.join(path, (study + "_metaboanalyst.txt"))
    path_metaboanalyst_pair = os.path.join(path, (
        study + "_metaboanalyst_pair.txt"
    ))
    path_report = os.path.join(path, (study + "_report.tsv"))
    # Write information to file.
    with open(path_pickle, "wb") as file_product:
        pickle.dump(information[study]["summary"], file_product)
    utility.write_file_table(
        information=information[study]["summary_text"],
        path_file=path_text,
        names=information[study]["summary_text"][0].keys(),
        delimiter="\t"
    )
    # Specify order of columns.
    names = list(information[study]["summary_metaboanalyst"][0].keys())
    names_minus = list(filter(lambda value: value != "sample", names))
    names_sequence = ["sample"]
    names_sequence.extend(names_minus)
    utility.write_file_table(
        information=information[study]["summary_metaboanalyst"],
        path_file=path_metaboanalyst,
        names=names_sequence,
        delimiter="\t"
    )
    if information[study]["summary_metaboanalyst_pair"] is not None:
        utility.write_file_table(
            information=information[study]["summary_metaboanalyst_pair"],
            path_file=path_metaboanalyst_pair,
            names=names_sequence,
            delimiter="\t"
        )
    utility.write_file_table(
        information=information[study]["report_match"],
        path_file=path_report,
        names=information[study]["report_match"][0].keys(),
        delimiter="\t"
    )


###############################################################################
# Procedure


def execute_procedure(directory=None):
    """
    Function to execute module's main behavior.

    The purpose of this procedure is to extract relevant information from the
    Human Metabolome Database.

    arguments:
        directory (str): path to directory for source and product files

    raises:

    returns:

    """

    # Read source information from file.
    source = read_source(directory=directory)
    # Curate samples' identifiers.
    # "citric acid", "alanine", "asparagine", "pyruvic acid"
    if False:
        match_samples_measurements_signals(
            analyte="citric acid",
            samples=source["study_one"]["samples"],
            analytes=source["study_one"]["analytes"],
            measurements=source["study_one"]["measurements"],
            signals=source["study_one"]["signals"],
            directory=directory
        )
        translate_samples_identifiers(
            translations=source["study_one"]["translations"],
            signals=source["study_one"]["signals"],
            directory=directory
        )
        compare_samples_measurements_signals(
            analyte="pyruvic acid",
            measurements=source["study_one"]["measurements"],
            signals=source["study_one"]["signals"]
        )
    # Curate measurements from study zero.
    # Measurements from study one represent metabolites in plasma before and
    # after exercise.
    if False:
        study_zero = curate_measurements_study_zero(
            measurements=source["study_zero"]["measurements"]
        )
    #
    # Analyze measurements from all studies without pairs of samples.
    #
    # Curate measurements from study two.
    # Measurements from study two represent metabolites in normal versus tumor
    # lung.
    study_one = curate_study(
        pair=True,
        normalization=True,
        group_numerator="tumor",
        group_denominator="normal",
        samples=source["study_one"]["samples"],
        analytes=source["study_one"]["analytes"],
        measurements=source["study_one"]["measurements"],
        signals=source["study_one"]["signals"],
        hmdb=source["reference"]["hmdb"],
        metabolites=source["reference"]["metabolites"]
    )

    # Curate measurements from study one.
    # Measurements from study two represent metabolites in visceral versus
    # subcutaneous adipose.
    study_two = curate_study(
        pair=True,
        normalization=True,
        group_numerator="visceral_fat",
        group_denominator="subcutaneous_fat",
        samples=source["study_two"]["samples"],
        analytes=source["study_two"]["analytes"],
        measurements=source["study_two"]["measurements"],
        signals=source["study_two"]["signals"],
        hmdb=source["reference"]["hmdb"],
        metabolites=source["reference"]["metabolites"]
    )
    # Curate measurements from study three.
    study_three = curate_study(
        pair=False,
        normalization=True,
        group_numerator="ischemia",
        group_denominator="normal",
        samples=source["study_three_four"]["samples"],
        analytes=source["study_three_four"]["analytes"],
        measurements=source["study_three_four"]["measurements"],
        signals=source["study_three_four"]["signals"],
        hmdb=source["reference"]["hmdb"],
        metabolites=source["reference"]["metabolites"]
    )
    # Curate measurements from study four.
    study_four = curate_study(
        pair=False,
        normalization=True,
        group_numerator="steatosis",
        group_denominator="normal",
        samples=source["study_three_four"]["samples"],
        analytes=source["study_three_four"]["analytes"],
        measurements=source["study_three_four"]["measurements"],
        signals=source["study_three_four"]["signals"],
        hmdb=source["reference"]["hmdb"],
        metabolites=source["reference"]["metabolites"]
    )
    # Curate measurements from study five.
    study_five = curate_study(
        pair=True,
        normalization=True,
        group_numerator="after_exercise",
        group_denominator="before_exercise",
        samples=source["study_five"]["samples"],
        analytes=source["study_five"]["analytes"],
        measurements=source["study_five"]["measurements"],
        signals=source["study_five"]["signals"],
        hmdb=source["reference"]["hmdb"],
        metabolites=source["reference"]["metabolites"]
    )
    # Compile information.
    information = {
        "study_one": study_one,
        "study_two": study_two,
        "study_three": study_three,
        "study_four": study_four,
        "study_five": study_five
    }
    #Write product information to file
    write_product(directory=directory, information=information)
    pass
