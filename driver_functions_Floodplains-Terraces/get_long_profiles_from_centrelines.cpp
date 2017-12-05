//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//
// get_long_profiles_from_centrelines
// write csv file of terrace long profiles from centrelines
//
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//
// 05/12/17
// Fiona J. Clubb
// SAFL, University of Minnesota
//
//
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include "../LSDStatsTools.hpp"
#include "../LSDRaster.hpp"
#include "../LSDIndexRaster.hpp"
#include "../LSDFlowInfo.hpp"
#include "../LSDJunctionNetwork.hpp"
#include "../LSDShapeTools.hpp"


int main (int nNumberofArgs,char *argv[])
{
	//Test for correct input arguments
	if (nNumberofArgs!=3)
	{
		cout << "FATAL ERROR: wrong number inputs. The program needs the path name, the driver file name" << endl;
		exit(EXIT_SUCCESS);
	}

	string path_name = argv[1];
	string f_name = argv[2];

	cout << "The path is: " << path_name << " and the filename is: " << f_name << endl;

	string full_name = path_name+f_name;

	ifstream file_info_in;
	file_info_in.open(full_name.c_str());
	if( file_info_in.fail() )
	{
		cout << "\nFATAL ERROR: the header file \"" << full_name
		     << "\" doesn't exist" << endl;
		exit(EXIT_FAILURE);
	}

	string terrace_shapefile;
	string ElevationRaster;
  string DEM_extension = "bil";
	string temp;
	string input_path;

	// read in the parameters
	file_info_in >> temp >> ElevationRaster
							 >> temp >> terrace_shapefile;

	// load the elevation raster
	LSDRaster Elevation((path_name+ElevationRaster), DEM_extension);
	cout << "Got the elevation raster" << endl;


	// now load the centrelines
	cout << "\t loading terrace centrelines" << endl;
	cout << "\t The shapefile is: " << path_name+terrace_shapefile+".shp" << endl;
	vector<PointData> Centrelines = LoadPolyline((path_name+terrace_shapefile+".shp").c_str());

	cout << "N lines = " << Centrelines.size() << endl;

	string output_csv = path_name+terrace_shapefile+"_profiles.csv";
	ofstream output_file;
	output_file.open(output_csv.c_str());
	output_file.precision(8);

	output_file << "TerraceID,X,Y,Elevation"  << endl;

	int id = 0;
	// now write the profiles to csv
	for (int i = 0; i < int(Centrelines.size()); i++)
	{
		vector<double> X = Centrelines[i].X;
		vector<double> Y = Centrelines[i].Y;
		for (int j = 0; j < int(X.size()); j++)
		{
			int row, col;
			Elevation.get_row_and_col_of_a_point( X[j], Y[j], row, col);
			float this_elev = Elevation.get_data_element(row, col);
			output_file << id << "," << X[j] << "," << Y[j] << "," << this_elev << endl;
		}
	}
	output_file.close();
}
