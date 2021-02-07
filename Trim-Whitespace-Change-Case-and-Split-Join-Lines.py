# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

bl_info = {
    "name": "Trim Whitespace, Change Case and Split/Join Lines",
    "author": "Tintwotin",
    "version": (0, 2, 1),
    "blender": (2, 80, 0),
    "location": "Text Editor Format Menu",
    "description": "Adds Trim Whitespace, Change Case and Split/Join Lines functions to the Text Editor",
    "warning": "",
    "wiki_url": "",
    "category": "Text Editor"}


import bpy
import re
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    EnumProperty,
)

class TEXT_OT_trim_whitespaces(Operator):
    '''Trims whitespaces'''
    bl_idname = "text.trim_whitespace"
    bl_label = "Trim Whitespace"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Trim Whitespaces",
        description="Trim whitespaces",
        options={'ENUM_FLAG'},
        items=(
             ('TRAILING', "Trailing", "Trim trailing whitespaces"),
             ('BOTH', "Leading & Trailing", "Trim leading and trailing whitespaces"),
             ('LEADING', "Leading", "Trim leading whitespaces"),
             ),
             default={'TRAILING'},
        )

    @classmethod
    def poll(cls, context):
        return (context.area.type == 'TEXT_EDITOR' and context.space_data.text)

    def execute(self, context):
        st = context.space_data
        text = st.text.as_string()
        name = st.text.name
        old_line = bpy.context.space_data.text.current_line_index
        trimmed = ""
        instance = 0
        lines = str(text).splitlines()

        for i in range(len(lines)):
            if self.type == {'TRAILING'}:
                trimmed += lines[i].rstrip()+"\n"
                if len(lines[i].rstrip()) < int(len(lines[i])):
                    instance += 1
            elif self.type == {'LEADING'}:
                trimmed += lines[i].lstrip()+"\n"
                if len(lines[i].lstrip()) < int(len(lines[i])):
                    instance += 1
            elif self.type == {'BOTH'}:
                trimmed += lines[i].strip()+"\n"
                if len(lines[i].strip()) < int(len(lines[i])):
                    instance += 1

        st.text.from_string(trimmed)
        st.text.current_line_index = old_line

        msg = "Trimmed "+str(instance)+" line(s) containing whitespace."
        self.report({'INFO'}, msg)

        return {'FINISHED'}


class TEXT_OT_convert_case(Operator):
    '''Convert case of selection'''
    bl_idname = "text.convert_case"
    bl_label = "Convert Case to"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Convert Case Data",
        description="Which case to convert to",
        options={'ENUM_FLAG'},
        items=(
             ('UPPERCASE', "UPPER CASE", "Convert to upper case"),
             ('LOWERCASE', "lower case", "Convert to lower case"),
             ('TITELCASE', "Titel Case", "Convert to titel case"),
             ('CAPITALIZE', "Capitalize case", "Convert to capitalize"),
             ('SNAKECASE', "snake_case", "Convert to snake case"),
             ('CAMELCASE', "CamelCase", "Convert to camel case"),
              ),
              default={'UPPERCASE'},
        )

    @classmethod
    def poll(cls, context):
        return (context.area.type == 'TEXT_EDITOR' and context.space_data.text)

    def execute(self, context):
        st = context.space_data
        s = get_selected_text(st.text)
        text = bpy.ops.text

        if not s or (len(s) == 0):
            return {'CANCELLED'}

        if self.type == {'UPPERCASE'}:
            text.insert(text=s.upper())
        if self.type == {'LOWERCASE'}:
            text.insert(text=s.lower())
        if self.type == {'TITELCASE'}:
            text.insert(text=s.title())
        if self.type == {'CAPITALIZE'}:
            s1 = re.sub(r"(\A\w)|"+"(?<!\.\w)([\.?!] )\w|"+"\w(?:\.\w)|"+"(?<=\w\.)\w", lambda x: x.group().upper(), s)
            text.insert(text=s1.capitalize())
        if self.type == {'SNAKECASE'}:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
            text.insert(text=re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace(" ", "_"))
        if self.type == {'CAMELCASE'}:
            s = s.lower().replace("_", " ")
            s1 = ''
            s1 += s[0].upper()
            for i in range(1, len(s) - 1):
                if (s[i] == ' '):
                    s1 += s[i + 1].upper()
                    i += 1
                elif(s[i - 1] != ' '):
                    s1 += s[i]
            text.insert(text=s1)
        return {'FINISHED'}


