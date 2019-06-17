"""
UBC Eye Movement Data Analysis Toolkit (EMDAT), Version 3
Created on 2012-08-23

Sample code to run EMDAT for a given experiment (multiprocessing version).

@author: Sebastien Lalle (creator), Samad Kardan
Institution: The University of British Columbia.
"""

from multiprocessing import freeze_support, cpu_count
from BasicParticipant_multiprocessing import *
from EMDAT_core.Participant import export_features_all, write_features_tsv
from EMDAT_core.ValidityProcessing import output_Validity_info_Segments, output_percent_discarded, output_Validity_info_Participants

if __name__ == '__main__':
    freeze_support() #for windows
    ul =        [200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 217, 218, 219, 220, 221, 223, 224, 225, 226, 227, 228, 229, 231, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 256, 257]    # list of user recordings (files extracted for one participant from Tobii studio)
    #ul =        [84]    # list of user recordings (files extracted for one participant from Tobii studio)
    uids =      ul    # User ID that is used in the external logs (can be different from above but there should be a 1-1 mapping)

    alogoffset = ul    # the time sifference between the eye tracker logs and the external log

    
    ###### Read participants
    nbprocess = cpu_count()
    ps = read_participants_Basic_multiprocessing(nbprocess, user_list = ul,pids = uids, log_time_offsets = alogoffset, datadir=params.EYELOGDATAFOLDER, 
                               prune_length = None, 
    #                           aoifile = "./sampledata/general.aoi",
    #                           aoifile = "./sampledata/Dynamic_1.aoi",
                               require_valid_segs = False, auto_partition_low_quality_segments = False)
#                               rpsfile = "./sampledata/all_rest_pupil_sizes.tsv")
    
    ######

    if params.DEBUG or params.VERBOSE == "VERBOSE":
        #explore_validation_threshold_segments(ps, auto_partition_low_quality_segments = False)
        output_Validity_info_Segments(ps, auto_partition_low_quality_segments_flag = False, validity_method = 3)
        output_percent_discarded(ps,'./outputfolder/disc_multiprocessing.csv')
        output_Validity_info_Segments(ps, auto_partition_low_quality_segments_flag = False, validity_method = 2, threshold_gaps_list = [100, 200, 250, 300],output_file = "./outputfolder/Seg_val_multiprocessing.csv")
        output_Validity_info_Participants(ps, include_restored_samples =True, auto_partition_low_quality_segments_flag = False)


    # WRITE features to file
    if params.VERBOSE != "QUIET":
        print
        print "Exporting:\n--General:", params.featurelist
    write_features_tsv(ps, './outputfolder/testing.tsv', featurelist=params.featurelist, id_prefix=False)

    #prop_valid_fix_per_segs(ps, './outputfolder/validity_function_Nov27_80.txt')

    #aoi_feat_names = (map(lambda x: x, params.aoigeneralfeat))
    #write_features_tsv(ps, './outputfolder/tobiiv3_nov23_full.tsv', featurelist=params.featurelist, aoifeaturelist=aoi_feat_names, id_prefix=False)

    ##### WRITE AOI sequences to file
    #aoi_feat_names = (map(lambda x:x, params.aoigeneralfeat))
    #write_features_tsv(ps, './outputfolder/sequences_nov23_full.tsv',featurelist = params.aoisequencefeat, aoifeaturelist=aoi_feat_names, id_prefix = False)

    #### Export pupil dilations for each scene to a separate file
    #print "--pupil dilation trends" 
    #plot_pupil_dilation_all(ps, './outputfolder/pupilsizes/', "problem1")
    #plot_pupil_dilation_all(ps, './outputfolder/pupilsizes/', "problem2")
