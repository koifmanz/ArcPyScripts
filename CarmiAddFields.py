import arcpy


pipes_lyr = arcpy.GetParameterAsText(0)  # line feature class
split_method = arcpy.GetParameterAsText(1)  # string
label_field = arcpy.GetParameterAsText(2) # field  for labeling and status, from pipes_lyr
Q_Rate = arcpy.GetParameterAsText(3) # Discharge field field from pipes_lyr


def Split_Style(way):
    """becuase they are little children, choose way to split, based on the user
    prefrence. if the way not in dict use carmi style.

    Parameters
    ----------
    way : string
         The Key for looking in the dict.
    """
    ways_dict = {"Space": " ", "Underline": "_"}
    return ways_dict.get(way, " ")


arcpy.AddMessage("You choose to split using {0}".format(split_method))
split_method = Split_Style(split_method)

# Add new fields
fields_list = ["Status", "Direction", "D_Label"]  # list of new fields
message = "Starting - adding new fields"
arcpy.SetProgressor("step", message)
for fld in fields_list:
    arcpy.AddField_management(pipes_lyr, fld, "TEXT")


def Get_Status(n, way):
    """Return True for new rows based on length.
    if the word new in text, return 1

    Parameters
    ----------
    n : field
        field which include NOTES field.
    """
    s = n.split(way)
    if len(s) > 1:
        return "1"
    else:
        return "0"


def Get_direction(n):
    """Return the direction of the line, for symbology, based on Q.

    Parameters
    ----------
    n : field
        field which include q data`.
    """
    if abs(n) == 0:
        return 0
    else:
        return n / abs(n)


data_fields = [label_field, Q_Rate] + fields_list
arcpy.SetProgressorPosition(25)
# main loop
with arcpy.da.UpdateCursor(pipes_lyr, data_fields) as cursor:
    for row in cursor:
        arcpy.SetProgressorLabel("Getting Status")
        row[2] = Get_Status(row[0], split_method)
        arcpy.SetProgressorLabel("Getting Direction")
        row[3] = Get_direction(row[1])
        arcpy.SetProgressorLabel("Getting Label")
        row[4] = row[0].split(split_method)[0]
        cursor.updateRow(row)
        arcpy.SetProgressorPosition()

arcpy.ResetProgressor()