class TEXT_OT_split_join_lines(Operator):
    '''Line Operations'''
    bl_idname = "text.split_join_lines"
    bl_label = "Line Operations"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Line Operations",
        description="Which line operation to do",
        options={'ENUM_FLAG'},
        items=(
             ('SPLIT', "Spilt line(s)", "Split line(s)"),
             ('JOIN', "Join line(s)", "Join line(s)"),
              ),
              default={'SPLIT'},
        )

    @classmethod
    def poll(cls, context):
        return (context.area.type == 'TEXT_EDITOR' and context.space_data.text)

    def execute(self, context):
        st = context.space_data
        s = get_selected_text(st.text)

        if not s or (len(s) == 0):
            return {'CANCELLED'}

        if self.type == {'SPLIT'}:
            bpy.ops.text.insert(text=s.replace(" ", "\n"))

        elif self.type == {'JOIN'}:
            bpy.ops.text.insert(text=''.join([line.strip() for line in s]))

        return {'FINISHED'}


def get_selected_text(text):
    """"""
    current_line = text.current_line
    select_end_line = text.select_end_line

    current_character = text.current_character
    select_end_character = text.select_end_character

    # if there is no selected text return None
    if current_line == select_end_line:
        if current_character == select_end_character:
            return None
        else:
            return current_line.body[min(current_character, select_end_character):max(current_character, select_end_character)]

    text_return = None
    writing = False
    normal_order = True  # selection from top to bottom

    for line in text.lines:
        if not writing:
            if line == current_line:
                text_return = current_line.body[current_character:] + "\n"
                writing = True
                continue
            elif line == select_end_line:
                text_return = select_end_line.body[select_end_character:] + "\n"
                writing = True
                normal_order = False
                continue
        else:
            if normal_order:
                if line == select_end_line:
                    text_return += select_end_line.body[:select_end_character]
                    break
                else:
                    text_return += line.body + "\n"
                    continue
            else:
                if line == current_line:
                    text_return += current_line.body[:current_character]
                    break
                else:
                    text_return += line.body + "\n"
                    continue

    return text_return


def menu_trim_whitespaces(self, context):
    self.layout.operator_menu_enum("text.trim_whitespace", "type")


def menu_convert_case(self, context):
    self.layout.separator()
    self.layout.operator_menu_enum("text.convert_case", "type")


def menu_split_join_lines(self, context):
    self.layout.operator_menu_enum("text.split_join_lines", "type")


def register():
    bpy.utils.register_class(TEXT_OT_trim_whitespaces)
    bpy.utils.register_class(TEXT_OT_convert_case)
    bpy.utils.register_class(TEXT_OT_split_join_lines)
    bpy.types.TEXT_MT_format.append(menu_trim_whitespaces)
    bpy.types.TEXT_MT_format.append(menu_convert_case)
    bpy.types.TEXT_MT_format.append(menu_split_join_lines)


def unregister():
    bpy.utils.unregister_class(TEXT_OT_trim_whitespaces)
    bpy.utils.unregister_class(TEXT_OT_convert_case)
    bpy.utils.unregister_class(TEXT_OT_split_join_lines)
    bpy.types.TEXT_MT_format.remove(menu_trim_whitespaces)
    bpy.types.TEXT_MT_format.remove(menu_convert_case)
    bpy.types.TEXT_MT_format.remove(menu_split_join_lines)

if __name__ == "__main__":
    register()

#unregister()
