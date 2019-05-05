import arcpy


InFeatureClass = arcpy.GetParameterAsText(0)  # layer
PressureField = arcpy.GetParameterAsText(1)  # field
ReClassPressureField = arcpy.GetParameterAsText(2)  # str

arcpy.AddField_management(InFeatureClass, ReClassPressureField, "TEXT")

fields = [PressureField, ReClassPressureField]
with arcpy.da.UpdateCursor(InFeatureClass, [fields]) as cursor:
    for row in cursor:
        if row[0] == 25:
            row[1] = "Low"
        elif row[0] >= 25 and row[0] < 30:
            row[1] = "Normal Low"
        elif row[0] >= 30 and row[0] < 50:
            row[1] = "Normal"
        elif row[0] >= 50 and row[0] < 60:
            row[1] = "Normal High"
        elif row[0] >= 60:
            row[1] = "High"
        else:
            row[1] = "NA"
        cursor.updateRow(row)
