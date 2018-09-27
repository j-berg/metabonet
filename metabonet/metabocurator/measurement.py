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
#import scipy

# Packages and modules from local source

import utility

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
    # Read information from file.
    # Compile information.
    reference = read_source_reference(directory=directory)
    study_one = read_source_study_one(directory=directory)
    study_two = read_source_study_two(directory=directory)
    # Compile and return information.
    return {
        "reference": reference,
        "study_one": study_one,
        "study_two": study_two
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
    path_conversion = os.path.join(directory, "conversion")
    path_metabolites = os.path.join(path_conversion, "metabolites.pickle")
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


def read_source_study_one(directory=None):
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
    path_study_one = os.path.join(
        path_measurement, "karl_physiological-reports_2017"
    )
    path_measurements = os.path.join(
        path_study_one, "measurements.tsv"
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


def read_source_study_two(directory=None):
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
    path_study_two = os.path.join(
        path_measurement, "metabolomics-workbench_pr000058_st000061"
    )
    path_samples = os.path.join(path_study_two, "samples.tsv")
    path_analytes = os.path.join(path_study_two, "analytes.tsv")
    path_measurements = os.path.join(path_study_two, "measurements.tsv")
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
    # Compile and return information.
    return {
        "samples": samples,
        "analytes": analytes,
        "measurements": measurements
    }


# Study one.


def curate_measurements_study_one(measurements=None):
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


def extract_measurements_study_one(records=None):
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


# Study two.


def curate_measurements_study_two(
    samples=None,
    analytes=None,
    measurements=None,
    hmdb=None,
    metabolites=None
):
    """
    Curates information about metabolomic measurements from a study.

    arguments:
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information measurements from a study
        hmdb (dict<dict>): information about metabolites from Human Metabolome
            Database (HMDB)
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict>): information about measurements

    """

    # Determine analytes' mean fold changes between groups.
    analytes_fold = determine_study_two_analytes_folds(
        group_numerator="subcutaneous_fat",
        group_denominator="visceral_fat",
        samples=samples,
        analytes=analytes,
        measurements=measurements
    )
    # Determine analytes' log-2 fold changes between groups.
    analytes_log = calculate_measurements_log(
        measurements_original=analytes_fold
    )
    # Determine analytes' p-values between groups.
    analytes_p = determine_study_two_analytes_p_values(
        samples=samples,
        analytes=analytes,
        measurements=measurements
    )


    # Match analytes to metabolites.

    # Compile and return information.
    return analytes_fold


def determine_study_two_analytes_folds(
    group_numerator=None,
    group_denominator=None,
    samples=None,
    analytes=None,
    measurements=None
):
    """
    Determines the mean fold changes for each analyte between experimental
    groups.

    arguments:
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information measurements from a study

    raises:

    returns:
        (list<dict>): information about measurements

    """

    # Determine identifiers of samples for same patients.
    patients_samples = determine_study_two_patients_samples(
        samples=samples
    )
    # Determine mean fold changes for each analyte.
    analytes_novel = []
    for analyte in analytes:
        name = analyte["name_study"]
        fold = determine_study_two_analyte_fold(
            analyte=name,
            group_numerator=group_numerator,
            group_denominator=group_denominator,
            patients_samples=patients_samples,
            measurements=measurements
        )
        analyte["fold"] = fold
        analytes_novel.append(analyte)
    return analytes_novel


def determine_study_two_patients_samples(
    samples=None
):
    """
    Determines the samples for each group for the same patient.

    arguments:
        samples (list<dict<str>>): information about samples from a study

    raises:

    returns:
        (dict): samples from each group for each patient

    """

    patients_samples = {}
    for sample_cis in samples:
        identifier_cis = sample_cis["identifier"]
        patient_cis = str(sample_cis["patient"])
        group_cis = sample_cis["group"]
        if patient_cis not in patients_samples.keys():
            # Find sample for same patient and other group.
            for sample_trans in samples:
                identifier_trans = sample_trans["identifier"]
                patient_trans = str(sample_trans["patient"])
                group_trans = sample_trans["group"]
                if (
                    (patient_trans == patient_cis) and
                    (group_trans != group_cis)
                ):
                    # Found the other sample for the same patient.
                    break
            patients_samples[patient_cis] = {
                group_cis: identifier_cis,
                group_trans: identifier_trans
            }
    return patients_samples


def determine_study_two_analyte_fold(
    analyte=None,
    group_numerator=None,
    group_denominator=None,
    patients_samples=None,
    measurements=None
):
    """
    Determines the mean fold change between experimental groups for an analyte.

    arguments:
        analyte (str): name of analyte
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        patients_samples (dict): samples from each group for each patient
        measurements (list<dict<str>>): information measurements from a study

    raises:

    returns:
        (float): fold change

    """

    # Find measurements for analyte.
    def match(record):
        return record["analyte"] == analyte
    measurements_analyte = utility.find(
        match=match,
        sequence=measurements
    )
    # Determine fold changes for analyte's measurements.
    folds = []
    for patient in patients_samples.keys():
        sample_numerator = patients_samples[patient][group_numerator]
        sample_denominator = patients_samples[patient][group_denominator]
        if (
            (sample_numerator in measurements_analyte.keys()) and
            (sample_denominator in measurements_analyte.keys())
        ):
            numerator = float(measurements_analyte[sample_numerator])
            denominator = float(measurements_analyte[sample_denominator])
            fold = numerator / denominator
            folds.append(fold)
    mean = statistics.mean(folds)
    return mean


def determine_study_two_analytes_p_values(
    samples=None,
    analytes=None,
    measurements=None
):
    """
    Determines the mean fold changes for each analyte between experimental
    groups.

    arguments:
        group_numerator (str): name of experimental group for numerator
        group_denominator (str): name of experimental group for denominator
        samples (list<dict<str>>): information about samples from a study
        analytes (list<dict<str>>): information about analytes from a study
        measurements (list<dict<str>>): information measurements from a study

    raises:

    returns:
        (list<dict>): information about measurements

    """

    # Determine identifiers of samples for each group.
    groups_samples = determine_study_two_groups_samples(
        samples=samples
    )
    # Determine p-value for each analyte.
    analytes_novel = []
    for analyte in analytes:
        name = analyte["name_study"]
        p_value = determine_study_two_analyte_p_value(
            analyte=name,
            groups_samples=groups_samples,
            measurements=measurements
        )
        analyte["p_value"] = p_value
        analytes_novel.append(analyte)
    return analytes_novel


def determine_study_two_groups_samples(
    samples=None
):
    """
    Determines the samples for each group.

    arguments:
        samples (list<dict<str>>): information about samples from a study

    raises:

    returns:
        (dict): samples from each group for each patient

    """

    # TODO: Change this so that measuremes are in order by patient?

    groups_samples = {}
    for sample in samples:
        identifier = sample["identifier"]
        group = sample["group"]
        if group not in groups_samples.keys():
            groups_samples[group] = [identifier]
        else:
            groups_samples[group].append(identifier)
    return groups_samples


def determine_study_two_analyte_p_value(
    analyte=None,
    groups_samples=None,
    measurements=None
):
    """
    Determines the p-value between experimental groups for an analyte.

    arguments:
        analyte (str): name of analyte
        groups_samples (dict): samples from each group
        measurements (list<dict<str>>): information measurements from a study

    raises:

    returns:
        (float): p-value

    """

    # Find measurements for analyte.
    def match(record):
        return record["analyte"] == analyte
    measurements_analyte = utility.find(
        match=match,
        sequence=measurements
    )
    # Collect measurements for each experimental group.
    group_one = list(groups_samples.keys())[0]
    group_two = list(groups_samples.keys())[1]
    groups_measurements = {
        group_one: [],
        group_two: []
    }
    for group in groups_samples.keys():
        for sample in groups_samples[group]:
            if sample in measurements_analyte.keys():
                measurement = float(measurements_analyte[sample])
                groups_measurements[group].append(measurement)
    # Determine p-values for analyte's measurements.
    print("here are the group measurements")
    print(groups_measurements)
    #mean = statistics.mean(folds)
    #return mean



# General utility.


def calculate_measurements_log(measurements_original=None):
    """
    Calculates base-2 logarithm of fold change in measurements.

    arguments:
        measurements_original (list<dict>): information about measurements

    raises:

    returns:
        (list<dict>): information about measurements

    """

    measurements_novel = []
    for measurement in measurements_original:
        fold = measurement["fold"]
        measurement["log_fold"] = math.log(fold, 2)
        measurements_novel.append(measurement)
    return measurements_novel


# TODO: do I also need to enhance PubChem references?

def enhance_measurements_hmdb_references(
    measurements_original=None, summary_hmdb=None
):
    """
    Enhances measurements' references to Human Metabolome Database (HMDB).

    arguments:
        measurements_original (list<dict>): information about measurements
        summary_hmdb (dict<dict>): information about metabolites from Human
            Metabolome Database (HMDB)

    raises:

    returns:
        (list<dict>): information about measurements

    """

    measurements_novel = []
    for measurement in measurements_original:
        reference_hmdb = measurement["hmdb"]
        name = measurement["name"]
        hmdb_keys = utility.match_hmdb_entries_by_identifiers_names(
            identifiers=[reference_hmdb],
            names=[name],
            summary_hmdb=summary_hmdb
        )
        del measurement["hmdb"]
        measurement["hmdb"] = hmdb_keys
        measurements_novel.append(measurement)
    return measurements_novel


def match_measurements_to_metabolites(
    reference=None,
    measurements_original=None,
    metabolites=None
):
    """
    Matches measurements to metabolites.

    arguments:
        reference (str): name of attribute to use for match
        measurements_original (list<dict>): information about measurements
        metabolites (dict<dict>): information about metabolites

    raises:

    returns:
        (list<dict>): information about measurements

    """

    measurements_novel = []
    for measurement in measurements_original:
        references_measurement = measurement[reference]
        # Find metabolites that match the reference.
        metabolites_matches = []
        for metabolite in metabolites.values():
            references_metabolite = metabolite["references"][reference]
            # Determine whether any measurement references match metabolite
            # references.
            matches = utility.filter_common_elements(
                list_one=references_measurement,
                list_two=references_metabolite
            )
            if len(matches) > 0:
                metabolites_matches.append(metabolite["identifier"])
        measurement["metabolites"] = metabolites_matches
        measurements_novel.append(measurement)
    return measurements_novel


def filter_measurements_metabolites(
    measurements_original=None
):
    """
    Filter measurements for those that map to metabolites.

    arguments:
        measurements_original (list<dict>): information about measurements

    raises:

    returns:
        (list<dict>): information about measurements

    """

    measurements_novel = []
    for measurement in measurements_original:
        metabolites = measurement["metabolites"]
        if len(metabolites) > 0:
            measurements_novel.append(measurement)
    return measurements_novel


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


def convert_measurements_text(measurements=None):
    """
    Converts information about measurements to text format.

    arguments:
        measurements_original (list<dict>): information about measurements

    returns:
        (list<dict>): information about measurements

    raises:

    """

    records = []
    for measurement in measurements:
        record = {
            "name": measurement["name"],
            "fold": measurement["fold"],
            "log_fold": measurement["log_fold"],
            "p_value": measurement["p_value"],
            "hmdb": ";".join(measurement["hmdb"]),
            "metabolites": ";".join(measurement["metabolites"])
        }
        records.append(record)
    return records


def prepare_curation_report(
    measurements=None
):
    """
    Prepares a summary report on curation of metabolic sets and entities.

    arguments:
        measurements (list<dict>): information about measurements

    returns:
        (str): report of summary information

    raises:

    """

    # Count measurements.
    count_measurements = len(measurements)
    # Count measurements with references to Human Metabolome Database (HMDB).
    count_hmdb = count_records_with_references(
        references=["hmdb"],
        records=measurements
    )
    proportion_hmdb = count_hmdb / count_measurements
    percentage_hmdb = round((proportion_hmdb * 100), 2)
    # Count measurements with references to Human Metabolome Database (HMDB).
    count_metab = count_records_with_references(
        references=["metabolites"],
        records=measurements
    )
    proportion_metabolite = count_metab / count_measurements
    percent_metabolite = round((proportion_metabolite * 100), 2)
    # Compile information.
    report = textwrap.dedent("""\

        --------------------------------------------------
        curation report

        measurements: {count_measurements}

        measurements with HMDB: {count_hmdb} ({percentage_hmdb} %)
        measurements with metabolite: {count_metab} ({percent_metabolite} %)

        --------------------------------------------------
    """).format(
        count_measurements=count_measurements,
        count_hmdb=count_hmdb,
        percentage_hmdb=percentage_hmdb,
        count_metab=count_metab,
        percent_metabolite=percent_metabolite
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
            if reference in record.keys():
                if len(record[reference]) > 0:
                    matches.append(True)
        if any(matches):
            count += 1
    return count


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
    path = os.path.join(directory, "measurement")
    utility.confirm_path_directory(path)
    path_pickle = os.path.join(path, "measurements.pickle")
    path_text = os.path.join(path, "measurements.tsv")
    # Write information to file.
    with open(path_pickle, "wb") as file_product:
        pickle.dump(information["measurements"], file_product)
    utility.write_file_table(
        information=information["measurements_text"],
        path_file=path_text,
        names=information["measurements_text"][0].keys(),
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
    # Curate measurements from study one.
    # Measurements from study one represent metabolites in plasma before and
    # after exercise.
    if False:
        study_one = curate_measurements_study_one(
            measurements=source["study_one"]["measurements"]
        )
    # Curate measurements from study two.
    # Measurements from study two represent metabolites in visceral and
    # subcutaneous adipose.
    study_two = curate_measurements_study_two(
        samples=source["study_two"]["samples"],
        analytes=source["study_two"]["analytes"],
        measurements=source["study_two"]["measurements"]
    )



    if False:
        # Compile information.
        information = {
            "measurements_one": measurements_significance,
            "measurements_one_text": measurements_text
        }
        #Write product information to file
        write_product(directory=directory, information=information)
        # Report.
        print("measurements before curation...")
        report = prepare_curation_report(
            measurements=measurements
        )
        print(report)
        print("measurements after enhancement of HMDB and metabolites")
        report = prepare_curation_report(
            measurements=measurements_metabolites
        )
        print(report)
        print("measurements after curation and filters...")
        report = prepare_curation_report(
            measurements=measurements_significance
        )
        print(report)
