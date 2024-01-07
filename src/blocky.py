"""
Blocky - Lightweight Python template engine.

Copyright (C) 2024 Lubomir Milko
This file is part of blocky <https://github.com/lubomilko/blocky>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path
from typing import Union, Callable

__author__ = "Lubomir Milko"
__copyright__ = "Copyright (C) 2024 Lubomir Milko"
__version__ = "1.0.0"
__license__ = "GPLv3"


class Tag:
    """
    Class representing a generic tag in the template.
    Each tag consists of tag name surrounded by tag begin and end strings.
    Example of a possible tag string with the tag name = *"example"*, tag begin
    string = *"<"* and tag end string = *">"*:
    *<example>*
    Tag name is usually variable, but a default name can be assigned.
    """
    # pylint: disable=used-before-assignment
    # rationale: Probably a bug in Pylint, because it assumes that the first "str" type hint is a variable
    # being used before assignment.
    def __init__(self, name: str = "", begin_str: str = r"<", end_str: str = r">") -> None:
        """
        Tag class constructor.

        Parameters:
            default_name (str, optional): Default tag name. Defaults to "".
            begin_str (str, optional): String defining the beginning of a tag. Defaults to "<".
            end_str (str, optional): String defining the end of a tag. Defaults to ">".
        """
        self.begin = begin_str
        self.end = end_str
        self.name = name

    def str_name(self, tag_name: str = "") -> str:
        """
        Returns complete tag string consisting of provided tag name surrounded by tag begin and
        tag end strings, i.e. "tag_begin"+"tag_name"+"tag_end".

        Args:
            tag_name (str): Name of the tag. If not specified, then default tag name is used. Defaults to "".

        Returns:
            str: Tag string.
        """
        name = tag_name if tag_name else self.name
        return str(f"{self.begin}{name}{self.end}")

    @property
    def str(self) -> str:
        """
        Property method that returns the complete tag string consisting of predefined tag name surrounded by
        tag begin and tag end strings, i.e. "tag_begin"+"tag_name"+"tag_end".

        Returns:
            str: Tag string.
        """
        return str(f"{self.begin}{self.name}{self.end}")


class TagsFormat:
    """
    Class defining the format of tags used in template strings.
    """
    def __init__(
            self, variable: Tag, block_start: Tag, block_end: Tag, block_variation: Tag, char_repeat: Tag,
            std_last_first_start: Tag, std_last_first_end: Tag) -> None:
        self.variable: Tag = variable
        self.block_start: Tag = block_start
        self.block_end: Tag = block_end
        self.block_variation: Tag = block_variation
        self.char_repeat: Tag = char_repeat
        self.std_last_first_start: Tag = std_last_first_start
        self.std_last_first_end: Tag = std_last_first_end


class BlockConfig:
    """
    Block configuration class defining the formatting of blocks within the string template.
    """
    def __init__(self, tags: TagsFormat, tab_size: int = 4) -> None:
        self.tags: TagsFormat = tags
        self.tab_size: int = tab_size


DEFAULT_BLOCK_CONFIG: BlockConfig = BlockConfig(
    TagsFormat(                             # tags
        Tag(),                                  # tags.variable
        Tag(),                                  # tags.block_start
        Tag(begin_str=r"</"),                   # tags.block_end
        Tag(begin_str=r"<^"),                   # tags.block_variation
        Tag(name=r"+"),                         # tags.char_repeat
        Tag(name=r"."),                         # tags.std_last_first_start
        Tag(name=r".", begin_str=r"</")),       # tags.std_last_first_end
    4)                                      # tab_size
"""
Object defining default block configuration.

* Below is the default format of template tags with example tag names using upper-case letters:

    * Variable: ``<VAR_NAME>``
    * Block

        * start: ``<BLOCK_NAME>``
        * end: ``</BLOCK_NAME>``

    * Right-aligned character repeat: ``<+>``
    * Standard/last value definition: ``<.>STD_VALUE<^.>LAST_VALUE</.>``
    * Standard/last/first value definition: ``<.>STD_VALUE<^.>LAST_VALUE<^.>FIRST_VALUE</.>``

