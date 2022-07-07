'''
@Creator = Andrew Sauerwin

This library will provide a set of different geoprocessing functions to be leveraged in any workflow.
Be sure to import the appropriate modules when using the following code.
'''
#
# Imports will vary but in general, these are required for the following functions below.
#
import arcpy, os
from arcpy import env

def update_Values(inputs):
'''This function reads the record of feature class in geodatabase then changes the record of the field(s)
 to a value of your choice. Valid work space environments will include standalone feature classes in a geodatabase,
 not those inside of datasets, though the code could easily be updated to find them.'''
   
	for i in inputs:
		print("Workspace set to: {0}".format(i))
		workspace = arcpy.env.workspace = inputs

		# Start an edit session. Must provide the workspace.
		edit = arcpy.da.Editor(workspace)
		
		# Edit session 
		edit.startEditing(False, False)
		
		# Starting edit operation
		edit.startOperation()

		print("Working on records in: {0}".format(i))
		featureclasses = arcpy.ListFeatureClasses()
		
		# Grabbing feature classes to work on
		print("Starting to reset the: {0}".format(i))
		for fc in featureclasses:
			# Setting Spatial Reference (No longer needed but will leave for future enhancements)
			spatial_ref = arcpy.Describe(fc).spatialReference
			print("{0}".format(fc))
						
			try:
				with arcpy.da.SearchCursor(fc, ["<Field of your choice>"]) as search_cursor:
					for s_row in search_cursor:
						print("\tExisting Record: {0}".format(s_row))
				with arcpy.da.UpdateCursor(fc, ["<Field of your choice>"]) as update_cursor:
					for a_row in update_cursor:
						# Update record with value below
						a_row[0] = str('<Value based on field type, in this instance this was a Text Field>')
						# Records get updated here
						update_cursor.updateRow(a_row)
				# This is not necessairly needed, but can be used to validate changes if ran against the same table.
				with arcpy.da.SearchCursor(fc, ["<Field of your choice>"]) as search_cursor:
					for s_row in search_cursor:
						print("\tChanged Record: {0}".format(s_row))
			except Exception as error_e:
				print("Error processing cursor: {0}".format(error_e))
		
		# Stop the edit operation.
		edit.stopOperation()

		# Stop the edit session and save the changes
		edit.stopEditing(True)
		
		# Function process complete
		print("Reset complete.")
	return
			
# Variable for setting the database
var_X = r""

# List to pass into the function can take one or more values. If more than one workspace needs updated,
# add another variable to have the function work on.
inputs = [""]
