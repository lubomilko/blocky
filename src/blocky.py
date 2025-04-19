"""
Blocky - Lightweight Python template engine.

Copyright (C) 2025 Lubomir Milko
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
from collections.abc import Callable
from dataclasses import dataclass
from typing import Union

__author__ = "Lubomir Milko"
__copyright__ = "Copyright (C) 2025 Lubomir Milko"
__version__ = "2.0.0"
__license__ = "GPLv3"


@dataclass
class BlockConfig:
    """The template block configuration defining the format of tags and other template elements."""
    tag_gen_var: Callable[[str], str] = lambda name: f"<{name.upper()}>"
    tag_gen_blk_start: Callable[[str], str] = lambda name: f"<{name.upper()}>"
    tag_gen_blk_end: Callable[[str], str] = lambda name: f"</{name.upper()}>"
    tag_gen_blk_vari: Callable[[str], str] = lambda name: f"<^{name.upper()}>"
    tag_name_charrep: str = "+"
    tag_name_stdlastfirst: str = "."
    tab_size: int = 4


class Block:
    """Block corresponding to the part of the template within the block start and end tags."""
    def __init__(self, template: str | Path = "", block_name: str = "",
                 config: BlockConfig = BlockConfig(), parent: "Block" = None) -> None:
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
        if Path(template).is_file():
            self.load_template(template)
        else:
            self.template = template

    @property
    def template(self) -> str:
        return self.__template

    @template.setter
    def template(self, template: str) -> None:
        self.__template = template
        self.content = template

    def load_template(self, file_path: str | Path) -> None:
        """Loads the block template from a text file."""
        with open(file_path, "r", encoding="utf-8") as file_template:
            self.template = file_template.read()
            self.name = Path(file_path).name

    def save_content(self, file_path: str | Path) -> None:
        """Saves the block content to a text file."""
        with open(file_path, "w", encoding="utf-8") as file_content:
            file_content.write(self.content)

    def fill(self, block_data: object | dict, __subidx: int = 0) -> int | bool:
        """
        Fills the block content using the data from a specified object (:class:`BlockData` recommended) or a
        dictionary. The list below defines the relationships between the object attribute values or dictionary
        values and their use in a block template:

        *   Strings, integers, floats, booleans -> Values set directly as block variables into the template tags.
        *   Subobject or subdictionary -> Data to be filled into a subblock of the parent block being filled.
        *   List or tuple -> Content of block clones. Each list or tuple item should consist of another subobject or
            a subdictionary representing attributes and their values to be used in one cloned instance of
            a template block.

        Args:
            block_data (object | dict): Object or dictionary with the attribute-value or key-value pairs to be
                used for filling the block template. The following two special attributes can be defined:

                *   ``fill_hndl``: A function called before the parent template block containing this
                    attribute is set into the template. Useful for custom low-level modifications of the
                    template block.
                *   ``vari_idx``: A *variation index* specifying the variation of the parent template block
                    containing this attribute to be set into the template. Only valid for blocks having
                    multiple variations (see the ``variation_idx`` attribute of the :meth:``set`` method).

            __subidx (int, optional): Internal value representing the item index for attributes of list type.
                The index is sent as an argument to the fill handler function (it it's used) to indicate which
                list item is being used for filling the template block. This parameter shall be left at a
                default value 0 when this method is called. Defaults to 0.

        Returns:
            int | bool: Iteration index to be used for setting the parent block containing the elements
                being filled within the current call of this method.
        """
        # Do nothing if block_data is not a dictionary or an object.
        if block_data is None or isinstance(block_data, (list, tuple, str, int, float, bool)):
            return 0

        # Returned variation index used for setting the parent block after the execution of this method.
        ret_vari_idx = 0

        # Get the block data in form of a dictionary even if it is defined as an object.
        data_dict = block_data if isinstance(block_data, dict) else block_data.__dict__

        # 1. Loop through list or tuple items of block data and fill the template blocks that need to be cloned.
        for (attrib, value) in data_dict.items():
            if isinstance(value, (list, tuple)):
                while True:
                    subblk = self.get_subblock(f"{attrib.upper()}")
                    if subblk is None:
                        break
                    if value:
                        for (i, val) in enumerate(value):
                            subblk.fill(val, i)
                            subblk.clone()
                        subblk.set(count=1)
                    else:
                        subblk.clear(count=1)   # Value is an empty list, i.e., [].

        # 2. Loop through other types (None, object or dict) of block data and fill the single instance (non-cloned)
        #    template blocks.
        for (attrib, value) in data_dict.items():
            if not isinstance(value, (list, tuple, str, int, float, bool)) and attrib != "fill_hndl":
                while True:
                    subblk = self.get_subblock(f"{attrib.upper()}")
                    if subblk is None:
                        # If value is a None object or an empty dict, i.e., None or {} and there is no
                        # template block with the specified name, then try to clear the variables with that name.
                        if not value:
                            self.clear_variables(f"{attrib.upper()}")
                        break
                    if value:
                        # Get the variation index from the internal elements if they contain a vari_idx attribute.
                        vari_idx = subblk.fill(value)
                        subblk.set(variation_idx=vari_idx, count=1)
                    else:
                        subblk.clear(count=1)   # Value is a None object or an empty dict, i.e., None or {}.

        # 3. Loop through simple data type items of block data and fill the template tags.
        for (attrib, value) in data_dict.items():
            if isinstance(value, (str, int, float, bool)):
                if attrib == "vari_idx":
                    # If the attribute is vari_idx, then return its value to be used as a variation_idx
                    # argument of the set method setting the parent block containing this attribute.
                    ret_vari_idx = value
                else:
                    while True:
                        subblk = self.get_subblock(f"{attrib.upper()}")
                        if subblk is None:
                            break
                        if value:
                            subblk.set(count=1)
                        else:
                            subblk.clear(count=1)   # Value is "", 0 or False
                    self.set_variables(**{f"{attrib.upper()}": value})

        # 4. If an external fill handle is defined within the block data, then call it.
        fill_hndl = data_dict.get("fill_hndl")
        if fill_hndl:
            fill_hndl(self, block_data, __subidx)

        return ret_vari_idx

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
                (subblk_start, subblk_end) = self.__get_subblock_pos(subblock_name)
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

    def set_subblock(self, *subblocks: "Block | str") -> None:
        """
        Sets the content of a subblock object into the template of the parent block object from which this method
        is called, i.e. replaces the subblock tags in the parent block template with the subblock content.

        .. note::
            Calling this method is equivalent to the call of the :meth:`set` method from the subblock object.

        Args:
            subblocks (:class:`Block` | str): Subblock object(s) or names whose content will be set into the
                parent block object template.
        """
        for subblk in subblocks:
            if isinstance(subblk, str):
                if subblk in self.subblocks:
                    # If subblock is already defined in child subblocks, then set it directly.
                    self.subblocks[subblk].set()
                else:
                    # If subblock is not defined yet, then extract it and then call the set method.
                    blk_sub = self.get_subblock(subblk)
                    if blk_sub:
                        blk_sub.set()
            else:
                subblk.set()

    def set(self, variation_idx: int | bool = 0, all_subblocks: bool = False,
            raw_content: bool | None = None, count: int = -1) -> None:
        """
        Sets the content of the block from which this method is called into its parent block template,
        i.e. replaces the subblock tags in the parent block template with the subblock content.

        Args:
            variation_idx (int | bool, optional): Variation index of a block content to be set starting from 0.
                Variations are content parts separated by the separator tags. Negative variation number causes
                the block to be cleared instead of set. A boolean value True represents the first block variation 0
                and False represents the block variation -1, i.e., it clears the block. Defaults to 0.
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
        # Convert potentially boolean variation index to integer.
        if isinstance(variation_idx, bool):
            variation_idx = 0 if variation_idx else -1

        # If variation index is below zero, then clear the block and exit.
        if variation_idx < 0:
            self.clear(count=count)
            return

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
            # rationale: Private method __get_subblock_pos is called from non-self object only here and
            # it is easier and simpler to keep it that way instead of rewriting the method to be static and sending
            # parent object data into it for processing.
            (subblk_start, subblk_end) = self.parent._Block__get_subblock_pos(self.name, True)
            if 0 <= subblk_start < subblk_end:
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
                var_tags.append(self.config.tag_gen_var(name_value_args[var_idx]))
                var_values.append(name_value_args[var_idx + 1])
        for var_name, var_value in name_value_kwargs.items():
            var_tags.append(self.config.tag_gen_var(f"{var_name}"))
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
            self.content = self.content.replace(self.config.tag_gen_var(var_name), "")

    def __get_subblock_pos(self, tag_name: str, include_tags: bool = False) -> tuple[int, int]:
        """Returns start and end position of a subblock string in the block content.

        Args:
            tag_name (str): Subblock tag name.
            include_tags (bool, optional): If true, then start-end position takes into account also
                the subblock tag characters themselves. Defaults to False.

        Returns:
            tuple[int, int]: Start and end character position of the subblock, i.e. ``(start_pos, end_pos)``.
        """
        start_tag = self.config.tag_gen_blk_start(tag_name)
        end_tag = self.config.tag_gen_blk_end(tag_name)
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
        charrep_tag = self.config.tag_gen_var(self.config.tag_name_charrep)
        # Get starting position of repeated characters.
        start_pos = input_string.find(charrep_tag, start_index)
        if start_pos >= 0:
            end_pos = start_pos + len(charrep_tag)
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
            (subblk_start, subblk_end) = self.__get_subblock_pos(self.config.tag_name_stdlastfirst, True)
            # If *last value* tag is found.
            if 0 <= subblk_start < subblk_end:
                # Extract the content of the *last value* tag without the start/end tags themselves.
                (subblk_cont_start, subblk_cont_end) = self.__get_subblock_pos(self.config.tag_name_stdlastfirst)
                value_content = self.content[subblk_cont_start: subblk_cont_end]
                value_content = self.__get_variation(
                    value_content, self.config.tag_name_stdlastfirst, 1 if last else 2 if first else 0)
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
        if self.config.tag_gen_blk_vari(block_name) in content:
            var_list = content.split(self.config.tag_gen_blk_vari(block_name))
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