* Default tabulator size = 4.
"""


class BlockData(object):
    """
    Class for creating objects containing data to be filled into template blocks defined by
    the :class:`Block` class. The object attributes shall directly correspond to the block and variable tags
    within the block template. The attribute values can then be used to :meth:`fill` the block template.
    The list below defines relationships between :class:`BlockData` object attribute types and their use in
    a block template:

    *   Strings, integers, floats, booleans -> Values set directly as block variables.
    *   :class:`BlockData` subobject -> Data to be filled into a subblock of the parent block being filled.
    *   List -> Content of block clones, each list item represents a content to be used in one cloned instance.

    """
    def __init__(self, data_dict: dict = None, fill_hndl: Callable[["Block", object, int], None] = None) -> None:
        """
        Constructor creating new block object data.

        Args:
            data_dict (dict, optional): Dictionary defining the object attributes to be created using the
                :meth:`import_dict` method. Defaults to None.
            fill_hndl (Callable[[Block, object, int], None], optional): Handler for a special
                function to be called when the data from a corresponding :class:`BlockData` object are filled
                into the block template. The handler can contain special operations to be performed during
                the template filling. Defaults to None.
        """
        self.fill_hndl: Callable[[Block, object, int], None] = fill_hndl
        if data_dict:
            self.import_dict(data_dict)

    def import_dict(self, data_dict: dict) -> None:
        """
        Imports data from dictionary, i.e., converts dictionary key-value pairs into object
        attributes with values. The dictionary keys are directly used as names for new :class:`Block` object
        attributes. The dictionary values are converted according to the following rules:

        *   Strings, integers, floats, booleans -> Directly used as :class:`BlockData` object attribute values.
        *   Subdictionary with its own key-value pairs -> Subdictionary is added as a :class:`BlockData` subobject
            into the parent :class:`BlockData` object with internal attributes set according to the key-value
            pairs of the subdictionary.
        *   List -> Added as a list type :class:`BlockData` object attribute. Only one-dimensional lists are
            supported for filling the template blocks.

        Args:
            data_dict (dict): Dictionary defining the structure of object attributes to be created.
        """
        def get_value(value: any) -> list | BlockData | str:
            val = None
            if isinstance(value, (list, tuple)):
                val = [get_value(v) for v in value]
            elif isinstance(value, dict):
                val = BlockData()
                val.import_dict(value)
            else:
                val = value
            return val

        for (attrib, value) in data_dict.items():
            setattr(self, attrib, get_value(value))


class Block:
    """
    Class representing a block indicated by block start and block end tags inside parent block template.
    """
    def __init__(self, template: str | Path = "", block_name: str = "",
                 config: BlockConfig = DEFAULT_BLOCK_CONFIG, parent: "Block" = None) -> None:
        """
        Constructor. Creates a new block object.

        Args:
            template (str, optional): Template to be used for the :class:`Block` object. Defaults to "".
            block_name (str, optional): Block name. Set automatically to the block tag name from the
                template when the :meth:`get_subblock` method is used.
            config (:class:`BlockConfig`, optional): Block configuration (template tags format, tabulator size, etc.)
            parent: Parent :class:`Block` object.
        """
        # Template with tags to be filled by filling module.
        self.__template: str = ""
        # Content created by filling tags in the template and its clones.
        # Flag indicating that a new clone of the template is going to be automatically added after the
        # actual content as soon as new template variables or blocks are set.
        self.__clone_flag: bool = False
        # Flag indicating that a first value of a special *first-last value* tag should be set.
        self.__set_first_value: bool = True
        self.raw_content: bool = False
        self.content: str = ""
        self.config = config
        # Block name corresponding to the block tag name in the template.
        self.name: str = block_name
        # Parent block and dictionary of child subblocks with block names as keys and block objects as values.
        self.parent: Block = parent
        if parent and block_name:
            parent.subblocks[block_name] = self
        self.subblocks: dict[str, Block] = {}

        # Set template if it is defined in constructor.
        if template:
            self.load_template(template)

    @property
    def template(self) -> str:
        """
        Property method that returns the block template string containing the tags representing subblocks and variables.

        Returns:
            str: Block template.
        """
        return self.__template

    @template.setter
    def template(self, template: str) -> None:
        """
        Setter method that sets a block template string containing the tags representing subblocks and variables.

        Args:
            template (str): Block template string.
        """
        self.__template = template
        self.content = template

    def load_template(self, template: str | Path, subblock_name: str = "") -> None:
        """
        Loads block template from the text file. Alternatively, if the template is provided directly
        as a string (i.e., not the file path), then the string is directly used as a block template.

        Args:
            template (str | Path): Path to the text file containing a string to be used as a block template.
                Alternatively, a raw string can be provided instead of the file path, to be directly used
                as a template.
            subblock_name (str, optional): Name of the subblock to be extracted from the specified template.
                If not specified, then the whole template string will be set as a template. Defaults to an
                empty string "".
        """
        if Path(template).is_file():
            with open(template, "r", encoding="utf-8") as file_template:
                template_str = file_template.read()
            self.name = Path(template).name
        else:
            template_str = template

        if subblock_name:
            blk_file = Block(template=template_str, config=self.config)
            self.template = blk_file.get_subblock(subblock_name).template
            self.name = subblock_name
            del blk_file
        else:
            self.template = template_str

    def save_content(self, content_file_path: str | Path) -> None:
        """
        Saves block content to the text file.

        Args:
            content_file_path (str | Path): Path to the text file in which the block content will be saved.
        """
        with open(content_file_path, "w", encoding="utf-8") as file_content:
            file_content.write(self.content)

    def fill(self, block_data: object, __subidx: int = 0) -> None:
        """
        Fills the block content using the data from specified object. The list below defines relationships
        between :class:`BlockData` object attribute types and their use in a block template:

        *   Strings, integers, floats, booleans -> Values set directly as block variables.
        *   :class:`BlockData` subobject -> Data to be filled into a subblock of the parent block being filled.
        *   List -> Content of block clones, each list item represents a content to be used in one cloned instance.

        Args:
            block_data (object): Object whose attributes will be used to fill the block template. It is
                recommended to use an instance of :class:`BlockData` class or an object inheriting from this
                class.
            __subidx (int, optional): Internal value representing the item index for attributes of list type.
                The index is sent as an argument to the fill handler function (it it's used) to indicate which
                list item is being used for filling the template block. This parameter shall be left at a
                default value 0 when this method is called. Defaults to 0.
        """
        for (attrib, value) in [(a, v) for (a, v) in block_data.__dict__.items() if isinstance(v, list)]:
            subblk = self.get_subblock(f"{attrib.upper()}")
            if subblk:
                if value:
                    for (i, val) in enumerate(value):
                        subblk.fill(val, i)
                        subblk.clone()
                    subblk.set()
                else:
                    subblk.clear()

        for (attrib, value) in [(a, v) for (a, v) in block_data.__dict__.items()
                                if not isinstance(v, (list, str, int, float, bool)) and a != "fill_hndl"]:
            subblk = self.get_subblock(f"{attrib.upper()}")
            if subblk:
                if value:
                    subblk.fill(value)
                    subblk.set()
                else:
                    subblk.clear()

        for (attrib, value) in [(a, v) for (a, v) in block_data.__dict__.items()
                                if isinstance(v, (str, int, float, bool))]:
            self.set_variables(**{f"{attrib.upper()}": value})

        if hasattr(block_data, "fill_hndl"):
            if block_data.fill_hndl:
                block_data.fill_hndl(self, block_data, __subidx)

    def reset(self, all_subblocks: bool = True) -> None:
        """
        Resets block content to the initial template.

        Args:
            all_subblocks (bool, optional): Flag indicating that all subblocks, i.e. child :class:`Block` objects
                are reset together with the parent current block. Defaults to True.
        """
        # Reset block by setting the content to the initial template string.
        self.content = self.__template
        self.__clone_flag = False
        if all_subblocks:
            # Reset all subblocks of the current block and recursively also their subblocks.
            for blk_obj in self.subblocks.values():
                blk_obj.reset()

    def clear(self, count: int = -1) -> None:
        """
        Clears subblock from parent block, i.e. the content of the subblock is erased from the parent content.

        Args:
            count (int, optional): Maximum number of subblocks to be cleared (if there are multiple blocks using
                the same tag names). If set to -1, then all corresponding subblock tags in the parent content will
                be replaced by empty string. Defaults to -1.
        """
        # Set the content to empty string and remove the block from parent's dictionary of subblocks.
        self.content = ""
        self.set(count=count)

    def clone(self, num_copies: int = 1, force: bool = False, passive: bool = False,
              set_subblocks: bool = False) -> None:
        """
        Clones block by adding the template after the actual block content. Then subblocks and variables in
        the added template can be filled again with values.

        .. note::
            This method actually only internaly indicates that there is a need to perform the template cloning
            and only if there is an already previously indicated need, then the actual cloning is performed.

        Args:
            num_copies (int, optional): Number of copies to be created. Defaults to 1.
            force (bool, optional): Switch forcing the cloning to be performed immediately regardless of whether
                it will be actually needed for setting subblocks and variables or not, i.e., new template is
                forcefully added after the block content. If the ``num_copies`` parameter is higher than 1, then
                this switch is always set to False. Defaults to False.
            passive (bool, optional): Switch to perform the cloning only if a need for the clone
                has already been indicated previously, otherwise no new cloning need is indicated. If the
                ``num_copies`` parameter is higher than 1, then this switch is always set to False.
                Defaults to False.
            set_subblocks (bool, optional): Switch to set all subblocks to this parent block first, before
                cloning this block. If the ``num_copies`` parameter is higher than 1, then the subblocks are
                set only once before making the first copy of this parent block. Defaults to False.
        """
        if set_subblocks:
            for blk_obj in self.subblocks.values():
                blk_obj.set()

        if num_copies > 1:
            for _ in range(num_copies):
                self.clone(1, False, False, False)
        else:
            # Check if cloning flag indicates that the cloning shall be actually performed.
            # If cloning is not forced, then the block should be cloned only after it has been filled, which is
            # indicated by the clone_flag.
            if force or self.__clone_flag:
                if not self.raw_content:
                    self.__set_std_last_first_tag(first=self.__set_first_value)
                    self.__set_first_value = False
                    self.__set_char_repeat_tag()
                # Perform a clone, i.e. finalize the content and add new template at the end of the content.
                self.content = f"{self.content}{self.__template}"
                self.__clone_flag = False
            if not passive:
                if not force:
                    self.__clone_flag = True
                # Reset all subblocks of the current block and recursively also their subblocks to have
                # a fresh new instance of all cloned blocks without any remaining unset modified content
                # strings or cloning flags set to True.
                for blk_obj in self.subblocks.values():
                    blk_obj.reset(all_subblocks=True)

    def get_subblock(self, *subblock_names: str) -> Union["Block", list["Block"], None]:
        """
        Returns a subblock object defined by block start and end tags within the actual block template.

        Args:
            subblock_names (str): Name(s) of the subblock tags in the actual block template. The string between
                the subblock tags is used as a template for the returned subblock object.

        Returns:
            :class:`CodeBlock`: Subblock object or a list of subblock objects in case of multiple subblock names
            specified in the input arguments. If the specified subblock is not found, then ``None`` is returned.
        """
        ret_blk = []
        for subblock_name in subblock_names:
            # Init subblock object to None, so if subblock name is not found, then None is returned.
            subblk = None
            # Clone block if the cloning flag is set to true to ensure that the subblock tags can be
            # found in the block content and the subblock content can be extracted from them.
            self.clone(passive=True)
            if subblock_name:
                (subblk_start, subblk_end) = self.__get_subblock_start_end_pos(
                    self.config.tags.block_start.str_name(subblock_name),
                    self.config.tags.block_end.str_name(subblock_name))
                if subblk_start >= 0 and subblk_end >= 0:
                    # If subblock tags are found, then create a new subblock and set correct parent-subblock relations.
                    subblk = Block(self.content[subblk_start: subblk_end], subblock_name, self.config, self)
            ret_blk.append(subblk)
        if ret_blk:
            if len(ret_blk) == 1:
                ret_blk = ret_blk[0]
        else:
            ret_blk = None
        return ret_blk

    def clear_subblock(self, *subblock_names: str) -> None:
        """
        Clears subblock with given name, i.e. the content of the subblock is erased from the parent content.

        .. note::
            Subblock can be cleared only if it has not been :meth:`set` to the parent block yet.

        Args:
            subblock_names (str): Subblock name(s) to be cleared from the current block content.
        """
        for subblock_name in subblock_names:
            if subblock_name in self.subblocks:
                # If subblock is already defined in child subblocks, then clear it directly.
                self.subblocks[subblock_name].clear()
            else:
                # If subblock is not defined yet, then extract it and then call the clear method.
                blk_sub = self.get_subblock(subblock_name)
                if blk_sub:
                    blk_sub.clear()

    def set_subblock(self, *subblocks: "Block") -> None:
        """
        Sets the content of a subblock object into the template of the parent block object from which this method
        is called, i.e. replaces the subblock tags in the parent block template with the subblock content.

        .. note::
            Calling this method is equivalent to the call of the :meth:`set` method from the subblock object.

        Args:
            subblocks (:class:`Block`): Subblock object(s) from which the content will be set into parent block
                object template.
        """
        for subblk in subblocks:
            subblk.set()

    def set(self, variation_idx: int = 0, all_subblocks: bool = False,
            raw_content: bool | None = None, count: int = -1) -> None:
        """
        Sets the content of the block from which this method is called into its parent block template,
        i.e. replaces the subblock tags in the parent block template with the subblock content.

        Args:
            variation_idx (int, optional): Variation of a block content to be set. Variations are
                content parts separated by separator tags. Defaults to 0.
            all_subblocks(bool, optional): Flag indicating that all subsequent child subblocks of current block
                should be set into its parent blocks first before the current block is set into its parent block.
            raw_content (bool | None, optional): Flag indicating that the block content should be set as is without
                any processing, i.e., without setting values for special tags. If set to ``None``, then the
                internal raw content flag for a block is unchanged and it is used to determine if the special tag values
                are set or not. Defaults to None.
            count (int, optional): Maximum number of block contents to be set. If set to -1, then all
                corresponding subblock tags in the parent content will be replaced by the subblock content.
                Defaults to -1.
        """
        if raw_content is not None:
            self.raw_content = raw_content

        if all_subblocks and self.subblocks:
            for blk_obj in self.subblocks.values():
                # pylint: disable=protected-access
                # rationale: Private variable __clone_flag is used primarily internally for cloning operation.
                # However, in this case it can be used to detect if subblock has been already set to parent block
                # or not. if clone flag is True, then the subblock needs to be set.
                if blk_obj.__clone_flag:
                    blk_obj.set(variation_idx, all_subblocks, raw_content)

        if self.parent and self.content != self.__template:
            # If content has been changed from the template, then clone the parent block if
            # its cloning flag is set to true to ensure that the subblock tags can be
            # found in the parent block content and the subblock content can be set into them.
            self.parent.clone(passive=True)
        if not self.raw_content:
            # Finalize the block content by setting value of special tags.
            self.__set_std_last_first_tag(last=True)
            self.__set_first_value = True
            self.__set_char_repeat_tag()
        set_num = 0
        while self.parent and (set_num < count or count < 0):
            # pylint: disable=protected-access
            # rationale: Private method __get_subblock_start_end_pos is called from non-self object only here and
            # it is easier and simpler to keep it that way instead of rewriting the method to be static and sending
            # parent object data into it for processing.
            (subblk_start, subblk_end) = self.parent._Block__get_subblock_start_end_pos(
                self.parent.config.tags.block_start.str_name(self.name),
                self.parent.config.tags.block_end.str_name(self.name),
                True)
            if subblk_start >= 0 and subblk_end >= 0:
                blk_content = self.__get_variation(self.content, self.name, variation_idx)
                # If subblock tags are found, then set the current block content into all corresponding subblock tags
                # in the parent block content.
                self.parent.content = \
                    f"{self.parent.content[: subblk_start]}{blk_content}{self.parent.content[subblk_end:]}"
                # Increment number of blocks being set into the parent block.
                set_num += 1
            else:
                break

    def set_variables(self, *name_value_args: str, autoclone: bool = False, **name_value_kwargs) -> None:
        """
        Sets values into the variables inside the block template, i.e. replaces the tags representing
        variables with the specified values.
        Only positional or only keyword arguments described below or both at the same time can be used
        to define the variables and their values.

        Args:
            name_value_args (str): Positional arguments representing variable *name*-*value* pairs. The
                following example illustrates setting the ``var1`` variable to value ``1`` and the ``var2``
                variable to value ``2``.

                .. code-block::

                    some_block.set_variables("var1", "1", "var2", "2")

                .. important::
                    Positional arguments ``name_value_args`` are supported only for backward compatibility
                    purposes. Usage of keyword arguments ``name_value_kwargs`` instead of positional arguments
                    is strongly recommended.

            autoclone (bool, optional): Flag indicating that the block containing the variable tags
                being set should be automatically cloned after the variable is set to its value.
            name_value_kwargs : Keyword arguments representing variable *name*-*value* pairs, e.g.:

                .. code-block::

                    some_block.set_variables(var1="1", var2="2")

        .. note::
            Non-string variable value types are allowed, if they have a string representation, i.e. they
            can be automatically converted to the string. Following example shows setting variable ``var`` to
            value ``1`` by specifying the value as an integer number:

            .. code-block::

                some_block.set_variables(var=1)
        """
        # If this method is called with the first positional argument set to something else than a string,
        # then assume that it is a boolean flag for the autoclone argument, e.g.: set_variables(True, VARIABLE=value).
        # Set the non-string argument into the the autoclone argument and increment the start index of the usable
        # positional arguments.
        pos_arg_start_idx = 0
        if name_value_args:
            if not isinstance(name_value_args[0], str):
                autoclone = bool(name_value_args[0])
                pos_arg_start_idx = 1

        var_tags = []
        var_values = []
        # Loop through variable name-value positional and keyword arguments and extract the variable tags
        # and corresponding values.
        for var_idx in range(pos_arg_start_idx, len(name_value_args), 2):
            if var_idx + 1 < len(name_value_args):
                var_tags.append(self.config.tags.variable.str_name(name_value_args[var_idx]))
                var_values.append(name_value_args[var_idx + 1])
        for var_name, var_value in name_value_kwargs.items():
            var_tags.append(self.config.tags.variable.str_name(f"{var_name}"))
            var_values.append(var_value)

        iter_idx = 0
        detected_iters_num = 1
        while iter_idx < detected_iters_num:
            # Clone block if the cloning flag is set to true to ensure that the variable tags can be
            # found in the block content and the variable values can be set into them.
            self.clone(passive=True)
            # Loop through variable tags and replace them with the corresponding variable values.
            for var_idx, var_tag in enumerate(var_tags):
                if isinstance(var_values[var_idx], str):
                    var_value = var_values[var_idx]
                else:
                    try:
                        _ = iter(var_values[var_idx])
                        if len(var_values[var_idx]) > detected_iters_num:
                            detected_iters_num = len(var_values[var_idx])
                        if len(var_values[var_idx]) > iter_idx:
                            var_value = var_values[var_idx][iter_idx]
                        else:
                            var_value = var_values[var_idx][-1]
                    except TypeError:
                        var_value = var_values[var_idx]
                self.content = self.content.replace(var_tag, f"{var_value}")
            iter_idx += 1
            if detected_iters_num > 1 or autoclone:
                self.clone()

    def clear_variables(self, *var_names: str) -> None:
        """
        Removes specified variables from the block template, i.e. replaces the tags representing variables with
        the empty strings.

        Args:
            var_names (str): Arguments with variable names to be cleared.
        """
        for var_name in var_names:
            self.content = self.content.replace(self.config.tags.variable.str_name(var_name), "")

    def __get_subblock_start_end_pos(self, start_tag: str, end_tag: str, include_tags: bool = False) -> tuple[int, int]:
        """
        Returns start and end position of a subblock string in the block content.

        Args:
            start_tag (str): Subblock start tag string.
            end_tag (str): Subblock end tag string.
            include_tags (bool, optional): If true, then start-end position takes into account also
                the subblock tags themselves. Defaults to False.

        Returns:
            tuple[int, int]: Returned start and end character position of the subblock, i.e. ``(start_pos, end_pos)``.
        """
        subblk_start = self.content.find(start_tag)
        if subblk_start >= 0:
            if not include_tags:
                subblk_start += len(start_tag)
                # Return "\n" char pos + 1 if "\n" is found, else return -1 + 1 = 0
                next_nl = self.content.find("\n", subblk_start) + 1
                if next_nl > 0 and not self.content[subblk_start: next_nl].strip():
                    subblk_start = next_nl
            else:
                prev_nl = self.content.rfind("\n", 0, subblk_start) + 1
                next_nl = self.content.find("\n", subblk_start)
                if next_nl > 0 and self.content[prev_nl: next_nl].strip() == start_tag:
                    subblk_start = prev_nl

        subblk_end = self.content.find(end_tag)
        if subblk_start >= 0 and subblk_end >= 0:
            if not include_tags:
                last_nl = self.content.rfind("\n", subblk_start, subblk_end) + 1
                if last_nl > 0 and not self.content[last_nl: subblk_end].strip():
                    subblk_end = last_nl
            else:
                prev_nl = self.content.rfind("\n", 0, subblk_end)
                subblk_end += len(end_tag)
                next_nl = self.content.find("\n", subblk_end) + 1
                if next_nl > 0 and self.content[prev_nl: next_nl].strip() == end_tag:
                    subblk_end = next_nl

        return (subblk_start, subblk_end)

    def __set_char_repeat_tag(self) -> None:
        """
        Replaces special tags representing repeated characters in the block content with the correct amount of
        repeated characters (usually spaces or tabulators) to keep predefined right-alignement.
        """
        last_pos = 0
        # Loop through all *char repeat* tags in block template and replace them with the correct
        # number of repeated characters.
        while True:
            # Get data about char repeat in the block content.
            (cont_start, cont_end, new_col, repeat_char) = self.__get_char_repeat_data(self.content)
            if cont_start >= 0:
                # Get data about char repeat in the block template, i.e. the content before it has been filled.
                (templ_start, templ_end, orig_col, _) = self.__get_char_repeat_data(
                    self.__template, True, last_pos)
                orig_len = templ_end - templ_start
                # Calculate new length of repeated characters in the filled content.
                new_len = orig_len + (orig_col - new_col)
                if repeat_char == "\t":
                    temp_len = new_len
                    new_len //= self.config.tab_size
                    if new_len * self.config.tab_size < temp_len:
                        new_len += 1
                if new_len <= 0:
                    new_len = 1
                # Set repeated characters into the block content instead of the *char repeat* tag.
                self.content = f"{self.content[0: cont_start]}{new_len * repeat_char}{self.content[cont_end:]}"
                # Remember last *char repeat* tag position in the template, because if there are more of these tags,
                # then we need to start searching only after the previous tag position, not again from the start.
                last_pos = templ_end
            else:
                break

    def __get_char_repeat_data(self, input_string: str, expand_tabs: bool = False, start_index: int = 0) \
            -> tuple[int, int, int, str]:
        """
        Returns data about special *char repeat* tag, i.e. its start, end position, column index in line and
        the character to be repeated.

        Args:
            input_string (str): String in which the special tag is searched.
            expand_tabs (bool, optional): If true, then tabulators are replaced with spaces for consistent
                character position counting. Defaults to False.
            start_index (int, optional): Start character index from which the special tag is searched.
                Defaults to 0.

        Returns:
            tuple[int, int, int, str]: *char repeat* tag data in form of a following tuple:
                ``(start_pos, end_pos, column_pos, repeated_char)``.
        """
        if expand_tabs:
            input_string = input_string.expandtabs(self.config.tab_size)
        end_pos = -1
        tag_col_pos = -1
        repeat_char = None
        # Get starting position of repeated characters.
        start_pos = input_string.find(self.config.tags.char_repeat.str, start_index)
        if start_pos >= 0:
            end_pos = start_pos + len(self.config.tags.char_repeat.str)
            # Get character immediately following the *char repeat* tag. This character is going to be repeated.
            repeat_char = input_string[end_pos]
            # Get ending position of repeated characters.
            while input_string[end_pos] == repeat_char:
                end_pos += 1
            # Get position of the line start in which the *char repeat* tag is located.
            line_start_pos = input_string.rfind("\n", 0, start_pos)
            line_start_pos = 0 if line_start_pos < 0 or line_start_pos > start_pos else line_start_pos + 1
            # Get column position of *char repeat* tag, i.e. the position of the *char repeat* tag within its line.
            tag_col_pos = len(input_string[line_start_pos: start_pos].expandtabs(self.config.tab_size))
        return (start_pos, end_pos, tag_col_pos, repeat_char)

    def __set_std_last_first_tag(self, first: bool = False, last: bool = False) -> None:
        """
        Replaces special *last value* tag in the block content with either the standard value or the last value.

        Args:
            first (bool, optional):  Switch to set the *first* value in place of the *std last first* tag. If False,
                then the standard value is used. Defaults to False.
            last (bool, optional): Switch to set the *last* value in place of the *std last first* tag. If False,
                then the standard value is used. This switch has a priority over the ``first`` switch argument.
                Defaults to False.
        """
        # Loop through all *last value* tags in block content and replace them with either standard value or last value.
        while True:
            # Get the start and end position of the *last value* tag including the start/end tags.
            (subblk_start, subblk_end) = \
                self.__get_subblock_start_end_pos(
                    self.config.tags.std_last_first_start.str,
                    self.config.tags.std_last_first_end.str,
                    True)
            # If *last value* tag is found.
            if subblk_start >= 0 and subblk_end >= 0:
                # Extract the content of the *last value* tag without the start/end tags themselves.
                (subblk_cont_start, subblk_cont_end) = \
                    self.__get_subblock_start_end_pos(
                        self.config.tags.std_last_first_start.str,
                        self.config.tags.std_last_first_end.str)
                value_content = self.content[subblk_cont_start: subblk_cont_end]
                value_content = self.__get_variation(
                    value_content, self.config.tags.std_last_first_start.name, 1 if last else 2 if first else 0)
                self.content = f"{self.content[: subblk_start]}{value_content}{self.content[subblk_end:]}"
            else:
                break

    def __get_variation(self, content: str, block_name: str, variation_idx: int) -> str:
        """
        Returns a block content string corresponding to the specified variation of a block content from
        all variations defined using special *block variation* tags.

        Args:
            content (str): Content string with multiple variations formatted using *block variation* tags.
            block_name (str): Block name that is used in *block variation* tags.
            variation_idx (int): Index of a variation (starting from 0) to be returned by this method.

        Returns:
            str: Block content string variation corresponding to the specified variation index.
        """
        var = content
        if self.config.tags.block_variation.str_name(block_name) in content:
            var_list = content.split(self.config.tags.block_variation.str_name(block_name))
            if variation_idx < len(var_list):
                var = var_list[variation_idx]
            else:
                var = var_list[0]
            # Remove initial empty space up to the first new line char "\n", including the "\n" if present.
            first_nl = var.find("\n") + 1
            if first_nl > 0 and var[: first_nl].strip() == "":
                var = var[first_nl:]
            # Remove trailing empty space after the final new line char "\n", not including the final "\n" if present).
            last_nl = var.rfind("\n") + 1
            if last_nl > 0 and var[last_nl:].strip() == "":
                var = var[0: last_nl]

        return var
