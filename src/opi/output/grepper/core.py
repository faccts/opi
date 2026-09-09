from collections.abc import Callable, Iterator
from pathlib import Path
from re import IGNORECASE, Pattern, RegexFlag, compile, escape, split
from typing import Any

from opi.output.grepper.pre_condition import (
    ConditionStatus,
    PreCondition,
)


def str2regex(string: str | Pattern[str], flags: RegexFlag | None = None, /) -> Pattern[str]:
    """
    Translates a plain string into a re.Pattern from regex

    Parameters
    ----------
    string : str
        string that gets transformed
    flags : RegexFlag | None, default: None
        Flags from the `re` module to be incorporated into the Pattern object.

    Returns
    -------
    Pattern
        transformed string
    """
    if isinstance(string, Pattern):
        return string
    if flags:
        return compile(escape(string), flags)
    else:
        return compile(escape(string))


def index_in_list(list_to_check: list[str], index: int | None) -> bool:
    """
    Checks if an index is in range or out of range

    Parameters
    ----------
    list_to_check : list[str]
        list that gets checked
    index : int | None
        index to check

    Returns
    -------
    bool
        True if index is in range, else False
    """

    length = len(list_to_check)
    if index is None:
        return True
    else:
        return bool(-length <= int(index) < length)


class Grepper:
    """
    This class can access a file and search for pattern inside it

    Attributes
    ----------
    file: Path
        Path to the file that gets searched
    """

    def __init__(self, file: Path) -> None:
        self.file = file
        self._search_completed: bool = False
        self.pattern: Pattern[str] | None = None

    def search(
        self,
        pattern: str | Pattern[str],
        /,
        *,
        pre_conditions: list[PreCondition] | None = None,
        kind: Callable[[str], Any] = str,
        case_sensitive: bool = False,
        field_sep: str = " ",
        trim_whitespaces: bool = True,
        merge_sep: bool = True,
        fallback: Any | None = None,
        skip_lines: int = 0,
        field: int | None = None,
        matching_pattern: int | None = None,
    ) -> list[Any] | Any:
        """
        Search function that search for `pattern` in given file.

        Parameters
        ----------
        pattern : str | Pattern[str]
            String or pattern to search for.
        pre_conditions : list[PreCondition] | None, default: None
            List of conditions that have to be meet before searching for `pattern`.
        kind : Callable[[str], Any], default: str
            Any method that takes a single string return, the desired data type.
        case_sensitive : bool , default: False
            Do not ignore case distinctions in file.
            Only applies if `pattern` is a string and not a `Pattern` object.
        field_sep : str, default: " "
            String delimiters that separates adjacent fields.
        trim_whitespaces :bool, default: True
            Trim leading and trailing whitespaces from matches.
        merge_sep :bool, default: True
            Treat consecutive field delimiters as one.
        fallback : Any | None = None
            Value, that is returned if no matching_pattern is found.
        skip_lines : int[n >= 0], default: 0
            Skip `n` lines after finding a matching_pattern. Further arguments apply to that `n`th after the matching_pattern.
        field : int[-Y <= n <= (Y-1)] | None, default: None
            Instead of return the whole line that matches, return the `n`th field from the line.
            The line is split into field according to `field_sep` and `merge_sep`.
            `Y` is the number of fields in the.
            Counting starts from 0, i.e. the first field is 0.
            If `n` is smaller 0, fields are access in reverse order.
            If `None` return entire line.
        matching_pattern : int[-Y <= n <= (Y-1)] | None, default: None
            Return the `n`th matching_pattern.
            For `n` the same conditions apply as with `field`.
            'None' means return all matches (as list). `kind` is applied to every item of the list.
            All parameters mentioned above effecting processing conditions apply for each matching_pattern.

        Returns
        -------
        A list of converted values to the desired data type using `kind`

        If no matching_pattern is found `fallback` is returned.
        """
        self._search_completed = False
        if not case_sensitive:
            flags = IGNORECASE
        else:
            flags = None

        if isinstance(pattern, str):
            # > convert string to regex pattern
            self.pattern = str2regex(pattern, flags)
        else:
            self.pattern = pattern

        if merge_sep:
            field_sep += "+"
        # > Searches for the `PreCondition` and collects the matches of the main pattern
        matches: list[str] = self.search_through_lines(pre_conditions, skip_lines)
        # > returns the wanted field and match form all matches
        reduced_matches: list[str] = self.reduce_matches(
            matches, matching_pattern, field, field_sep, trim_whitespaces, fallback
        )
        if reduced_matches != fallback:
            # > converts match/matches to the type defined by kind
            return_value: list[Any] = self.convert_matches(reduced_matches, kind, fallback)
        else:
            return_value = fallback
        return return_value

    def open_file(self) -> Iterator[str]:
        """
        Opens the file and yields the lines

        Returns
        -------
        Iterator[str]
        """
        return self.file.open()

    def search_through_lines(
        self, pre_conditions: list[PreCondition] | None, skip_lines: int | None
    ) -> list[str]:
        """
        Determines whether a `PreCondition` pattern or pattern is searched and calls the correct function until search is completed

        Parameters
        ----------
        pre_conditions : list[PreCondition]| None
            condition that have to be fulfilled before the pattern can be searched
        skip_lines : int| None
            Numbers of lines that are skipped, after pattern is found

        Returns
        -------
        list[str]
            List containing all the lines that are a matching_pattern for the main search
        """
        pre_condition_search: bool = bool(pre_conditions)
        first_time: bool = True
        matches: list[str] = []

        file = self.open_file()
        while True:
            while pre_condition_search and not self._search_completed and pre_conditions:
                # > searches for the pre conditions in the file
                pre_conditions_in_file = self.search_for_precondition(
                    file, pre_conditions, first_time
                )
                # > checks if pre conditions are found
                pre_conditions_found = self.condition_found(pre_conditions_in_file)
                if pre_conditions_found:
                    first_time = False
                    pre_condition_search = False
            # < searches for the pattern in the file
            line = self.search_for_pattern(file)

            if not self._search_completed:
                try:
                    if isinstance(skip_lines, int):
                        for _ in range(skip_lines):
                            line = next(file)
                    if line:
                        matches.append(line)
                    pre_condition_search = bool(pre_conditions)
                except StopIteration:
                    self._search_completed = True
            else:
                return matches

    def search_for_precondition(
        self,
        file: Iterator[str],
        pre_conditions: list[PreCondition],
        first_time: bool,
    ) -> list[PreCondition]:
        """
        Searches for all the pre conditions that needs to be searched

        Parameters
        ----------
        file : Iterator[str]
            The lines of the file
        pre_conditions : list[PreConditions]
            list of all the pre conditions
        first_time : bool
            Is that the first time searching for the pre conditions

        Returns
        -------
        list[PreConditions]
        """
        try:
            line: str = next(file)
        except StopIteration:
            self._search_completed = True
        else:
            for condition in pre_conditions:
                if isinstance(condition.pattern, str):
                    condition.pattern = str2regex(condition.pattern, None)
                line_counter = 0
                # > Checks if condition search is needed
                if first_time or condition.per_match:
                    condition.condition_information = ConditionStatus()
                    while not bool(condition.condition_information):
                        if not condition.pattern.search(line):
                            line_counter = +1
                            try:
                                line = next(file)
                            except StopIteration:
                                self._search_completed = True
                                return pre_conditions
                            # > checks if the search is within the search scope
                        if condition.within:
                            if not line_counter - condition.within:
                                return pre_conditions
                        if condition.pattern.search(line):
                            condition.condition_information.condition_found = True
                            condition.condition_information.line = line
        return pre_conditions

    @staticmethod
    def condition_found(pre_conditions: list[PreCondition]) -> bool:
        """
        Checks if all `PreCondition` where found

        Parameters
        ----------
        pre_conditions : list[PreCondition]
            List of all pre conditions
        """
        for condition in pre_conditions:
            if not bool(condition.condition_information):
                return False

        return True

    def search_for_pattern(self, file: Iterator[str]) -> str | None:
        """
        Searches for the pattern

        Parameters
        ----------
        file : Iterator[str]
            The lines of the file

        Returns
        -------
        str | None
            Last checked line, None if last line has been searched
        """
        try:
            line = next(file)
        except StopIteration:
            self._search_completed = True
        else:
            while not self._search_completed:
                assert self.pattern
                if self.pattern.search(line):
                    return line
                else:
                    try:
                        line = next(file)
                    except StopIteration:
                        self._search_completed = True
        return None

    @staticmethod
    def reduce_matches(
        matches: list[str],
        matching_pattern: int | None,
        field: int | None,
        field_sep: str,
        trim_whitespaces: bool,
        fallback: Any,
    ) -> list[str] | Any:
        """
        Reduces the matches, so only wanted information is returned

        Parameters
        ----------
        matches : list[str] | list[()]
            List of all found matches
        matching_pattern : int[-Y <= n <= (Y-1)] | None
            Return the `n`th matching_pattern.
            For `n` the same conditions apply as with `field`.
            'None' means return all matches (as list). `kind` is applied to every item of the list.
            All parameters mentioned above effecting processing conditions apply for each matching_pattern.
        field : int[-Y <= n <= (Y-1)] | None
            Instead of return the whole line that matches, return the `n`th field from the line.
            The line is split into field according to `field_sep` and `merge_sep`.
            `Y` is the number of fields in the.
            Counting starts from 0, i.e. the first field is 0.
            If `n` is smaller 0, fields are access in reverse order.
            If `None` return entire line.
        field_sep : str
            String delimiters that separates adjacent fields
        trim_whitespaces : bool
            Trim leading and trailing whitespaces from matches
        fallback : Any
            Value that gets returned if no matches where found or matching_pattern or field are out of bounds

        Returns
        -------
        list[str]| Any
            Reduced list or fallback
        """
        if not matches:
            return fallback
        match_in_matches: list[str] = []
        if matching_pattern is not None and index_in_list(matches, matching_pattern):
            match_in_matches.append(matches[matching_pattern])
        elif matches is not None and not index_in_list(matches, matching_pattern):
            return fallback
        else:
            match_in_matches = matches
        if field is not None:
            match_field = []
            for index in range(len(match_in_matches)):
                split_field = split(field_sep, match_in_matches[index])
                if index_in_list(split_field, field):
                    match_field.append(split_field[field])
        else:
            match_field = match_in_matches

        if not match_field:
            return fallback

        if trim_whitespaces:
            reduced_matches = []
            for field_in_match in match_field:
                reduced_matches.append(field_in_match.strip())
            return reduced_matches
        else:
            return match_field

    @staticmethod
    def convert_matches(
        reduced_matches: list[str], kind: Callable[[str], Any], fallback: Any
    ) -> list[Any] | Any:
        """
        Converts the found matching_pattern to the datatype using `kind`

        Parameters
        ----------
        reduced_matches : list[str]
            List of all found matches.
        kind : Callable[[str, Any]]
            converts a string to `kind`
        fallback : Any
            fallback value if conversion fails

        Raises
        ------
        ValueError
            if conversion fails

        Returns
        -------
            list[Any] | Any
            converted list if possible otherwise fallback
        """
        converted_list: list[Any] = []
        for matching_pattern in reduced_matches:
            try:
                converted_list.append(kind(matching_pattern))
            except ValueError:
                converted_list.append(fallback)
        return converted_list
